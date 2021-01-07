Courts-DB
=========

Courts-DB is an open source repository to organize a db of all courts current and historical.
It was built for use in Courtlistener.com.

Its main goal is to interface with CL to identify historical and current courts
by string.  It incldues mechanisms to filter results based on dates and/or whether it is a bankruptcy court.

Further development is intended and all contributors, corrections and additions are welcome.

Background
==========

Free Law Project built this database using the metadata (case names, dates etc.)
of over 16 millions data points.  This data represents hundreds of hours of
research and testing.  We believe to be the most extensive open dataset of its kind.

Quickstart
===========

You can feed in a courtlistener Court_ID or string to find a court.

::

        from courts_db import find_court, find_court_by_id

        find_court_by_id("mass")

        returns:
        [{
            "regex": [
                "${sjc} ${ma}?",
                "${ma} ${sjc}",
                "Supreme Court Of ${ma}",
                "State Of ${ma} Supreme Court"
            ],
            "name_abbreviation": "Mass. Sup. Jud. Ct.",
            "dates": [
                {
                    "start": "1692-01-01",
                    "end": null
                }
            ],
            "name": "Massachusetts Supreme Judicial Court",
            "level": "colr",
            "case_types": ["All"],
            "system": "state",
            "examples": [
                "Supreme Court Of Massachusetts",
                "Supreme Judicial Court Of Massachusetts",
                "Massachusetts Supreme Judicial Court"
            ],
            "court_url": "http://www.mass.gov/courts/sjc/",
            "type": "appellate",
            "id": "mass",
            "location": "Massachusetts",
            "citation_string": "Mass."
        }]


::

        from courts_db import find_court

        mass_sjc = find_court(u"Massachusetts Supreme Judicial Court")

        returns: ["mass"]


Filtering on less unique strings is built in.

Feed a date string or bankruptcy flag to filter on those parameters
For example District of Massachusetts is non unique and returns both the Federal District Court of Massachusetts and its Bankruptcy Court
::

        from datetime import datetime as dt

        courts_db.find_court(
            u"District of Massachusetts",
        )

        returns ==> ["mad", "mab"]

        courts_db.find_court(
            u"District of Massachusetts",
            bankruptcy=True,
        )

        returns ==> ["mab"]

        courts_db.find_court(
            u"District of Massachusetts",
            date_found=dt.strptime("10/02/1975", "%m/%d/%Y"),
        )

        returns ==> ["mad"]


Some Notes on the Data
======================
Somethings to keep in mind as you are reviewing the data.

1. The data is devided into two files courts.json and variables.json
2. Courts.json holds the bulk of the information
3. Variables.json holds templates for large numbers of regexes.

Fields
======

1. :code:`id` ==> string; Courtlistener Court Identifier
2. :code:`court_url` ==> string; url for court website
3. :code:`regex` ==>  array; regexes patterns to find courts
4. :code:`examples` ==>  array; regexes patterns to find courts
5. :code:`name` ==> string; full name of the court
6. :code:`name_abbreviation` ==> string; court name abbreviations
7. :code:`dates` ==> Array; Contains start date, end date and notes on date range
8. :code:`system` ==> string; Defines main jurisdiction, ex. State, Federal, Tribal
9. :code:`level` ==> string; code defining where court is in system structure, ex. COLR (Court of Last Resort), IAC (Intermediate Appellate Court), GJC (General Jurisdiction Court), LJC (Limited Jurisdiction Court)
10. :code:`location` ==> string; refers to the physical location of the main court
11. :code:`type` ==> string; Identifies kind of cases handled (Trial, Appellate, Bankruptcy, AG)
12. :code:`citation_string` ==> string; Identifies the string used in a citation to refer to the court

Installation
============

Installing courts-db is easy.

    ::

        pip install courts_db


Or install the latest dev version from github

    ::

        pip install git+https://github.com/freelawproject/courts-db.git@master



Future
=======

1) Continue to improve and expand the dataset.
2) Add filtering mechanisms by state, reporters, citation(s), judges, counties and cities.


Deployment
==========

If you wish to create a new version manually, the process is:

1. Update version info in ``setup.py``

2. Install the requirements in requirements_dev.txt

3. Set up a config file at ~/.pypirc

4. Generate a universal distribution that worksin py2 and py3 (see setup.cfg)

    ::

        python setup.py sdist bdist_wheel

5. Upload the distributions

    ::

        twine upload dist/* -r pypi (or pypitest)



License
=======

This repository is available under the permissive BSD license, making it easy and safe to incorporate in your own libraries.

Pull and feature requests welcome. Online editing in Github is possible (and easy!)
