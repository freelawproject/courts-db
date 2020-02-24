from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from .utils import (
    load_courts_db,
    gather_regexes,
    make_court_dictionary,
    find_state,
)
from string import Template, punctuation
from glob import iglob
from io import open

from datetime import datetime
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


def find_court_ids_by_name(court_str):

    if not type(court_str) == six.text_type:
        court_str = unicode(court_str)

    assert (
        type(court_str) == six.text_type
    ), "court_str is not a text type, it's of type %s" % type(court_str)

    court_matches = set()
    for regex, court_id, court_name, court_type in regexes:
        match = re.search(regex, court_str)
        if match:
            court_matches.add(court_id)

    return list(court_matches)


def filter_courts_by_date(found_ids, date_found, strict=False):
    """

    :param found_ids:
    :param date_found:
    :param strict:
    :return:
    """
    date_format = "%Y-%m-%d"
    results = [court for court in courts if court["id"] in found_ids]
    filtered_results = []
    for result in results:
        for date_object in result["dates"]:

            date_start = date_object["start"]
            date_end = date_object["end"]

            if strict == False:
                if date_start == None:
                    date_start = "1600-01-01"
                if date_end == None:
                    date_end = "2100-01-01"
            if strict:
                if date_start == None:
                    continue
                if date_end == None:
                    date_end = "2100-01-01"

            df = datetime.strptime(date_found, date_format)

            date_start = datetime.strptime(date_start, date_format)
            date_end = datetime.strptime(date_end, date_format)

            if date_start <= df <= date_end:
                filtered_results.append(result["id"])

    return filtered_results


def filter_courts_by_bankruptcy(found_ids, bankruptcy):
    results = [court for court in courts if court["id"] in found_ids]
    if bankruptcy:
        return [
            court["id"] for court in results if court["type"] == "bankruptcy"
        ]
    return [court["id"] for court in results if court["type"] != "bankruptcy"]


def filter_courts_by_state(found_ids, state):
    state = find_state(state)
    return [
        court["id"]
        for court in courts
        if court["id"] in found_ids and court["location"] == state
    ]


def find_court_by_id(court_id):
    return [court for court in courts if court["id"] == court_id]
