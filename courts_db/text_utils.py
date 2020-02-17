import re
from string import punctuation

reg_punc = re.compile("[%s]" % re.escape(punctuation))
combined_whitespace = re.compile(r"\s+")


def strip_punc(court_str):
    clean_court_str = reg_punc.sub(" ", court_str)
    clean_court_str = combined_whitespace.sub(" ", clean_court_str).strip()
    ccs = "%s" % clean_court_str.title()

    return ccs
