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
import six
import unittest
from glob import iglob
from io import open
from string import Template, punctuation
from unittest import TestCase


accents = re.compile("([^\w\s%s]+)" % re.escape(punctuation))
courts = re.compile("(^\s{4}?{)((.*\n){1,100}?)(\s{4}?},)")


def load_courts_db():
    """Load the court data from disk, and render regex variables

    Court data is on disk as one main JSON file, another containing variables,
    and several others containing placenames. These get combined via Python's
    template system and loaded as a Python object

    :return: A python object containing the rendered courts DB
    """
    with open(os.path.join("data", "variables.json"), "r") as v:
        variables = json.load(v)

    for path in iglob(os.path.join("data", "places", "*.txt")):
        with open(path, "r") as p:
            places = "(%s)" % "|".join(p.read().splitlines())
            variables[path.split(os.path.sep)[-1].split(".txt")[0]] = places

    with open(os.path.join("data", "courts.json"), "r") as f:
        s = Template(f.read()).substitute(**variables)
    s = s.replace("\\", "\\\\")

    return json.loads(s)


def gather_regexes(courts, bankruptcy=False, court_id=None):
    """Create a variable mapping regexes to court IDs

    :param courts: The court DB
    :type courts: list
    :param bankruptcy: Whether to include bankruptcy courts in the final
    mapping.
    :type bankruptcy: bool
    :return: A list of two-tuples, with tuple[0] being a compiled regex and
    tuple[1] being the court ID.
    :rtype: list
    """
    regexes = []
    for court in courts:
        if bankruptcy == False:
            if court["type"] == "bankruptcy":
                continue
        for reg_str in court["regex"]:
            regex = re.compile(reg_str, (re.I | re.U))
            regexes.append((regex, court["id"]))

    if court_id is not None:
        regexes = list(filter(lambda x: x[1] == court_id, regexes))

    return regexes


def find_court(court_str, filed_date=None, regexes=None, bankruptcy=False):
    """

    :param court_str:
    :param filed_date:
    :param regexes:
    :return:
    """
    cd = {}
    cdd = []
    court_matches = []
    assert (
        type(court_str) == six.text_type
    ), "court_str is not a text type, it's of type %s" % type(court_str)
    for regex, court_id in regexes:
        match = re.search(regex, court_str)
        if match:
            court_matches.append(court_id)
            cd[match.group()] = court_id
            cdd.append({"id": court_id, "text": match.group()})
            # print(cdd)

    results = list(set(court_matches))
    if len(results) > 1:
        flist = []
        remove_list = [x["text"] for x in cdd]
        subsetlist = []

        for test in remove_list:
            for item in [x for x in remove_list if x != test]:
                if test in item:
                    subsetlist.append(test)
        final_list = [x for x in remove_list if x not in subsetlist]
        for r in cdd:
            if r["text"] in final_list:
                if bankruptcy == True:
                    pass
                else:
                    court_key = r["id"]
                    if court_key != "" and court_key is not None:
                        if court_key[-1] != "b":
                            flist.append(r["id"])
        return flist

    return court_matches


class DataTest(TestCase):
    """Data tests are used to confirm our data set is functional."""

    try:
        courts = load_courts_db()
        regexes = gather_regexes(courts)
    except:
        pass

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
        courts = load_courts_db()

        court_id = "mdcrctct"
        court = [x for x in courts if x["id"] == court_id][0]
        regexes = gather_regexes(courts)

        for example in court["examples"]:
            print("Testing ... %s" % example),
            matches2 = find_court(court_str=example, regexes=regexes)
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
