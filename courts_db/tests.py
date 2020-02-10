# -*- coding: utf-8 -*-
from unittest import TestCase
import unittest
import json
from string import Template
from datetime import datetime as dt
import re
from glob import iglob


def load_template():
    """

    :return:
    """
    with open('data/courts.json', "r") as f:
        court_data = json.loads(f.read())

    with open('data/variables.json', "r") as v:
        variables = json.loads(v.read())

    for path in iglob("data/places/*.txt"):
        with open(path, "r") as p:
            places = "(%s)" % "|".join(p.read().splitlines())
            variables[path.split("/")[-1].split(".txt")[0]] = places

    s = Template(json.dumps(court_data["courts"])).substitute(**variables)
    return s.replace("\\", "\\\\")


def find_court(court_str, filed_date=None, courts_db=None):
    """

    :param court_str:
    :param filed_date:
    :param courts_db:
    :return:
    """
    court_matches = []
    if filed_date is None:
        for court in courts_db:
            for reg_str in court['regex']:
                reg_str = re.sub(r'\s{2,}', ' ', reg_str)
                regex = re.compile(reg_str, re.I)
                if re.search(regex, court_str):
                    court_matches.append(court['id'])
                    break
    else:
        filed_date = dt.strptime(filed_date, "%Y-%m-%d")
        court_matches = []
        for court in courts_db:
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

# normalize strings ... > ---
#

class ConstantsTest(TestCase):

    def test_ex(self):
        court_id = "paed"
        s = load_template()
        courts = json.loads(s)
        for court in courts:
            if court['id'] == court_id:
                break

        for example in court['examples']:
            matches = find_court(
                court_str=example,
                filed_date=None,
                courts_db=courts
            )
            results = list(set(matches))
            if len(results) == 1:
                if results[0] == court['id']:
                    print "Success for", court['name']
        return


    def test_all_ex(self):
        s = load_template()
        courts = json.loads(s)
        for court in courts:
            try:
                for example in court['examples']:
                    matches = find_court(
                        court_str=example,
                        filed_date=None,
                        courts_db=courts
                    )
                    results = list(set(matches))
                    # print results, court['id']
                    if len(results) == 1:
                        if results == [court['id']]:
                            # print results, [court['id']], "\t√\t", "Success for", court['name']
                            continue
                    else:
                        print results, [court["id"]], "\txx\t", example, "\n", court['regex']
            except Exception as e:
                print (str(e))
                print "Fail at", court['name']


    def test_str(self):
        # """Can we extract the correct court id from string and date?"""
        s = load_template()
        courts = json.loads(s)
        test = "UNITED STATES DISTRICT COURT EASTERN DISTRICT OF PENNA"
        matches = find_court(
            court_str=test,
            filed_date=None,
            courts_db=courts
        )
        print matches
        self.assertEqual(matches, ['vaed'])


    def test_west(self):
        with open("output.txt", "r") as f:
            rows = f.read().splitlines()
        rows = sorted(rows)[::-1]
        # rows = sorted(rows)
        s = load_template()
        courts = json.loads(s)
        count = 0
        for row in rows:
            count = count + 1
            row = re.sub(r'\W+', ' ', row)
            row = re.sub(r'\s{2,}', ' ', row)
            row = row.title()
            # print row
            matches = find_court(court_str=row, courts_db=courts)
            if len(matches) == 0:

                print count, matches, "\t\t\t", row


if __name__ == '__main__':
    unittest.main()