# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import json
import os
import re
import sys
import unittest
from collections import Counter
from io import open
from json.decoder import JSONDecodeError
from unittest import TestCase

from courts_db import find_court, find_court_by_id
from courts_db.text_utils import strip_punc
from courts_db.utils import db_root, load_courts_db


class CourtsDBTestCase(TestCase):
    def setUp(self):
        self.courts = load_courts_db()


class DataTest(CourtsDBTestCase):
    """Data tests are used to confirm our data set is functional."""

    def test_unicode_handling(self):
        """Do we handle regex matching with accents or other non-ascii?"""
        sample_text = "Tribunal Dé Apelaciones De Puerto Rico"
        matches = find_court(court_str=sample_text)
        expected_matches = ["prapp"]
        self.assertEqual(matches, expected_matches)

    def test_parent_courts(self):
        """Can we find the parent court"""

        court_str_example = (
            "California Court of Appeal, First Appellate District"
        )
        matches = find_court(court_str=court_str_example)
        self.assertEqual(
            find_court_by_id(matches[0])[0].get("parent", None), "calctapp"
        )

        court_str_example = "Supreme Court of the United States"
        matches = find_court(court_str=court_str_example)
        self.assertEqual(
            find_court_by_id(matches[0])[0].get("parent", None), None
        )

    def test_all_example(self):
        """Can we extract the correct court id from string and date?"""

        for court in self.courts:
            for court_str_example in court["examples"]:
                print(f"Testing {court_str_example}", end=" ... ")
                matches = find_court(court_str=court_str_example)
                self.assertIn(
                    court["id"],
                    matches,
                    f"Failure to find {court['id']} in {court_str_example}",
                )
                print("√")

    def test_location_filter(self):
        """Can we use location to filter properly"""

        court_ids = find_court("Calhoun County Circuit Court")
        self.assertEqual(
            sorted(court_ids),
            ["flacirct14cal", "micirct37cal"],
            msg="Court filtering failed",
        )

        florida_court_ids = find_court(
            "Calhoun County Circuit Court", location="Florida"
        )
        self.assertEqual(
            ["flacirct14cal"],
            florida_court_ids,
            msg="Florida county court not found",
        )

        michigan_court_ids = find_court(
            "Calhoun County Circuit Court", location="Michigan"
        )
        self.assertEqual(
            ["micirct37cal"],
            michigan_court_ids,
            msg="Michican county court not found",
        )


class ExamplesTest(CourtsDBTestCase):
    def test_all_non_bankruptcy_examples(self):
        for court in self.courts:
            if court["type"] == "bankruptcy":
                continue
            for example in court["examples"]:
                example = strip_punc(example)
                matches = find_court(court_str=example, bankruptcy=False)
                results = list(set(matches))
                self.assertIn(court["id"], results, msg=f"Failed {example}")

    def test_bankruptcy_examples(self):
        for court in self.courts:
            if court["type"] != "bankruptcy":
                continue
            for example in court["examples"]:
                example = strip_punc(example)
                matches = find_court(court_str=example, bankruptcy=True)
                results = list(set(matches))
                self.assertIn(court["id"], results, msg=f"Failed {example}")


class JsonTest(CourtsDBTestCase):
    def setUp(self) -> None:
        self.name_regex = r'"name": "(?P<name>.*)",'
        self.court_regex = r"(^\s{4}?{)((.*\n){1,100}?)(\s{4}?},)"
        self.id_regex = r'"id": ("(?P<id>.*)"|null)'

    def test_json(self):
        """Does our json load properly, and if not where are the issues"""
        try:
            # Load entire json to shortcircuit testing
            with open(os.path.join(db_root, "data", "courts.json"), "r") as f:
                data = f.read()
                json.loads(data)
                return
        except JSONDecodeError as e:
            print("Errors exist in the data structure")
            pass

        matches = re.finditer(self.court_regex, data, re.MULTILINE)
        for match in enumerate(matches, start=1):
            court = match[1].group().strip(",")
            try:
                # Load individual courts
                j = json.loads(court)
                continue
            except JSONDecodeError:
                pass
            id = re.search(self.id_regex, court).group("id")
            name = re.search(self.name_regex, court).group("name")
            print("Issues with (%s) -- %s" % (id, name))

    def test_unique_ids(self):
        """Are all court ids unique?"""
        court_ids = [row["id"] for row in load_courts_db()]
        c = Counter(court_ids)
        self.assertEqual(
            len(court_ids), len(list(set(court_ids))), msg=c.most_common(10)
        )

    def test_id_length(self):
        """Make sure Id length does not exceed 15 characters"""
        max_id_length = max([len(row["id"]) for row in load_courts_db()])
        ids = []
        if max_id_length > 15:
            print(
                "Ids are longer than 15 characters. This is not allowed. "
                "Please update the id to be 15 characters or less."
            )
            ids = [
                row["id"] for row in load_courts_db() if len(row["id"]) > 15
            ]
        self.assertLessEqual(
            max_id_length, 15, msg=f"#{len(ids)}: Ids longer than 15: {ids}"
        )


class LazyLoadTest(TestCase):
    def test_lazy_load(self):
        """Each lazy attribute should only exist after it is first used."""
        # reset courts_db module in case it was already loaded by another test
        sys.modules.pop("courts_db")
        import courts_db

        for attr in ("courts", "court_dict", "regexes"):
            self.assertNotIn(attr, dir(courts_db))
            self.assertIsNotNone(getattr(courts_db, attr, None))
            self.assertIn(attr, dir(courts_db))


if __name__ == "__main__":
    unittest.main()
