import json
import os
import re
from glob import iglob
from io import open
from string import Template, punctuation

db_root = os.path.dirname(os.path.realpath(__file__))

ordinals = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
    "nineth",
    "tenth",
    "eleventh",
    "twelveth",
    "thirteenth",
    "fourteenth",
    "fifteenth",
    "sixteenth",
    "seventeenth",
    "eighteenth",
    "nineteenth",
    "twentieth",
    "twenty(-| )first",
    "twenty(-| )secondth",
    "twenty(-| )third",
    "twenty(-| )fourth",
    "twenty(-| )fifth",
    "twenty(-| )sixth",
    "twenty(-| )seventh",
    "twenty(-| )eighth",
    "twenty(-| )nineth",
    "thirtieth",
    "thirty(-| )first",
    "thirty(-| )secondth",
    "thirty(-| )third",
    "thirty(-| )fourth",
    "thirty(-| )fifth",
    "thirty(-| )sixth",
    "thirty(-| )seventh",
    "thirty(-| )eighth",
    "thirty(-| )nineth",
    "fortieth",
    "fourty(-| )first",
    "fourty(-| )secondth",
    "fourty(-| )third",
    "fourty(-| )fourth",
    "fourty(-| )fifth",
    "fourty(-| )sixth",
    "fourty(-| )seventh",
    "fourty(-| )eighth",
    "fourty(-| )nineth",
    "fiftieth",
    "fifty(-| )first",
    "fifty(-| )secondth",
    "fifty(-| )third",
    "fifty(-| )fourth",
    "fifty(-| )fifth",
    "fifty(-| )sixth",
    "fifty(-| )seventh",
    "fifty(-| )eighth",
    "fifty(-| )nineth",
    "sixtieth",
    "sixty(-| )first",
    "sixty(-| )secondth",
    "sixty(-| )third",
    "sixty(-| )fourth",
    "sixty(-| )fifth",
    "sixty(-| )sixth",
    "sixty(-| )seventh",
    "sixty(-| )eighth",
    "sixty(-| )nineth",
    "seventieth",
    "seventy(-| )first",
    "seventy(-| )secondth",
    "seventy(-| )third",
    "seventy(-| )fourth",
    "seventy(-| )fifth",
    "seventy(-| )sixth",
    "seventy(-| )seventh",
    "seventy(-| )eighth",
    "seventy(-| )nineth",
    "eightieth",
    "eighty(-| )first",
    "eighty(-| )secondth",
    "eighty(-| )third",
    "eighty(-| )fourth",
    "eighty(-| )fifth",
    "eighty(-| )sixth",
    "eighty(-| )seventh",
    "eighty(-| )eighth",
    "eighty(-| )nineth",
    "ninetieth",
    "ninety(-| )first",
    "ninety(-| )secondth",
    "ninety(-| )third",
    "ninety(-| )fourth",
    "ninety(-| )fifth",
    "ninety(-| )sixth",
    "ninety(-| )seventh",
    "ninety(-| )eighth",
    "ninety(-| )nineth",
    "one[- ]hundredth",
]

# def get_court_data_from_ids(id_list):
#     cd = {}
#     for id in id_list:
#         cd[id] = court
#     return cd


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

    # Add in code to allow ordinal creation for many many judicial district numbers
    # for example 1 to 56 judicial districts
    with open(os.path.join(db_root, "data", "courts.json"), "r") as f:
        temp = f.read()
        ord_arrays = re.findall(r"\${(\d+)-(\d+)}", temp)
        for ord in ord_arrays:
            re_ord = f"(({')|('.join(ordinals[int(ord[0])-1: int(ord[1])])}))"
            temp = temp.replace(f"${{{ord[0]}-{ord[1]}}}", re_ord)

    with open(os.path.join(db_root, "data", "courts.json"), "r") as f:
        s = Template(temp).substitute(**variables)
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
        # Add a regex for the court's citation string, e.g. "W.D. Wash."
        # See #61: https://github.com/freelawproject/courts-db/issues/61
        regexes.append(
            (
                citation_to_regex(court["citation_string"]),
                court["id"],
                court["name"],
                court["type"],
                court.get("location"),
            )
        )

    return regexes


def citation_to_regex(citation_str: str):
    """
    Tricky ones:
        D. Alaska       No trailing period
    """
    # Skip most of this if there are no periods.
    if citation_str.count(".") > 0:
        reg_str = ""
        reg_elements = citation_str.split(".")
        for element in reg_elements:
            if element != "":
                reg_str += f"{element.strip()}\\.\\s?"
        # Trim last \s? from regex pattern
        if reg_str.endswith("\\s?"):
            reg_str = reg_str[:-3]
        # Make last period optional to avoid some weirdness like ""
        regex = re.compile(reg_str, (re.I | re.U))
        print(f"regex pattern: {regex.pattern}")
        return regex.pattern
    # Just return the original string if nothing is abbreviated with periods.
    else:
        return citation_str


def write_citation_regexes():
    data = None
    output_data = []

    # Read current courts.json file
    with open(os.path.join(db_root, "data", "courts.json"), "r") as f:
        data = json.load(f)

    # Loop over it
    for court in data:
        print(court["id"])

        # Don't bother unless there is a citation string listed for the court.
        if "citation_string" in court and court["citation_string"] != "":

            citation_str = court["citation_string"]

            # Add the citation string to the examples if it's not there already.
            if citation_str not in court["examples"]:
                print(f"Adding citation string \"{citation_str}\" to \"examples\" for court {court['id']}")
                court["examples"].append(citation_str)
            
            # Compute a regex
            regex = citation_to_regex(citation_str)
            if regex not in court["regex"]:
                print(f"Adding regex {regex} to \"regex\" for court {court['id']}")
                court["regex"].append(regex)
        
        output_data.append(court)
    
    # Write file
    with open(os.path.join(db_root, "data", "courts2.json"), "w") as output_f:
        json.dump(output_data, output_f, indent=4)

    print("Done!")
