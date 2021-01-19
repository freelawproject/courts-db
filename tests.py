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
import unittest
from io import open
from json.decoder import JSONDecodeError
from unittest import TestCase

from courts_db import find_court
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

    def test_one_example(self):
        """Can we extract the correct court id from string and date?"""

        court_id = "mntax"
        court = [x for x in self.courts if x["id"] == court_id][0]

        for example in court["examples"]:
            example = strip_punc(example)
            print("Testing ... %s" % example),
            matches2 = find_court(court_str=example)
            self.assertEqual(
                list(set(matches2)), [court_id], "Failure %s" % matches2
            )
            print("Success.", matches2[0], "<=>", court_id)


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


if __name__ == "__main__":
    unittest.main()
