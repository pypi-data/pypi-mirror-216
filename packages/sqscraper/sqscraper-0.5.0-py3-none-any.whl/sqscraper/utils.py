"""
"""

import datetime
import decimal
import re


TODAY = datetime.datetime.today()
YTD = (TODAY - datetime.datetime(TODAY.year, 1, 1)).days


def expand_value(value: str) -> int:
    """
    :param value:
    :return:
    """
    powers = {"K": 3, "M": 6, "B": 9, "T": 12}
    regex = re.compile(r"^(-?\d+\.?\d*)([KMBT])$")

    quantity, magnitude = regex.search(value).groups()
    return int(decimal.Decimal(quantity) * 10 ** powers[magnitude])


def normalize_value(value: str) -> str:
    """
    :param value:
    :return:
    """
    regex = re.compile(r"^([-+]?)\$?([\d.,]+)%?$")
    try:
        return "".join(regex.sub(r"\1\2", value).split(","))
    except ValueError:
        return value
