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

# from .text_utils import strip_punc

accents = re.compile("([^\w\s%s]+)" % re.escape(punctuation))
db_root = os.path.dirname(os.path.realpath(__file__))



def load_courts_db():
    """Load the court data from disk, and render regex variables

    Court data is on disk as one main JSON file, another containing variables,
    and several others containing placenames. These get combined via Python's
    template system and loaded as a Python object

    :return: A python object containing the rendered courts DB
    """

    with open(os.path.join(db_root, 'data', 'variables.json')) as f:
        variables = json.load(f)

    for path in iglob(os.path.join(db_root, 'data', 'places', '*.txt')):
        with open(path, "r") as p:
            places = "(%s)" % "|".join(p.read().splitlines())
            variables[path.split(os.path.sep)[-1].split(".txt")[0]] = places

    with open(os.path.join(db_root, 'data', 'courts.json'), "r") as f:
        s = Template(f.read()).substitute(**variables)

    s = s.replace("\\", "\\\\")

    return json.loads(s)

def get_court_list(fp):
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


def make_court_dictionary(courts):
    cd = {}
    for court in courts:
        cd[court['id']] = court
    return cd


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


def find_court_id(court_str, filed_date=None, regexes=None, bankruptcy=False):
    """

    :param court_str:
    :param filed_date:
    :param regexes:
    :return:
    """
    courts = load_courts_db()
    regexes = gather_regexes(courts)
    court_str = unicode(court_str)

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
        court_matches = []
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
                            court_matches.append(r["id"])

    if len(court_matches) == 0:
        return None
    assert len(court_matches)==1, "Too many matches"
    return court_matches[0]


def find_court(court_str, filed_date=None, regexes=None, bankruptcy=False):
    """

    :param court_str:
    :param filed_date:
    :param regexes:
    :return:
    """
    courts = load_courts_db()
    regexes = gather_regexes(courts)
    court_str = unicode(court_str)
    court_dict = make_court_dictionary(courts)

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

        return [court_dict[x] for x in flist]

    return [court_dict[x] for x in court_matches]
