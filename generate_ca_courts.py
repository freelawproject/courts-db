#!/usr/bin/env python3
"""Generate all missing California Superior Court entries."""

import json

# California counties with their founding dates and court URLs
# Source: https://en.wikipedia.org/wiki/List_of_counties_in_California
# Court URLs from courts.ca.gov

CALIFORNIA_COUNTIES = [
    # Using short IDs to stay under 15 chars (calsuppct = 9 chars, max 6 for county)
    {
        "name": "Alameda",
        "date": "1853-03-25",
        "url": "https://www.alameda.courts.ca.gov/",
        "id": "ala",
    },
    {
        "name": "Alpine",
        "date": "1864-03-16",
        "url": "https://www.alpine.courts.ca.gov/",
        "id": "alp",
    },
    {
        "name": "Amador",
        "date": "1854-05-11",
        "url": "https://www.amadorcourt.org/",
        "id": "ama",
    },
    {
        "name": "Butte",
        "date": "1850-02-18",
        "url": "https://www.buttecourt.ca.gov/",
        "id": "but",
    },
    {
        "name": "Calaveras",
        "date": "1850-02-18",
        "url": "https://www.calaveras.courts.ca.gov/",
        "id": "cal",
    },
    {
        "name": "Colusa",
        "date": "1850-02-18",
        "url": "https://www.colusa.courts.ca.gov/",
        "id": "col",
    },
    {
        "name": "Contra Costa",
        "date": "1850-02-18",
        "url": "https://www.cc-courts.org/",
        "id": "cc",
    },
    {
        "name": "Del Norte",
        "date": "1857-03-02",
        "url": "https://www.delnorte.courts.ca.gov/",
        "id": "dn",
    },
    {
        "name": "El Dorado",
        "date": "1850-02-18",
        "url": "https://www.eldorado.courts.ca.gov/",
        "id": "eld",
    },
    {
        "name": "Fresno",
        "date": "1856-04-19",
        "url": "https://www.fresno.courts.ca.gov/",
        "id": "fre",
    },
    {
        "name": "Glenn",
        "date": "1891-03-11",
        "url": "https://www.glenn.courts.ca.gov/",
        "id": "gle",
    },
    {
        "name": "Humboldt",
        "date": "1853-05-12",
        "url": "https://www.humboldt.courts.ca.gov/",
        "id": "hum",
    },
    {
        "name": "Imperial",
        "date": "1907-08-15",
        "url": "https://www.imperial.courts.ca.gov/",
        "id": "imp",
    },
    {
        "name": "Inyo",
        "date": "1866-03-22",
        "url": "https://www.inyo.courts.ca.gov/",
        "id": "iny",
    },
    {
        "name": "Kern",
        "date": "1866-04-02",
        "url": "https://www.kern.courts.ca.gov/",
        "id": "ker",
    },
    {
        "name": "Kings",
        "date": "1893-03-22",
        "url": "https://www.kings.courts.ca.gov/",
        "id": "kin",
    },
    {
        "name": "Lake",
        "date": "1861-05-20",
        "url": "https://www.lake.courts.ca.gov/",
        "id": "lak",
    },
    {
        "name": "Lassen",
        "date": "1864-04-01",
        "url": "https://www.lassen.courts.ca.gov/",
        "id": "las",
    },
    # Los Angeles - already exists as calsuppctla
    {
        "name": "Madera",
        "date": "1893-03-11",
        "url": "https://www.madera.courts.ca.gov/",
        "id": "mad",
    },
    {
        "name": "Marin",
        "date": "1850-02-18",
        "url": "https://www.marin.courts.ca.gov/",
        "id": "mrn",
    },
    {
        "name": "Mariposa",
        "date": "1850-02-18",
        "url": "https://www.mariposa.courts.ca.gov/",
        "id": "mpa",
    },
    {
        "name": "Mendocino",
        "date": "1850-02-18",
        "url": "https://www.mendocino.courts.ca.gov/",
        "id": "men",
    },
    {
        "name": "Merced",
        "date": "1855-04-19",
        "url": "https://www.merced.courts.ca.gov/",
        "id": "mer",
    },
    {
        "name": "Modoc",
        "date": "1874-02-17",
        "url": "https://www.modoc.courts.ca.gov/",
        "id": "mod",
    },
    {
        "name": "Mono",
        "date": "1861-04-24",
        "url": "https://www.mono.courts.ca.gov/",
        "id": "mon",
    },
    {
        "name": "Monterey",
        "date": "1850-02-18",
        "url": "https://www.monterey.courts.ca.gov/",
        "id": "mnt",
    },
    {
        "name": "Napa",
        "date": "1850-02-18",
        "url": "https://www.napa.courts.ca.gov/",
        "id": "nap",
    },
    {
        "name": "Nevada",
        "date": "1851-04-25",
        "url": "https://www.nevada.courts.ca.gov/",
        "id": "nev",
    },
    {
        "name": "Orange",
        "date": "1889-03-11",
        "url": "https://www.occourts.org/",
        "id": "ora",
    },
    {
        "name": "Placer",
        "date": "1851-04-25",
        "url": "https://www.placer.courts.ca.gov/",
        "id": "pla",
    },
    {
        "name": "Plumas",
        "date": "1854-03-18",
        "url": "https://www.plumas.courts.ca.gov/",
        "id": "plu",
    },
    {
        "name": "Riverside",
        "date": "1893-03-11",
        "url": "https://www.riverside.courts.ca.gov/",
        "id": "riv",
    },
    {
        "name": "Sacramento",
        "date": "1850-02-18",
        "url": "https://www.saccourt.ca.gov/",
        "id": "sac",
    },
    {
        "name": "San Benito",
        "date": "1874-02-12",
        "url": "https://www.sanbenito.courts.ca.gov/",
        "id": "sbt",
    },
    {
        "name": "San Bernardino",
        "date": "1853-04-26",
        "url": "https://www.sb-court.org/",
        "id": "sbr",
    },
    {
        "name": "San Diego",
        "date": "1850-02-18",
        "url": "https://www.sdcourt.ca.gov/",
        "id": "sd",
    },
    # San Francisco - already exists as calsuppctsf
    {
        "name": "San Joaquin",
        "date": "1850-02-18",
        "url": "https://www.sjcourts.org/",
        "id": "sj",
    },
    {
        "name": "San Luis Obispo",
        "date": "1850-02-18",
        "url": "https://www.slo.courts.ca.gov/",
        "id": "slo",
    },
    {
        "name": "San Mateo",
        "date": "1856-04-19",
        "url": "https://sanmateo.courts.ca.gov/",
        "id": "sm",
    },
    {
        "name": "Santa Barbara",
        "date": "1850-02-18",
        "url": "https://www.santabarbara.courts.ca.gov/",
        "id": "sb",
    },
    {
        "name": "Santa Clara",
        "date": "1850-02-18",
        "url": "https://www.scscourt.org/",
        "id": "sc",
    },
    {
        "name": "Santa Cruz",
        "date": "1850-02-18",
        "url": "https://www.santacruzcourt.org/",
        "id": "scz",
    },
    {
        "name": "Shasta",
        "date": "1850-02-18",
        "url": "https://www.shasta.courts.ca.gov/",
        "id": "sha",
    },
    {
        "name": "Sierra",
        "date": "1852-04-16",
        "url": "https://www.sierra.courts.ca.gov/",
        "id": "sie",
    },
    {
        "name": "Siskiyou",
        "date": "1852-03-22",
        "url": "https://www.siskiyou.courts.ca.gov/",
        "id": "sis",
    },
    {
        "name": "Solano",
        "date": "1850-02-18",
        "url": "https://www.solano.courts.ca.gov/",
        "id": "sol",
    },
    {
        "name": "Sonoma",
        "date": "1850-02-18",
        "url": "https://www.sonomacourt.org/",
        "id": "son",
    },
    {
        "name": "Stanislaus",
        "date": "1854-04-01",
        "url": "https://www.stanct.org/",
        "id": "sta",
    },
    {
        "name": "Sutter",
        "date": "1850-02-18",
        "url": "https://www.sutter.courts.ca.gov/",
        "id": "sut",
    },
    {
        "name": "Tehama",
        "date": "1856-04-09",
        "url": "https://www.tehama.courts.ca.gov/",
        "id": "teh",
    },
    {
        "name": "Trinity",
        "date": "1850-02-18",
        "url": "https://www.trinity.courts.ca.gov/",
        "id": "tri",
    },
    {
        "name": "Tulare",
        "date": "1852-04-20",
        "url": "https://www.tulare.courts.ca.gov/",
        "id": "tul",
    },
    {
        "name": "Tuolumne",
        "date": "1850-02-18",
        "url": "https://www.tuolumne.courts.ca.gov/",
        "id": "tuo",
    },
    {
        "name": "Ventura",
        "date": "1872-03-22",
        "url": "https://www.ventura.courts.ca.gov/",
        "id": "ven",
    },
    {
        "name": "Yolo",
        "date": "1850-02-18",
        "url": "https://www.yolo.courts.ca.gov/",
        "id": "yol",
    },
    {
        "name": "Yuba",
        "date": "1850-02-18",
        "url": "https://www.yuba.courts.ca.gov/",
        "id": "yub",
    },
]

