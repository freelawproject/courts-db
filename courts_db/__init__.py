from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import json
import os
import re
from datetime import datetime
from glob import iglob
from io import open
from string import Template, punctuation
from typing import List, Optional, Tuple, Union

import six

from courts_db.text_utils import strip_punc

from .utils import gather_regexes, load_courts_db, make_court_dictionary

try:
    courts = load_courts_db()
    court_dict = make_court_dictionary(courts)
    regexes = gather_regexes(courts)
except Exception as e:
    print(str(e))


def find_court_ids_by_name(court_str: str, bankruptcy: bool) -> List[str]:
    """Find court IDs with our courts-db regex list

    :param court_str: test string
    :param bankruptcy: Are we searhing for a bankruptcy court
    :return: List of Court IDs matched
    """
    assert (
        type(court_str) == six.text_type
    ), "court_str is not a text type, it's of type %s" % type(court_str)

    court_matches = set()
    matches = []
    for regex, court_id, court_name, court_type in regexes:
        # Filter gathered regexes by bankruptcy flag.
        if bankruptcy is True:
            if court_type != "bankruptcy":
                continue
        elif bankruptcy is False:
            if court_type == "bankruptcy":
                continue
        match = re.search(regex, court_str)
        if match:
            m = (match.group(0), court_id)
            matches.append(m)

    matched_strings = [m[0] for m in matches]
    filtered_list = filter(
        lambda x: [x for i in matched_strings if x in i and x != i] == [],
        matched_strings,
    )
    for item in list(filtered_list):
        for mat in matches:
            if item == mat[0]:
                court_matches.add(mat[1])
    return list(court_matches)


def filter_courts_by_date(matches, date_found, strict_dates=False):
    """Filter IDs by date found.

    Strict dates should be more useful as dates are filled in.
    :param matches:
    :param date_found: datetime object
    :param strict_dates: Boolean that helps tell the sytsem how to handle
    null dates in courts-db
    :return: List of court IDs matched
    """
    assert (
        type(date_found) is datetime
    ), "date_found is not a date object, it's of type %s" % type(date_found)

    results = [court for court in courts if court["id"] in matches]
    filtered_results = []
    for result in results:
        for date_object in result["dates"]:
            date_start = date_object["start"]
            date_end = date_object["end"]
            if strict_dates == False:
                if date_start == None:
                    date_start = "1600-01-01"
                if date_end == None:
                    date_end = "2100-01-01"
            if strict_dates:
                if date_start == None:
                    continue
                if date_end == None:
                    date_end = "2100-01-01"

            date_start = datetime.strptime(date_start, "%Y-%m-%d")
            date_end = datetime.strptime(date_end, "%Y-%m-%d")

            if date_start <= date_found <= date_end:
                filtered_results.append(result["id"])

    return filtered_results


def filter_courts_by_bankruptcy(matches, bankruptcy):
    results = [court for court in courts if court["id"] in matches]
    if bankruptcy:
        return [
            court["id"] for court in results if court["type"] == "bankruptcy"
        ]
    return [court["id"] for court in results if court["type"] != "bankruptcy"]


def find_court_by_id(court_id):
    """Find court dictionary using court id code.

    :param court_id: Court code used by Courtlistener.com
    :return: Return dictionary court object from db
    """
    return [court for court in courts if court["id"] == court_id]


def find_court(
    court_str, bankruptcy=None, date_found=None, strict_dates=False
):
    """Finds a list of court ID for a given string and parameters

    :param court_str: The unicode string we are testing
    :param bankruptcy: Tells function to exclude or include bankruptcy cases
    :param date_found: Date object
    :param strict_dates: Boolean that helps tell the sytsem how to handle
    null dates in courts-db
    :return: List of court IDs if any
    """
    court_str = strip_punc(court_str)
    matches = find_court_ids_by_name(court_str, bankruptcy)
    if bankruptcy is not None:
        matches = filter_courts_by_bankruptcy(
            matches=matches, bankruptcy=bankruptcy
        )
    if date_found:
        matches = filter_courts_by_date(
            matches=matches, date_found=date_found, strict_dates=strict_dates
        )

    return matches
