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

        find_court_by_id(["mass"])

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
            "location": "Massachusetts"
        }]


::

        from courts_db import find_court

        mass_sjc = find_court_by_id(u"Massachusetts Supreme Judicial Court")

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