# Administrative tribunals
ADMIN_TRIBUNALS = [
    {
        "id": "calstatebar",
        "name": "State Bar Court of California",
        "name_abbreviation": "Cal. State Bar Ct.",
        "citation_string": "Cal. State Bar Ct.",
        "court_url": "https://www.statebarcourt.ca.gov/",
        "date": "1989-01-01",
        "level": "special",
        "type": "special",
        "notes": "Disciplinary tribunal for California attorneys. Has Hearing Department (trial level) and Review Department (appellate level).",
        "examples": [
            "State Bar Court of California",
            "California State Bar Court",
            "State Bar Court Review Department",
            "State Bar Court Hearing Department",
        ],
        "regex": [
            "State Bar Court of California",
            "California State Bar Court",
            "State Bar Court Review Department",
            "State Bar Court Hearing Department",
            "State Bar Court",
            "Cal\\.? State Bar Court",
            "State Bar of California Court",
        ],
    },
    {
        "id": "calwcab",
        "name": "Workers' Compensation Appeals Board of California",
        "name_abbreviation": "Cal. WCAB",
        "citation_string": "Cal. WCAB",
        "court_url": "https://www.dir.ca.gov/wcab/wcab.htm",
        "date": "1913-01-01",
        "level": "special",
        "type": "special",
        "notes": "Adjudicates workers' compensation disputes in California.",
        "examples": [
            "Workers' Compensation Appeals Board",
            "California WCAB",
            "Cal WCAB",
        ],
        "regex": [
            "Workers'? Compensation Appeals Board",
            "California WCAB",
            "Cal\\.? WCAB",
            "WCAB",
        ],
    },
    {
        "id": "calcuiab",
        "name": "California Unemployment Insurance Appeals Board",
        "name_abbreviation": "Cal. CUIAB",
        "citation_string": "Cal. CUIAB",
        "court_url": "https://www.cuiab.ca.gov/",
        "date": "1943-01-01",
        "level": "special",
        "type": "special",
        "notes": "Hears appeals of unemployment and disability insurance decisions.",
        "examples": [
            "California Unemployment Insurance Appeals Board",
            "CUIAB",
        ],
        "regex": [
            "California Unemployment Insurance Appeals Board",
            "Unemployment Insurance Appeals Board",
            "CUIAB",
        ],
    },
    {
        "id": "calperb",
        "name": "California Public Employment Relations Board",
        "name_abbreviation": "Cal. PERB",
        "citation_string": "Cal. PERB",
        "court_url": "https://perb.ca.gov/",
        "date": "1975-01-01",
        "level": "special",
        "type": "special",
        "notes": "Adjudicates public sector labor disputes.",
        "examples": [
            "Public Employment Relations Board",
            "California PERB",
            "PERB",
        ],
        "regex": [
            "Public Employment Relations Board",
            "California PERB",
            "Cal\\.? PERB",
            "PERB",
        ],
    },
    {
        "id": "calcpuc",
        "name": "California Public Utilities Commission",
        "name_abbreviation": "Cal. PUC",
        "citation_string": "Cal. PUC",
        "court_url": "https://www.cpuc.ca.gov/",
        "date": "1911-01-01",
        "level": "special",
        "type": "special",
        "notes": "Regulates utilities and has quasi-judicial authority.",
        "examples": [
            "California Public Utilities Commission",
            "CPUC",
            "Cal PUC",
        ],
        "regex": [
            "California Public Utilities Commission",
            "Public Utilities Commission",
            "CPUC",
            "Cal\\.? PUC",
        ],
    },
    {
        "id": "calalrb",
        "name": "California Agricultural Labor Relations Board",
        "name_abbreviation": "Cal. ALRB",
        "citation_string": "Cal. ALRB",
        "court_url": "https://www.alrb.ca.gov/",
        "date": "1975-01-01",
        "level": "special",
        "type": "special",
        "notes": "Adjudicates agricultural labor disputes under the ALRA.",
        "examples": [
            "Agricultural Labor Relations Board",
            "California ALRB",
            "ALRB",
        ],
        "regex": [
            "Agricultural Labor Relations Board",
            "California ALRB",
            "Cal\\.? ALRB",
            "ALRB",
        ],
    },
    {
        "id": "caloah",
        "name": "California Office of Administrative Hearings",
        "name_abbreviation": "Cal. OAH",
        "citation_string": "Cal. OAH",
        "court_url": "https://www.dgs.ca.gov/OAH",
        "date": "1945-01-01",
        "level": "special",
        "type": "special",
        "notes": "Provides administrative law judges for state agency hearings.",
        "examples": [
            "Office of Administrative Hearings",
            "California OAH",
            "OAH",
        ],
        "regex": [
            "Office of Administrative Hearings",
            "California OAH",
            "Cal\\.? OAH",
            "OAH",
        ],
    },
]


