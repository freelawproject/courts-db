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
local_path = "/Users/Palin/Code/courtlistener/cl/assets/media/opinion_metadata/lexis/%s.csv"


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

                # print reg_str
                # reg_str = remove_accents(reg_str)
                # print reg_str
                # reg_str = unicodedata.normalize('NFKD',
                #               reg_str.decode('unicode-escape')).\
                #                       encode('ascii', 'ignore')

                reg_str = re.sub(r'\s{2,}', ' ', reg_str)
                regex = re.compile(reg_str, re.I)
                if re.search(regex, court_str):
                    court_matches.append(court['id'])
                    cdd.append(
                        {"id":court['id'],
                        "text":re.search(regex, court_str).group()}
                   )
                    # cd[re.search(regex, court_str).group()] = court['id']
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
    # print results
    if len(results) > 1:
        # print results
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
    # print cdd
    return results

def find_court_alt(court_str, filed_date=None, courts_db=None, regexes=None, bankruptcy=False):
    """

    :param court_str:
    :param filed_date:
    :param courts_db:
    :param regexes:
    :return:
    """
    cd = {}
    cdd = []
    court_matches = []
    for regex in regexes:
        if re.search(regex[0], court_str):
            court_matches.append(regex[1])
            cd[re.search(regex[0], court_str).group()] = regex[1]
            cdd.append(
                {"id": regex[1],
                 "text": re.search(regex[0], court_str).group()}
            )

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
        for r in cdd:
            if r['text'] in final_list:
                if bankruptcy == True:
                    pass
                else:
                    court_key = r['id']
                    if court_key != "" and court_key is not None:
                        if court_key[-1] != "b":
                            flist.append(r['id'])
        return flist

    return court_matches



