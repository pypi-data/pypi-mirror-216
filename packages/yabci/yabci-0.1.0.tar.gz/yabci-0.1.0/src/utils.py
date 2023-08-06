import importlib.util
# import sys
from hashlib import sha1
import datetime
import dateutil
import benedict
from beancount.core.number import D
from beancount.core import amount
import os
from .logger import logger


def load_config(path):

    # see https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    module_name = "config"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    # sys.modules[module_name] = module
    spec.loader.exec_module(module)
    # print(module.__dict__)
    # print(module.__dict__.get("account"))
    # exit()
    return module.__dict__


def critical_error(*args):
    logger.critical(*args)
    exit(1)


def map_dict(value, data: dict):
    """
    >>> map_dict({'bc-payee': 'payee', 'date': ['payee', 'date', lambda test: 'bar', {'meh': 'payee'}]}, {'payee': 'foo-payee', 'date': 'foo-date'})
    {'bc-payee': 'foo-payee', 'date': ['foo-payee', 'foo-date', 'bar', {'meh': 'foo-payee'}]}
    """
    ret = {}

    if callable(value):
        return value(benedict.benedict(data))

    if isinstance(value, bytes):
        return value.decode()

    if isinstance(value, str):
        return benedict.benedict(data).get(value)

    if isinstance(value, set):
        return {map_dict(x, data) for x in value}

    if isinstance(value, list):
        return [map_dict(x, data) for x in value]

    if isinstance(value, dict):
        return {k: map_dict(v, data) for k, v in value.items()}

    return value


def hash_str(s: str):
    """
    >>> hash_str("foo")
    '0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33'
    """
    # https://death.andgravity.com/stable-hashing
    hash_value = sha1(s.encode("utf-8")).hexdigest()
    return hash_value


def parse_date(thing) -> datetime.date:
    """
    Turn a random variable into a date

    - date: return unchanged
    - datetime -> datetime's date
    - string: gets parsed via dateutil

    >>> parse_date(datetime.date(2023,2,3))
    datetime.date(2023, 2, 3)
    >>> parse_date(datetime.datetime(2023,1,1,12,34,56))
    datetime.date(2023, 1, 1)
    >>> parse_date("2017-11-05T00:06:18")
    datetime.date(2017, 11, 5)
    """

    try:
        if isinstance(thing, datetime.datetime):
            return thing.date()

        if isinstance(thing, datetime.date):
            return thing

        return dateutil.parser.parse(thing).date()
    except Exception as e:
        raise type(e)("parse_date: %s" % str(e))


def parse_amount(thing, default_currency="EUR") -> amount.Amount:
    """
    Create a beancount amount object from any values

    >>> parse_amount([120, "USD"])
    120 USD
    >>> parse_amount("120")
    120 EUR
    >>> parse_amount(120)
    120 EUR
    >>> parse_amount("120", "GBP")
    120 GBP
    """
    try:
        if thing is None:
            return None

        if isinstance(thing, amount.Amount):
            return thing

        if isinstance(thing, list):
            return amount.Amount(D(thing[0]), thing[1])

        return amount.Amount(D(thing), default_currency)
    except Exception as e:
        raise type(e)("parse_amount: %s" % str(e))


def path_to_dict(path):

    def subpath_to_dict(subpath, d={}):

        name = os.path.basename(subpath)

        if os.path.isdir(subpath):
            if name not in d:
                d[name] = {'_': []}
            for x in os.listdir(subpath):
                subpath_to_dict(os.path.join(subpath,x), d[name])
        else:
            d['_'].append(benedict.benedict(subpath))
        return d

    return list(subpath_to_dict(path).values())[0]


def read_json_files_in_folder(filename):
    download_folder = os.path.join(os.path.dirname(filename), benedict.benedict(filename).get("folder"))
    return path_to_dict(download_folder)


def read_json_from_zip(filename, pattern: None):
    """
    Traverses a zip archive, parse the first *.json file and return its parsed
    content
    """
    import zipfile
    import json
    import re
    with zipfile.ZipFile(filename, "r") as z:
        for filename in z.namelist():
            if pattern and re.match(pattern, filename):
                with z.open(filename) as f:
                    return json.loads(f.read())
