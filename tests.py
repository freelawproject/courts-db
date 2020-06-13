# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from courts_db.utils import load_courts_db, db_root
from courts_db.text_utils import strip_punc
from courts_db import find_court
from unittest import TestCase
from io import open

import unittest
import json
import os
import re

import jsonschema


def open_courts():
    return open(os.path.join(db_root, "data", "courts.json"), "r")


def open_schema():
    return open(os.path.join(".", "schema", "court.json"), "r")


class DataTest(TestCase):
    """Data tests are used to confirm our data set is functional."""

    try:
        courts = load_courts_db()
    except:
        print("JSON FAIL")
        pass

    def test_all_examples(self):
        for court in self.courts:
            bank = False
            try:
                if court["type"] == "bankruptcy":
                    bank = True

                for example in court["examples"]:
                    example = strip_punc(example)

                    matches = find_court(court_str=example, bankruptcy=bank)

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

    def test_json(self):
        """Does our json load properly, and if not where are the issues"""

        name_regex = r'"name": "(?P<name>.*)",'
        court_regex = r"(^\s{4}?{)((.*\n){1,100}?)(\s{4}?},)"
        id_regex = r'"id": ("(?P<id>.*)"|null)'
        count = 1

        try:
            with open_courts() as f:
                data = f.read()
                json.loads(data)
                print("JSON is correct. %s", "√√√")
                return

        except Exception as e:
            print("error")
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


class ValidationTest(TestCase):
    """Validation makes sure the database conforms to its JSON Schema."""

    try:
        courts = load_courts_db()
    except:
        print("JSON FAIL")
        pass

    def test_validates(self):
        instance, schema = None, None
        with open_courts() as f:
            data = f.read()
            instance = json.loads(data)
        with open_schema() as schema_f:
            schema_data = schema_f.read()
            schema = json.loads(schema_data)
        try:
            jsonschema.validate(
                instance=instance, schema=schema,
            )
        except jsonschema.ValidationError as exc:
            self.fail(f"JSON failed validation against schema: {exc}")


if __name__ == "__main__":
    unittest.main()