class ConstantsTest(TestCase):
    """ """
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

        print matches, "==", ['paed']
        # self.assertEqual(matches, ['mnd'])


    def test_west(self):
        with open("output.txt", "r") as f:
            rows = f.read().splitlines()
        # rows = sorted(rows)[::-1]
        rows = sorted(rows)
        s = load_template()
        courts = json.loads(s)
        count = 0
        for row in rows:

            # row = re.sub(r'\W+', ' ', row)
            row = re.sub(re.compile('[%s]' % re.escape(punctuation)), ' ', row)

            row = re.sub(r'\s{2,}', ' ', row).strip()
            row = row.title()
            # print row
            matches = find_court(court_str=row, courts_db=courts)
            if len(matches) == 0:
                count = count + 1
                print count, matches, "\t\t\t", row


    def test_fast(self):
        with open("output.txt", "r") as f:
            rows = f.read().splitlines()
        # rows = sorted(rows)[::-1]
        rows = sorted(rows)
        s = load_template()
        courts = json.loads(s)
        count = 0
        regexes = []
        for court in courts:
            for reg_str in court['regex']:
                reg_str = re.sub(r'\s{2,}', ' ', reg_str)
                regex = re.compile(reg_str, re.I)
                regexes.append((regex, court['id']))

        for row in rows:
            row = re.sub(r'\W+', ' ', row)
            row = re.sub(r'\s{2,}', ' ', row).strip()
            row = row.title().strip()


            matches = find_court_alt(court_str=row,
                                     courts_db=courts,
                                     regexes=regexes)
            if len(matches) != 1:
                count = count + 1
                print count, matches, "\t\t\t", row#, orig


    def test_fast_examples(self):
        s = load_template()
        courts = json.loads(s)
        examples = []
        for court in courts:
            for example in court['examples']:
                examples.append((example, court["id"], court['regex']))

        count = 0
        # regexes = []
        # for court in courts:
        #     for reg_str in court['regex']:
        #         reg_str = re.sub(r'\s{2,}', ' ', reg_str)
        #         regex = re.compile(reg_str, re.I)
        #         regexes.append((regex, court['id']))

        for example_triple in examples:
            courtid = example_triple[1]
            if courtid is None:
                courtid = ""
            regexes = [(courtid, example_triple[2])]
            ex_str = example_triple[0]

            ex_str = re.sub(r'\W+', ' ', ex_str)
            ex_str = re.sub(r'\s{2,}', ' ', ex_str)
            ex_str = ex_str.title().strip()

            if len(example_triple[2]) > 0:
                matches = find_court_alt(court_str=ex_str, courts_db=courts, regexes=regexes)
                if len(matches) != 1:
                    count = count + 1
                    print count, matches, "\t\t\t", ex_str, courtid


    def test_main(self):
        import pandas
        count = 0
        court_set = set()
        reporter = "*"
        volume = "*"

        s = load_template()
        courts = json.loads(s)
        regexes = []
        for court in courts:
            for reg_str in court['regex']:
                reg_str = re.sub(r'\s{2,}', ' ', reg_str)
                regex = re.compile(reg_str, re.I)
                regexes.append((regex, court['id']))

        gpath = "/Users/Palin/Code/courtlistener/cl/assets/media/opinion_metadata/%s/%s_vol_%s.csv" % (reporter, reporter, volume)
        for file_path in iglob(gpath):
            current_reporter = file_path.split("opinion_metadata/")[1].split("/")[0]
            if reporter != current_reporter:
                reporter = current_reporter
                # print reporter

            if "lexis" not in file_path and "bankruptcy" not in file_path:
                cd = {}
                df = pandas.read_csv(file_path,
                                     usecols=['Court Line'],
                                     )

                cl = df['Court Line'].tolist()
                cl = [x for x in cl if type(x) == str]
                courts = set(cl)

                for court_str in courts:
                    try:
                        clean_court_str = re.sub("[%s]" % re.escape(punctuation), ' ', court_str)
                        clean_court_str = re.sub(r'\s{2,}', ' ', clean_court_str)
                        clean_court_str = clean_court_str.title().strip()
                        court_set.add(clean_court_str)
                    except Exception as e:
                        print court_str, str(e)

        output = []
        for court_strings in court_set:

            matches = find_court_alt(court_str=court_strings,
                                     courts_db=courts,
                                     regexes=regexes)
            # if len(matches) > 0:
            for match in matches:
                if match is not None and match != "":
                    if match[-1] == "b":
                        matches.remove(match)

            if len(list(set(matches))) != 1:
                count = count + 1
                print count, matches, "\t\t\t", court_strings
                output.append(court_strings)

        # print "\n\n\n"
        # for x in sorted(output):
        #     print x
        #
        with open('new_output.txt', 'w') as f:
            for item in sorted(output):
                f.write("%s\n" % item)


    def test_lexis(self):
        count = 0
        reporter = "lexis"
        volume = "*"

        s = load_template()
        courts = json.loads(s)
        regexes = []
        output = []
        duplicates = []

        for court in courts:
            for reg_str in court['regex']:
                if re.search(accents, reg_str):
                    reg_str = unicodedata.normalize('NFKD',
                                  reg_str.decode('unicode-escape')).\
                                          encode('ascii', 'ignore')

                reg_str = re.sub(r'\s{2,}', ' ', reg_str)
                regex = re.compile(reg_str, re.I)
                regexes.append((regex, court['id']))

        for file_path in iglob(local_path % volume):
            if "bankruptcy" in file_path:
                continue

            court_set = get_court_list(fp=file_path)
            for court_string in court_set:
                if re.search(accents, court_string):
                    court_string = remove_accents(court_string)

                matches = find_court_alt(court_str=court_string,
                                         courts_db=courts,
                                         regexes=regexes)

                for match in matches:
                    if match is not None and match != "":
                        if match[-1] == "b":
                            matches.remove(match)

                if len(list(set(matches))) < 1:
                    count = count + 1
                    # print count, matches, "\t\t\t", court_strings
                    output.append(court_string)
                elif len(list(set(matches))) > 1:
                    duplicates.append(court_string)

        joined_list = sorted(output) + \
                      ["\n--- NOW DUPLICATES --- \n"] + \
                      sorted(duplicates)

        with open('lexis_output.txt', 'w') as f:
            for item in joined_list:
                f.write("%s\n" % item)


    def test_regex(self):
        court_str = "Trib  unal   Circuito,,, De Ápelációnes De Puerto Rico"
        reg_punc = re.compile('[%s]' % re.escape(punctuation))
        combined_whitespace = re.compile(r"\s+")
        clean_court_str = reg_punc.sub(' ', court_str)
        clean_court_str = combined_whitespace.sub(' ', clean_court_str)
        print clean_court_str


if __name__ == '__main__':
    unittest.main()