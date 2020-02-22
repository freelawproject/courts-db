from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from .utils import load_courts_db, gather_regexes, make_court_dictionary
from string import Template, punctuation
from glob import iglob
from io import open

import json
import os
import re
import six

try:
    courts = load_courts_db()
    court_dict = make_court_dictionary(courts)
    regexes = gather_regexes(courts)
except:
    pass


def find_court(court_str, filed_date=None, bankruptcy=False):
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
    for regex, court_id, court_name, court_type in regexes:
        match = re.search(regex, court_str)
        if match:
            court_matches.append(court_id)
            if court_id is None:
                court_id = court_name
            cd[match.group()] = court_id
            cdd.append(
                {
                    "id": court_id,
                    "text": match.group(),
                    "court_name": court_name,
                    "court_type": court_type,
                }
            )
            # print(cdd)

    results = list(set(court_matches))
    if len(results) > 1:
        court_matches = []
        remove_list = [x["text"] for x in cdd]
        subsetlist = []

        for test in remove_list:
            for item in [x for x in remove_list if x != test]:
                if test in item:
                    subsetlist.append(test)
        final_list = [x for x in remove_list if x not in subsetlist]

        for r in cdd:
            if r["text"] in final_list:
                court_key = r["id"]
                court_matches.append(court_key)

    court_matches = list(set(court_matches))

    if len(court_matches) > 1:
        new_cd = [x for x in cdd if x["id"] in court_matches]
        bank = list(
            set([x["id"] for x in new_cd if x["court_type"] == "bankruptcy"])
        )
        non_bank = list(
            set([x["id"] for x in new_cd if x["court_type"] != "bankruptcy"])
        )

        if bankruptcy == True:
            if len(bank) == 1:
                return bank
            else:
                if len(non_bank) == 1:
                    return non_bank
        else:
            if len(non_bank) == 1:
                return non_bank

    return court_matches


def find_court_info(court_str, filed_date=None, bankruptcy=False):
    """

    :param court_str:
    :param filed_date:
    :param bankruptcy:
    :return:
    """
    matches = find_court(court_str, filed_date, bankruptcy)
    return [court_dict[x] for x in matches]
