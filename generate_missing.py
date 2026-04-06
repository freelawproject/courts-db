from typing import Any, Literal, TypedDict

import courts_db


class Court(TypedDict):
    case_types: list[Any]
    citation_string: str
    court_url: str
    dates: list[dict[str, Any]]
    examples: list[str]
    id: str
    level: str
    location: str
    name: str
    parent: str | None
    regex: list[str]
    system: Literal["state", "federal"]
    type: Literal["appellate", "special", "bankruptcy", "trial"] | None


with open("../missing_courts.txt") as f:
    courts = [court.strip() for court in f.readlines()]

missing = [court for court in courts if not courts_db.find_court(court)]

added: dict[str, Court] = {}


def add_court(court: Court):
    if court["id"] in added:
        added[court["id"]]["regex"].extend(court["regex"])
        added[court["id"]]["examples"].extend(court["examples"])
    else:
        added[court["id"]] = court


for court in missing:
    if "Texas" in court:
        if "District" in court:
            add_court(
                Court(
                    case_types=[],
                    citation_string="",
                    court_url="",
                    dates=[],
                    examples=[],
                    id="texdistct",
                    parent="",
                    level="",
                    location="Texas",
                    name=court,
                    regex=[],
                    system="state",
                    type="trial",
                )
            )
            continue
        if "County" in court:
            add_court(
                Court(
                    case_types=[],
                    citation_string="",
                    court_url="",
                    dates=[],
                    examples=[],
                    id="texcntyct",
                    parent="",
                    level="",
                    location="Texas",
                    name=court,
                    regex=[],
                    system="state",
                    type="trial",
                )
            )
            continue
    if "Court of Appeals of Ohio" in court:
        county = court.split()[-2:-1][0]
        district_counties = {
            1: ["Hamilton"],
            2: [
                "Champaign",
                "Clark",
                "Darke",
                "Greene",
                "Miami",
                "Montgomery",
            ],
            3: [
                "Allen",
                "Auglaize",
                "Crawford",
                "Defiance",
                "Hancock",
                "Hardin",
                "Henry",
                "Logan",
                "Marion",
                "Mercer",
                "Paulding",
                "Putnam",
                "Seneca",
                "Shelby",
                "Union",
                "Van Wert",
                "Wyandot",
            ],
            4: [
                "Adams",
                "Athens",
                "Gallia",
                "Highland",
                "Hocking",
                "Jackson",
                "Lawrence",
                "Meigs",
                "Pickaway",
                "Pike",
                "Ross",
                "Scioto",
                "Vinton",
                "Washington",
            ],
            5: [
                "Ashland",
                "Coshocton",
                "Delaware",
                "Fairfield",
                "Guernsey",
                "Holmes",
                "Knox",
                "Licking",
                "Morgan",
                "Morrow",
                "Muskingum",
                "Perry",
                "Richland",
                "Stark",
                "Tuscarawas",
            ],
            6: [
                "Erie",
                "Fulton",
                "Huron",
                "Lucas",
                "Ottawa",
                "Sandusky",
                "Williams",
                "Wood",
            ],
            7: [
                "Belmont",
                "Carroll",
                "Columbiana",
                "Harrison",
                "Jefferson",
                "Mahoning",
                "Monroe",
                "Noble",
            ],
            8: ["Cuyahoga"],
            9: ["Lorain", "Medina", "Summit", "Wayne"],
            10: ["Franklin"],
            11: ["Ashtabula", "Geauga", "Lake", "Portage", "Trumbull"],
            12: [
                "Brown",
                "Butler",
                "Clermont",
                "Clinton",
                "Fayette",
                "Madison",
                "Preble",
                "Warren",
            ],
        }
        for district, counties in district_counties.items():
            if county in counties:
                add_court(
                    Court(
                        case_types=[],
                        citation_string="",
                        court_url="",
                        dates=[],
                        examples=[],
                        id=f"ohctapp{district}{county.lower()}",
                        level="",
                        location="Ohio",
                        name=court,
                        parent="ohctapp",
                        regex=[],
                        system="state",
                        type="trial",
                    )
                )
                break
        continue
    # if "Pennsylvania" in court:
    print(court)
