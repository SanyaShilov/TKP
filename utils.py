import pytz

import dateutil.parser


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
