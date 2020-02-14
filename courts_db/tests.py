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
    ccs = clean_court_str.title()

    return ccs


def remove_accents(text):
    if re.search(accents, text):
        text = unicode(text, 'utf-8')
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
    return text


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
                        cd[court['id']] = re.search(regex, court_str)
                        continue

    results = list(set(court_matches))
    flist = []
    if len(results) > 1:
        remove_list = [x['text'] for x in cdd]
        subsetlist = []

        for test in remove_list:
            # print remove_list
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



class ConstantsTest(TestCase):
    """ """


    def test_all_examples(self):
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

        s = load_template()
        courts = json.loads(s)

        text = "United States District Court For The District Of Canal Zone"
        if re.search(accents, text):
            text = remove_accents(text)

        matches = find_court(
            court_str=text,
            filed_date=None,
            courts_db=courts
        )


if __name__ == '__main__':
    unittest.main()