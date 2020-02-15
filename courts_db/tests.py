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

from courts_db.text_utils import strip_punc


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


def get_court_list(fp):
    print(fp)
    court_set = set()
    df = pandas.read_csv(fp, usecols=["court"])
    cl = df["court"].tolist()
    cl = [x for x in cl if type(x) == str]
    court_list = set(cl)

    for court_str in court_list:
        try:
            clean_str = strip_punc(court_str)
            court_set.add(clean_str)
        except Exception as e:
            print(court_str, str(e))

    return court_set


def gather_regexes(courts, bankruptcy=False):
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
            reg_str = reg_str.decode("unicode-escape")
            regex = re.compile(reg_str, (re.I | re.U))
            regexes.append((regex, court["id"]))
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
    for regex in regexes:
        if re.search(regex[0], court_str):
            court_matches.append(regex[1])

            cd[re.search(regex[0], court_str).group()] = regex[1]
            cdd.append(
                {
                    "id": regex[1],
                    "text": re.search(regex[0], court_str).group(),
                }
            )
            print(cdd)

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


class ConstantsTest(TestCase):
    """ """

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

    def test_str(self):
        # """Can we extract the correct court id from string and date?"""
        court_id = "prapp"

        sample_text = "Tribunal Dé Apelaciones De Puerto Rico"

        matches2 = find_court(court_str=sample_text, regexes=self.regexes)
        self.assertEqual(list(set(matches2)), [court_id], "Failure")

        print(list(set(matches2)), end=" ")
        print("√")

    def test_json(self):

        try:
            with open(os.path.join("data", "courts.json"), "r") as f:
                court_data = json.loads(f.read())
        except Exception as e:
            print(e)
            with open(os.path.join("data", "courts.json"), "r") as f:
                cd = f.read()

            matches = re.match(courts, cd)
            print(matches)
            # "(^\s{4}?{)((.*\n){1,100}?)(\s{4}?},)"


if __name__ == "__main__":
    unittest.main()
