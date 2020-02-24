Courts-DB
=========

Courts-DB is an open source repository of all courts current and historical.
It was originally built for use in Courtlistener.com.


Quickstart
===========

Find court information by unicode string

::

        from courts_db import find_court_info

        mass_sjc = find_court_info(u"Massachusetts Supreme Judicial Court")

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

        mass_sjc = find_court(u"Massachusetts Supreme Judicial Court")

        returns: ["mass"]



Installation
============

Installing courts-db is easy.

    ::

        pip install courts_db


Or install the latest dev version from github

    ::

        pip install git+https://github.com/freelawproject/courts-db.git@master


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
