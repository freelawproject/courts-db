# -*- coding: utf-8 -*-
from unittest import TestCase
import unittest
import json
from string import Template, punctuation
from datetime import datetime as dt
import re
from glob import iglob
import pandas
import unicodedata

reg_punc = re.compile('[%s]' % re.escape(punctuation))
combined_whitespace = re.compile(r"\s+")
accents = re.compile('([^\w\s%s]+)' % re.escape(punctuation))
courts = re.compile('(^\s{4}?{)((.*\n){1,100}?)(\s{4}?},)')

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

    s = Template(json.dumps(court_data)).substitute(**variables)

    return s.replace("\\", "\\\\")

def clean_punct(court_str):
    clean_court_str = reg_punc.sub(' ', court_str)
    clean_court_str = combined_whitespace.sub(' ', clean_court_str).strip()
    ccs = u"%s" % clean_court_str.lower()
    return ccs


def get_court_list(fp):
    print fp
    court_set = set()
    df = pandas.read_csv(fp, usecols=['court'])
    cl = df['court'].tolist()
    cl = [x for x in cl if type(x) == str]
    court_list = set(cl)

    for court_str in court_list:
        try:
            clean_str = clean_punct(court_str)
            court_set.add(clean_str)
        except Exception as e:
            print court_str, str(e)

    return court_set


def gather_regexes(courts, bankruptcy=False):
    regexes = []
    for court in courts:
        if bankruptcy == False:
            if court["type"] == "bankruptcy":
                continue
        for reg_str in court['regex']:
            reg_str = reg_str.decode('unicode-escape')
            regex = re.compile(reg_str, (re.I | re.U))
            regexes.append((regex, court['id']))
    return regexes


def find_court_alt(court_str, filed_date=None, regexes=None, bankruptcy=False):
    """
    :param court_str:
    :param filed_date:
    :param regexes:
    :return:
    """
    cd = {}
    cdd = []
    court_matches = []
    assert type(court_str) == unicode, "text not unicode"
    for regex in regexes:
        if re.search(regex[0], court_str):
            court_matches.append(regex[1])

            cd[re.search(regex[0], court_str).group()] = regex[1]
            cdd.append(
                {"id": regex[1],
                 "text": re.search(regex[0], court_str).group()}
            )
            # print cdd

    results = list(set(court_matches))
    if len(results) > 1:
        flist = []
        remove_list = [x['text'] for x in cdd]
        subsetlist = []
        for test in remove_list:
            for item in [x for x in remove_list if x != test]:
                if test in item:
                    subsetlist.append(test)
        final_list = [x for x in remove_list if x not in subsetlist]
        # print final_list

        for r in cdd:
            if r['text'] in final_list:
                if bankruptcy == True:
                    pass
                else:
                    court_key = r['id']
                    if court_key != "" and court_key is not None:
                        if court_key[-1] != "b":
                            flist.append(r['id'])
                    else:
                        flist.append(r['text'])
        return flist

    return court_matches


def find_court(court_str, filed_date=None, courts_db=None):
    """

    :param court_str:
    :param filed_date:
    :param courts_db:
    :return:
    """
    cd = {}
    court_matches = []
    cdd = []

    if filed_date is None:
        for court in courts_db:
            for reg_str in court['regex']:
                reg_str = unicodedata.normalize('NFKD',
                              reg_str.decode('unicode-escape')).\
                                      encode('ascii', 'ignore')

                reg_str = re.sub(r'\s{2,}', ' ', reg_str)
                regex = re.compile(reg_str, re.I)
                if re.search(regex, court_str):
                    court_matches.append(court['id'])
                    cdd.append(
                        {"id":court['id'],
                        "text":re.search(regex, court_str).group()}
                   )
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
                        cd[court['id']] = re.search(regex, court_str)
                        continue

    results = list(set(court_matches))
    flist = []

    if len(results) > 1:
        print results
        remove_list = [x['text'] for x in cdd]
        subsetlist = []

        for test in remove_list:
            print remove_list
            for item in [x for x in remove_list if x != test]:
                if test in item:
                    subsetlist.append(test)
        final_list = [x for x in remove_list if x not in subsetlist]
        bankruptcy = False

        for r in cdd:
            if r['text'] in final_list:
                if bankruptcy == True:
                    pass
                else:
                    court_key = r['id']
                    if court_key is not None and court_key != "":
                        if court_key[-1] != "b":
                            flist.append(r['id'])

        return flist
    return results



class DataTests(TestCase):
    """
     python tests.py DataTests.test_court
     """


    def test_all_examples(self):
        s = load_template()
        courts = json.loads(s)
        regexes = gather_regexes(courts)

        for court in courts:
            try:
                for example in court['examples']:
                    matches = find_court_alt(
                        court_str=example,
                        regexes=regexes
                    )
                    results = list(set(matches))
                    if len(results) == 1:
                        if results == [court['id']]:
                            continue
                    else:
                        print results, [court["id"]], "\txx\t", example, "\n" #court['regex']
            except Exception as e:
                print (str(e))
                print "Fail at", court['name']



    def test_str(self):
        # """Can we extract the correct court id from string and date?"""

        bankruptcy = False
        s = load_template()
        courts = json.loads(s)

        court_id = "prapp"

        sample_text = u"Tribunal Circuito De Apelaciones"
        s_text = sample_text
        regexes = gather_regexes(courts)

        matches2 = find_court_alt(court_str=s_text,
                                  regexes=regexes
                                  )
        print matches2
        # self.assertEqual(list(set(matches2)), [court_id], "Failure %s" % matches2)

        print list(set(matches2)),
        print u"√"


    def test_one_example(self):
        """Can we extract the correct court id from string and date?"""

        bankruptcy = False
        s = load_template()
        courts = json.loads(s)
        court_id = "prapp"
        court = [x for x in courts if x['id'] == "prapp"][0]
        regexes = gather_regexes(courts)

        for example in court['examples']:
            print "Testing ... %s" % example.decode('unicode-escape'),
            example = example.decode('unicode-escape')
            matches2 = find_court_alt(court_str=example, regexes=regexes)
            self.assertEqual(list(set(matches2)), [court['id']], "Failure %s" % matches2)
            print u"√"



    def test_json(self):
        """
        A simple testing mechanism to show where the JSON problems exist.
        :return:
        """

        try:
            with open('data/courts.json', "r") as f:
                json.loads(f.read())
        except Exception as e:
            with open('data/courts.json', "r") as f:
                cd = f.read()

        regex = r"(^\s{4}?{)((.*\n){1,100}?)(\s{4}?},)"
        matches = re.finditer(regex, cd, re.MULTILINE)
        for match in enumerate(matches, start=1):
            court = match[1].group()[:-1]
            try:
                j = json.loads(court.strip())
            except:
                problem = court.strip()
                name = re.search('\"name\": \"(?P<name>.*)\"', problem).group('name')
                id = re.search('\"id\": \"(?P<id>.*)\"', problem).group('id')
                print id, "-", name



if __name__ == '__main__':
    unittest.main()