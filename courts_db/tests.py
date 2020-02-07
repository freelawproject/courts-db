from unittest import TestCase
import unittest
import json
from string import Template
from datetime import datetime as dt
import re


def load_template():
    with open('data/courts.json', "r") as f:
        court_data = json.loads(f.read())
    s = Template(json.dumps(court_data["courts"])).substitute(
        **court_data['variables']).replace("\\", "\\\\")
    return s


def find_court_by_date(court_str, filed_date):
    s = load_template()
    courts = json.loads(s)
    filed_date = dt.strptime(filed_date, "%Y-%m-%d")
    court_matches = []
    for court in courts:
        for date in court['dates']:
            if date['start'] is None:
                continue
            date_start = dt.strptime(date['start'], "%Y-%m-%d")

            if date['end'] is None:
                date_end = dt.today()
            else:
                date_end = dt.strptime(date['end'], "%Y-%m-%d")

            if not date_start <= filed_date <= date_end:
                continue
            if court['id'] is None:
                continue

            for reg_str in court['regex']:
                regex = re.compile(reg_str, re.I)
                if re.search(regex, court_str):
                    court_matches.append(court['id'])
                    continue
    return court_matches


class ConstantsTest(TestCase):
    def test_extract_court(self):
        """Can we extract the correct court id from string and date?"""
        test = "Alabama Supreme Court"
        matches = find_court_by_date(court_str=test, filed_date="1840-01-01")
        print matches
        self.assertEqual(matches, ['ala'])


if __name__ == '__main__':
    unittest.main()