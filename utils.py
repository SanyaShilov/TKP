import dateutil.parser
import pymorphy2
import re

import pytz


MORPH = pymorphy2.MorphAnalyzer()


def keyword_string(phrase: str):
    keyword_set = set()
    for keyword in re.findall(r"[\w']+", phrase.lower()):
        for parsed in MORPH.parse(keyword):
            keyword_set.add(parsed.normal_form)
    return ' '.join(sorted(keyword_set))


def parse_timestring(time_string, timezone='UTC'):
    """Parse timestring into naive UTC

    :param time_string: in ISO-8601 format
    :param timezone: if time_string contains no timezone, this argument is used
    :return: naive time in UTC
    """
    time = dateutil.parser.parse(time_string)
    if time.tzinfo is None:
        time = pytz.timezone(timezone).localize(time)
    utctime = time.astimezone(pytz.utc).replace(tzinfo=None)

    return utctime
