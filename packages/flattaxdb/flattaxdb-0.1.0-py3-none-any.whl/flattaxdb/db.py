#!/usr/bin/env python3

from os.path import isfile
from collections import defaultdict
import logging
import pickle

logging.getLogger(__name__).addHandler(logging.NullHandler())


class TaxonDB:
    """Parse and query different taxonomic databases

    Aims
    ----
     * Work with taxonomic databases from data dump flatfiles.
     * Load them directly into memory for queries and other operations.
     * Use same internal data structures and methods for different source DBs.
     * Report output as far as possible with DwC terms.
     
    Databases supported
    -------------------
     * NCBI Taxonomy (names.dmp and nodes.dmp file from taxdump)
     * GBIF Backbone Taxonomy (Taxon.tsv file from backbone dump)
    """

    # Compulsory fields in table
    COMPULSORY = [
        "taxonID",
        "parentNameUsageID",
        "canonicalName",
        "taxonRank",
        "scientificName",
        "taxonomicStatus",
    ]

    RANKS_CANONICAL = [
        "kingdom",
        "phylum",
        "class",
        "order",
        "family",
        "genus",
        "species",
    ]

    def __init__(self):
        """Initialize TaxonDB object

        Fields
        ------
        db : dict
            Dict of records keyed by taxonID. Each record is a dict keyed by
            database fields, which are most DwC core terms.
        accepted : dict
            Dict of synonymous taxonIDs for each accepted taxonID. It is faster
            to index them when reading the database then compute them on the
            fly later in the function get_descendants().
        fields : list
            List of database fields, which are mostly DwC core terms.

        Parameters
        ----------
        dbpath : str
            Path to read or create SQLite3 database file
        """
        self.logger = logging.getLogger(__name__)
        self.db = {}
        self.accepted = {}  # dict of synonymous taxonIDs keyed by accepted taxonID
        self.fields = []
        return

    def pickle(self, path: str):
        with open(path, "wb") as fh:
            pickle.dump(self, fh)
        return

    def create_from_gbif(self, filepath):
        """Convert GBIF backbone taxonomy flatfile to database in-memory

        Parameters
        ----------
        filepath : str
            Path to `Taxon.tsv` file from GBIF Backbone archive
        """
        if not isfile(filepath):
            self.logger.warn("Flatfile %s is not a regular file", filepath)
            return None
        self.logger.info("Opening GBIF Taxon flatfile %s", filepath)
        # Get header line
        fh = open(filepath, "r")
        header = fh.readline()
        self.fields = header.rstrip().split("\t")
        # Check that compulsory fields are present
        if not all([i in self.fields for i in TaxonDB.COMPULSORY]):
            self.logger.error(
                "Compulsory field(s) missing, check Taxon flatfile header"
            )
            return None
        # Iterate across Taxon.tsv file
        # Header line already skipped above
        counter = 0
        for line in fh:
            counter += 1
            if counter % 500000 == 0:  # report progress
                self.logger.debug("... parsed %d entries", counter)
            # Dict of fields
            spl = line.rstrip("\n").split(
                "\t"
            )  # strip newlines only, else will remove trailing '\t'
            rec = dict(zip(self.fields, spl))
            # it is MUCH faster to index synonyms while reading DB than
            # doing it on the fly later
            if "acceptedNameUsageID" in rec and rec["acceptedNameUsageID"]:
                if rec["acceptedNameUsageID"] in self.accepted:
                    self.accepted[rec["acceptedNameUsageID"]].append(rec["taxonID"])
                else:
                    self.accepted[rec["acceptedNameUsageID"]] = [rec["taxonID"]]
            self.db[spl[0]] = rec

        # Commit last chunk
        self.logger.info("... parsed %d entries (total)", counter)
        # Close handles
        fh.close()
        return

    def create_from_ncbi(self, namespath, nodespath):
        """Convert NCBI taxonomy dump files to database in-memory

        Handling of `authority` field
        -----------------------------
        In the `names.dmp` file, names are classified as 'scientific name'
        (=canonicalName), 'authority' (=scientificName, including authority), as
        well as 'synonym'. There is only one scientific name per taxid, but there
        can be multiple synonyms. Authority versions of both the accepted
        scientific name and synonyms are all labeled as 'authority', so the
        respective authority version for each name or synonym must be matched.

        Handling of taxonIDs for synonyms
        ---------------------------------
        NCBI Taxonomy lists synonyms under the same taxonID as the accepted
        taxon name, unlike GBIF which assigns a separate taxonID to each name
        regardless of synonymy. For consistency, we create new dummy taxonIDs
        for synonyms, by appending `.[0-9]+` to the original taxonID.

        Missing information from taxdump flat files
        -------------------------------------------
        For several taxonIDs, the full scientific name with authority
        information is absent from the names.dmp file but accessible online in
        the browser interface to the NCBI Taxonomy.

        Parameters
        ----------
        namespath : str
            Path to `names.dmp` file from NCBI taxonomy dump archive
        nodespath : str
            Path to `nodes.dmp` file from NCBI taxonomy dump archive
        """

        # Check if files exist
        if not isfile(namespath):
            self.logger.warn("Flatfile %s is not a regular file", namespath)
            return None
        if not isfile(nodespath):
            self.logger.warn("Flatfile %s is not a regular file", nodespath)
            return None

        # Parse and hash names
        counter = 0
        taxid2names = defaultdict(lambda: defaultdict(list))
        self.logger.info("Parsing names dump file %s", namespath)
        with open(namespath, "r") as fh:
            for line in fh:
                counter += 1
                spl = line.rstrip("\t|\n").split("\t|\t")
                taxid2names[spl[0]][spl[3]].append(spl[1])
        self.logger.info("%d entries parsed (total)", counter)

        # Match authority to canonical name or synonyms and insert into database
        counter = 0
        self.logger.info("Matching scientific names to authorities")
        for taxid in taxid2names:
            # Report progress
            counter += 1
            if counter % 500000 == 0:
                self.logger.debug("... parsed %d entries", counter)
            # Parse accepted name
            if (
                len(taxid2names[taxid]["scientific name"]) > 1
            ):  # There should be only one scientific name
                self.logger.warning(
                    "More than one scientific name found for taxid %s", taxid
                )
            fields = {
                "taxonID": taxid,
                "acceptedNameUsageID": None,
                "canonicalName": taxid2names[taxid]["scientific name"][0],
                "taxonomicStatus": "accepted",
                "scientificName": None,
            }
            if "authority" in taxid2names[taxid]:
                authority_matches = [
                    a
                    for a in taxid2names[taxid]["authority"]
                    if taxid2names[taxid]["scientific name"][0] in a
                ]
                if len(authority_matches) > 0:
                    fields["scientificName"] = authority_matches[0]
            self.db[taxid] = fields

            # Parse synonyms
            # In NCBI Taxonomy, synonyms have the same taxonID as the accepted
            # name. To disambiguate them we add a suffix to the taxonID
            if "synonym" in taxid2names[taxid]:
                syn_auth = []
                for s in taxid2names[taxid]["synonym"]:
                    authority_matches = [
                        a for a in taxid2names[taxid]["authority"] if s in a
                    ]
                    if len(authority_matches) == 0:
                        syn_auth.append("")
                    else:
                        syn_auth.append(authority_matches[0])
                for i, pair in enumerate(zip(taxid2names[taxid]["synonym"], syn_auth)):
                    dummy_id = taxid + "." + str(i)
                    fields = {
                        "taxonID": dummy_id,
                        "acceptedNameUsageID": taxid,
                        "canonicalName": pair[0],
                        "taxonomicStatus": "synonym",
                        "scientificName": pair[1],
                    }
                    self.db[dummy_id] = fields
                    # Hash synonyms by accepted taxonID
                    if taxid in self.accepted:
                        self.accepted[taxid].append(dummy_id)
                    else:
                        self.accepted[taxid] = [dummy_id]
        self.logger.info("... parsed %d entries (total)", counter)

        # Parse nodes table (child-parent links)
        counter = 0
        self.logger.info("Parsing nodes dump file %s", nodespath)
        with open(nodespath, "r") as fh:
            for line in fh:
                if counter % 500000 == 0:
                    counter += 1
                    self.logger.debug("... parsed %d entries", counter)
                counter += 1
                spl = line.rstrip("\t|\n").split("\t|\t")
                [taxonID, parentNameUsageID, taxonRank] = spl[0:3]
                self.db[taxonID]["parentNameUsageID"] = parentNameUsageID
                self.db[taxonID]["taxonRank"] = taxonRank
                # Include this information for synonyms too
                if taxonID in self.accepted:
                    for synonym_taxonID in self.accepted[taxonID]:
                        self.db[synonym_taxonID]["parentNameUsage"] = parentNameUsageID
                        self.db[synonym_taxonID]["taxonRank"] = taxonRank
        self.logger.info("... parsed %d entries (total)", counter)

        # Save fields headers
        self.fields = [
            "taxonID",
            "parentNameUsageID",
            "acceptedNameUsageID",
            "scientificName",
            "canonicalName",
            "taxonRank",
            "taxonomicStatus",
        ]

        self.logger.info("NCBI flatfiles parsed")
        return

    #     def close(self):
    #         """Close database connection"""
    #         self.db.close()
    #         return

    def get_lineage(self, taxonID, canonical_ranks=False):
        """Get lineage from specified taxonID to root node

        Parameters
        ----------
        taxonID
            taxonID for the taxon of interest
        canonical_ranks : bool
            Return canonical ranks (kingdom, phylum, class, order, family,
            genus, species) only, do not return intermediate ranks.

        Returns
        -------
        list
            List of tuples (taxonID, canonicalName, taxonRank) ordered from
            specified node to the root node.
        """
        lineage = []
        target = taxonID
        while target:  # GBIF taxonomy: parent is null at root
            [taxonID, target, canonicalName, taxonRank] = [
                self.db[target][var]
                for var in [
                    "taxonID",
                    "parentNameUsageID",
                    "canonicalName",
                    "taxonRank",
                ]
            ]
            lineage.append((taxonID, canonicalName, taxonRank))
            if target == taxonID:  # NCBI taxonomy: taxonID == parent at the root
                break
        if canonical_ranks:
            lineage = [i for i in lineage if i[2] in TaxonDB.RANKS_CANONICAL]
        return lineage

    def get_taxtree(self, taxonIDs):
        """Get taxonomy tree from a list of taxonIDs

        Parameters
        ----------
        taxonIDs : list
            List of taxonIDs to place in common taxonomy tree

        Returns
        -------
        dict
            Dict of taxonIDs (keys) and their parent nodes (values). Key=value at root node.
        """
        lineages = []
        tax2parent = {}
        for taxonID in taxonIDs:
            target = taxonID
            while target:  # GBIF taxonomy: parent is null at root
                [taxonID, target, canonicalName, taxonRank] = [
                    self.db[target][var]
                    for var in [
                        "taxonID",
                        "parentNameUsageID",
                        "canonicalName",
                        "taxonRank",
                    ]
                ]
                if (taxonID, canonicalName, taxonRank) in lineages:
                    break
                lineages.append((taxonID, canonicalName, taxonRank))
                tax2parent[taxonID] = target
                if target == taxonID:  # NCBI taxonomy: taxonID == parent at the root
                    break
                if not target:  # GBIF taxonomy: parent is null at root
                    tax2parent[taxonID] = taxonID
        return tax2parent

    def find_name(self, name):
        """Get records matching a given canonical name

        Parameters
        ----------
        name : str
            canonicalName to search, must be exact match

        Returns
        -------
        list
            List of dicts for entries matching given taxonIDs
        """
        res = [self.db[i] for i in self.db if self.db[i]["canonicalName"] == name]
        if len(res) > 1:
            self.logger.warn("More than one match to name %s", name)
        return res

    def get_records(self, id_list: list):
        """Get list of records from list of taxonIDs

        Parameters
        ----------
        id_list : list
            List of taxonIDs to retrieve records

        Returns
        -------
        list
            List of dicts for entries matching given taxonIDs
        """
        return [self.db[i] for i in id_list]

    def get_synonyms(self, taxonID, nodoubtful=True):
        """Get synonyms of a given taxon

        Returns
        -------
        list
            List of dicts for entries matching given taxonIDs, including the
            entry with that given taxonID.
        """
        accepted = ""
        if self.db[taxonID]["taxonomicStatus"] == "accepted":
            accepted = taxonID
        elif (
            "acceptedNameUsageID" in self.db[taxonID]
            and self.db[taxonID]["acceptedNameUsageID"]
        ):
            accepted = self.db[taxonID]["acceptedNameUsageID"]
        else:
            self.logger.error(
                "Taxon %s not an accepted name but no acceptedNameUsageID specified",
                str(taxonID),
            )
            return None

        if accepted not in self.accepted:  # No synonyms, accepted name only
            return [self.db[accepted]]
        else:
            append = [self.db[i] for i in self.accepted[accepted]]
            if nodoubtful:
                append = [i for i in append if i["taxonomicStatus"] != "doubtful"]
            return [self.db[accepted]] + append

    def get_descendants(self, taxonID):
        """Get descendants of a given taxonID

        Returns
        -------
        list
            List of dicts for entries matching given taxonIDs
        """
        out = {
            i: {"data": self.db[i], "visited": False}
            for i in self.db
            if "parentNameUsageID" in self.db[i]
            and self.db[i]["parentNameUsageID"] == taxonID
        }
        lastlen = 0
        while lastlen < len(out):
            # If list doesn't grow => all taxa without descendants found
            lastlen = len(out)
            ids = [t for t in out if not out[t]["visited"]]
            # Faster to search in batches with IN than with multiple = statements
            res = {
                i: {"data": self.db[i], "visited": False}
                for i in self.db
                if "parentNameUsageID" in self.db[i]
                and self.db[i]["parentNameUsageID"] in ids
            }
            for t in out:  # Memoize which taxa already checked
                if t in ids:
                    out[t]["visited"] = True
            out.update(res)
        return [i["data"] for i in out.values()]
