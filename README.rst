Courts-DB
=========

Courts-DB is an open source repository to organize a database of all courts current and historical.
It was built for use in CourtListener.com.

Its main goal is to interface with CourtListener to identify historical and current courts
by string.  It includes mechanisms to filter results based on dates and/or whether it is a bankruptcy court.

Further development is intended and all contributors, corrections and additions are welcome.

Background
==========

Free Law Project built this database using the metadata (case names, dates etc.)
of over 16 millions data points.  This data represents hundreds of hours of
research and testing.  We believe this to be the most extensive open dataset of its kind.

Quickstart
===========

You can feed in a CourtListener Court Identifier or string to find a court.

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

Feed a date string or bankruptcy flag to filter on those parameters.
For example District of Massachusetts is non unique and returns both the Federal District Court of Massachusetts and its Bankruptcy Court.

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
Some things to keep in mind as you are reviewing the data:

1. The data is divided into two files ``courts.json`` and ``variables.json``.
2. ``courts.json`` holds the bulk of the information.
3. ``variables.json`` holds templates for large numbers of regexes.

Fields
======

1. ``id`` — string; CourtListener Court Identifier
2. ``court_url`` — string; url for court website
3. ``regex`` —  array; regexes patterns to find courts
4. ``examples`` —  array; regexes patterns to find courts
5. ``name`` — string; full name of the court
6. ``name_abbreviation`` — string; court name abbreviations
7. ``dates`` — Array; contains start date, end date and notes on date range
8. ``system`` — string; defines main jurisdiction, ex. State, Federal, Tribal
9. ``level`` — string; code defining where court is in system structure, ex. COLR (Court of Last Resort), IAC (Intermediate Appellate Court), GJC (General Jurisdiction Court), LJC (Limited Jurisdiction Court)
10. ``location`` — string; refers to the physical location of the main court
11. ``type`` — string; identifies kind of cases handled (Trial, Appellate, Bankruptcy, AG)
12. ``citation_string`` — string; identifies the string used in a citation to refer to the court
13. ``notes`` — string; a place to put notes about a court

Installation
============

Installing Courts-DB is easy.

    ::

        pip install courts_db


Or install the latest development version from GitHub.

    ::

        pip install git+https://github.com/freelawproject/courts-db.git@master



Future
=======

1. Continue to improve and expand the dataset.
2. Add filtering mechanisms by state, reporters, citation(s), judges, counties and cities.


Deployment
==========

If you wish to create a new version, the process is:

1. Update version info in ``setup.py`` and commit it.

2. Tag the commit with the version number.

To proceed manually
-------------------

1. Push your commit. CI (Continuous Integration) should take care of the rest.


To proceed manually
-------------------

1. Install the requirements in ``requirements_dev.txt``.

2. Set up a config file at ``~/.pypirc``.

3. Generate a universal distribution that works in Python 2 and Python 3 (see ``setup.cfg``).

    ::

        python setup.py sdist bdist_wheel

4. Upload the distributions.

    ::

        twine upload dist/* -r pypi # (or pypitest)


License
=======

This repository is available under the permissive BSD license, making it easy and safe to incorporate in your own libraries.

Pull and feature requests welcome. Online editing in GitHub is possible (and easy!)