def generate_superior_court(county_data):
    """Generate a Superior Court entry for a county."""
    name = county_data["name"]
    county_id = county_data["id"]

    return {
        "case_types": [],
        "citation_string": "",
        "court_url": county_data["url"],
        "dates": [{"end": None, "start": county_data["date"]}],
        "examples": [
            f"Superior Court of California, County of {name}",
            f"{name} County Superior Court",
            f"Superior Court of {name} County",
            f"State of California Superior Court County of {name}",
        ],
        "id": f"calsuppct{county_id}",
        "jurisdiction": "C.A.",
        "level": "gjc",
        "location": "California",
        "name": f"{name} County Superior Court",
        "name_abbreviation": f"{name} Cnty. Super. Ct.",
        "parent": "calsuperct",
        "regex": [
            f"Superior Court of California,? County of {name}",
            f"{name} County Superior Court",
            f"Superior Court of {name} County",
            f"State of California Superior Court County of {name}",
            f"Superior Court.* {name} County.* California",
        ],
        "system": "state",
        "type": "trial",
    }


def generate_admin_tribunal(tribunal_data):
    """Generate an administrative tribunal entry."""
    return {
        "case_types": [],
        "citation_string": tribunal_data["citation_string"],
        "court_url": tribunal_data["court_url"],
        "dates": [{"end": None, "start": tribunal_data["date"]}],
        "examples": tribunal_data["examples"],
        "id": tribunal_data["id"],
        "jurisdiction": "C.A.",
        "level": tribunal_data["level"],
        "location": "California",
        "name": tribunal_data["name"],
        "name_abbreviation": tribunal_data["name_abbreviation"],
        "notes": tribunal_data["notes"],
        "regex": tribunal_data["regex"],
        "system": "state",
        "type": tribunal_data["type"],
    }


def main():
    # Load existing courts.json
    with open("courts_db/data/courts.json") as f:
        courts = json.load(f)

    # Find insertion point (after calsuppctsf)
    insert_idx = None
    for i, court in enumerate(courts):
        if court.get("id") == "calsuppctsf":
            insert_idx = i + 1
            break

    if insert_idx is None:
        print("Could not find calsuppctsf to insert after")
        return

    # Generate new courts
    new_courts = []

    # Add Superior Courts
    for county in CALIFORNIA_COUNTIES:
        new_courts.append(generate_superior_court(county))

    # Add admin tribunals
    for tribunal in ADMIN_TRIBUNALS:
        new_courts.append(generate_admin_tribunal(tribunal))

    # Insert new courts
    courts = courts[:insert_idx] + new_courts + courts[insert_idx:]

    # Write back
    with open("courts_db/data/courts.json", "w") as f:
        json.dump(courts, f, indent=4, sort_keys=False)

    print(
        f"Added {len(new_courts)} courts ({len(CALIFORNIA_COUNTIES)} Superior Courts + {len(ADMIN_TRIBUNALS)} admin tribunals)"
    )


if __name__ == "__main__":
    main()
