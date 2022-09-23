import re
from datetime import datetime
from typing import List, Optional

from courts_db.text_utils import strip_punc

from .utils import gather_regexes, load_courts_db, make_court_dictionary

__all__ = [
    # lazy-loaded data structures:
    "courts",
    "court_dict",
    "regexes",
    # helper functions:
    "find_court_ids_by_name",
    "filter_courts_by_date",
    "filter_courts_by_bankruptcy",
    "find_court_by_id",
    "find_court",
]


def __getattr__(name):
    """Lazy load data structures from loaders module."""
    if name == "courts":
        value = load_courts_db()
    elif name == "court_dict":
        from . import courts

        value = make_court_dictionary(courts)
    elif name == "regexes":
        from . import courts

        value = gather_regexes(courts)
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")
    globals()[name] = value
    return value


def find_court_ids_by_name(
    court_str: str,
    bankruptcy: Optional[bool],
    location: Optional[str],
    allow_partial_matches: bool,
) -> List[str]:
    """Find court IDs with our courts-db regex list

    :param court_str: test string
    :param bankruptcy: Are we searhing for a bankruptcy court
    :return: List of Court IDs matched
    """
    from . import regexes

    assert isinstance(
        court_str, str
    ), f"court_str is not a text type, it's of type {type(court_str)}"

    court_matches = set()
    matches = []
    for regex, court_id, court_name, court_type, court_location in regexes:
        # If location provided - check if overlapped.
        if location and court_location != location:
            continue
        # Filter gathered regexes by bankruptcy flag.
        if bankruptcy is True:
            if court_type != "bankruptcy":
                continue
        elif bankruptcy is False:
            if court_type == "bankruptcy":
                continue
        match = re.search(regex, court_str)
        if match:
            if not allow_partial_matches:
                if len(court_str) != match.span()[1] - match.span()[0]:
                    continue
            m = (match.group(0), court_id)
            matches.append(m)
    # If no matches found - check against - Court Name - not regex patterns.
    if not matches:
        for court in courts:
            # Add validation for location if provided.
            if location and court_location != location:
                continue
            if strip_punc(court_str) == strip_punc(court["name"]):
                matches.append((court_str, court["id"]))

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
    from . import courts

    assert (
        type(date_found) is datetime
    ), f"date_found is not a date object, it's of type {type(date_found)}"

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
    from . import courts

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
    from . import courts

    return [court for court in courts if court["id"] == court_id]


def _filter_parents_from_list(matches: List[str]) -> List[str]:
    """Remove parents from the list of matches.

    Check if a match has a parent in the list.  If so remove it.

    :param matches: List of court ids
    :return: List of court ids without parents
    """
    parents = []
    for match in matches:
        parent = find_court_by_id(match)[0].get("parent", None)
        if parent in matches:
            parents.append(parent)
    if parents:
        matches = list(set(matches) ^ set(parents))
    return matches


def find_court(
    court_str: str,
    bankruptcy: Optional[bool] = None,
    date_found: Optional[datetime] = None,
    strict_dates: Optional[bool] = False,
    location: Optional[str] = None,
    allow_partial_matches: Optional[bool] = False,
) -> List[str]:
    """Finds a list of court ID for a given string and parameters

    :param court_str: The unicode string we are testing
    :param bankruptcy: Tells function to exclude or include bankruptcy cases
    :param date_found: Date object
    :param strict_dates: Boolean that helps tell the system how to handle
    :param location: Where the court is located.
    :allow_partial_matches: Allow partial string matches useful if given a sent.
    :return: List of court IDs if any
    """
    court_str = strip_punc(court_str)
    matches = find_court_ids_by_name(
        court_str, bankruptcy, location, allow_partial_matches
    )
    # print(matches)

    # Check bankruptcy cases if appropriate
    if bankruptcy is not None:
        matches = filter_courts_by_bankruptcy(
            matches=matches, bankruptcy=bankruptcy
        )

    # Match against dates
    if date_found:
        matches = filter_courts_by_date(
            matches=matches, date_found=date_found, strict_dates=strict_dates
        )

    # Check if the matches are parent/children of each other
    # for example California Court of Appeal, First Appellate District
    # is a child of California Court of Appeals
    # Reduce that list to just child element.
    if len(matches) > 1:
        matches = _filter_parents_from_list(matches)

    return matches
