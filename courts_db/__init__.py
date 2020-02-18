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

courts = load_courts_db()
regexes = gather_regexes(courts)
court_dict = make_court_dictionary(courts)


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

    court_matches = list(set(court_matches))

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
