# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from utils import load_courts_db, gather_regexes
from __init__ import find_court
from unittest import TestCase
from io import open

import unittest
import json
import os
import re


class DataTest(TestCase):
    """Data tests are used to confirm our data set is functional."""

    courts = load_courts_db()
    regexes = gather_regexes(courts)

    def test_all_examples(self):

        for court in self.courts:
            try:
                for example in court["examples"]:
                    matches = find_court(
                        court_str=example, regexes=self.regexes
                    )
                    results = list(set(matches))
                    if len(results) == 1:
                        if results == [court["id"]]:
                            continue
                    else:
                        print(
                            results,
                            [court["id"]],
                            "\txx\t",
                            example,
                            "\n",  # court['regex']
                        )
            except Exception as e:
                print(str(e))
                print("Fail at", court["name"])

    def test_specific_example(self):
        """"Can we process illappct correctly."""

        for court in self.courts:
            if court["id"] == "illappct":
                try:
                    for example in court["examples"]:
                        matches = find_court(
                            court_str=example,
                            filed_date=None,
                            regexes=self.regexes,
                        )
                        results = list(set(matches))
                        if len(results) == 1:
                            if results == [court["id"]]:
                                continue
                        else:
                            print(
                                results, [court["id"]], "\txx\t", example, "\n"
                            )  # court['regex']
                except Exception as e:
                    print((str(e)))
                    print("Fail at", court["name"])

    def test_unicode_handling(self):
        """Do we handle regex matching with accents or other non-ascii?"""
        sample_text = "Tribunal Dé Apelaciones De Puerto Rico"
        matches = find_court(court_str=sample_text, regexes=self.regexes)
        expected_matches = ["prapp"]
        self.assertEqual(matches, expected_matches)

    def test_one_example(self):
        """Can we extract the correct court id from string and date?"""

        bankruptcy = False

        court_id = "mdcrctct"
        court = [x for x in self.courts if x["id"] == court_id][0]

        for example in court["examples"]:
            print("Testing ... %s" % example),
            matches2 = find_court(court_str=example, regexes=self.regexes)
            self.assertEqual(
                list(set(matches2)), [court["id"]], "Failure %s" % matches2
            )
            print("√")

    def test_json(self):
        """Does our json load properly, and if not where are the issues"""

        name_regex = r'"name": "(?P<name>.*)",'
        court_regex = r"(^\s{4}?{)((.*\n){1,100}?)(\s{4}?},)"
        id_regex = r'"id": ("(?P<id>.*)"|null)'
        count = 1

        try:
            with open(os.path.join("data", "courts.json"), "r") as f:
                data = f.read()
                json.loads(data)
                print("JSON is correct. %s", "√√√")
                return

        except Exception as e:
            print("problem")
            pass

        matches = re.finditer(court_regex, data, re.MULTILINE)
        for match in enumerate(matches, start=1):
            court = match[1].group().strip(",")
            try:
                j = json.loads(court)
                continue
            except:
                pass

            id = re.search(id_regex, court).group("id")
            name = re.search(name_regex, court).group("name")
            print("Issues with (%s) -- %s" % (id, name))


if __name__ == "__main__":
    unittest.main()
