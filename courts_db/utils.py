import json
import os
import re
from glob import iglob
from io import open
from string import Template, punctuation

db_root = os.path.dirname(os.path.realpath(__file__))


def get_court_data_from_ids(id_list):
    cd = {}
    for id in id_list:
        cd[id] = court
    return cd


def make_court_dictionary(courts):
    cd = {}
    for court in courts:
        cd[court["id"]] = court
    return cd


def load_courts_db():
    """Load the court data from disk, and render regex variables

    Court data is on disk as one main JSON file, another containing variables,
    and several others containing placenames. These get combined via Python's
    template system and loaded as a Python object

    :return: A python object containing the rendered courts DB
    """
    with open(os.path.join(db_root, "data", "variables.json"), "r") as v:
        variables = json.load(v)

    for path in iglob(os.path.join(db_root, "data", "places", "*.txt")):
        with open(path, "r") as p:
            places = f"({'|'.join(p.read().splitlines())})"
            variables[path.split(os.path.sep)[-1].split(".txt")[0]] = places

    with open(os.path.join(db_root, "data", "courts.json"), "r") as f:
        s = Template(f.read()).substitute(**variables)
    s = s.replace("\\", "\\\\")
    data = json.loads(s)

    for k in data:
        # If a child of a parent court - add parent data to child if not present
        # this should allow for streamed down data.  Inheritance
        if "parent" in k.keys():
            if not {"dates", "type", "location"} <= set(k.keys()):
                parent = [x for x in data if x["id"] == k["parent"]][0]
                if "dates" not in k.keys():
                    k["dates"] = parent["dates"]
                if "type" not in k.keys():
                    k["type"] = parent["type"]
                if "location" not in k.keys():
                    k["location"] = parent["location"]

    return data


def gather_regexes(courts):
    """Create a variable mapping regexes to court IDs

    :param courts: The court DB
    :type courts: list
    :return: A list of tuples, with tuple[0] being a compiled regex,
    tuple[1] being the court ID, tuple[2] being the court name, and tuple[3]
    being the court type. Example: (<_sre.SRE_Pattern object>, u'ala',
    'Supreme Court of Alabama', 'appellate')
    :rtype: list
    """
    regexes = []
    for court in courts:
        for reg_str in court["regex"]:
            # Unwind the extra gruff in regexes
            reg_str = reg_str.replace("\\\\", "\\")
            regex = re.compile(reg_str, (re.I | re.U))
            regexes.append(
                (
                    regex,
                    court["id"],
                    court["name"],
                    court["type"],
                    court.get("location"),
                )
            )

    return regexes
