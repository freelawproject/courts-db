import re
from string import punctuation

reg_punc = re.compile(f"[{re.escape(punctuation)}]")
combined_whitespace = re.compile(r"\s{2,}")


def strip_punc(court_str: str) -> str:
    """Remove whitespace from court_str.
    :param: court_str: The court string
    :return: The court string without extra whitespace
    """
    return combined_whitespace.sub(" ", court_str).strip()
