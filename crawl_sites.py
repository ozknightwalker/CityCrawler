from __future__ import unicode_literals

import os

from lib.geonames import Geoname
from lib.country_code import CountryCode
from lib.writer import dict_to_csv

import multiprocessing

items_to_crawl = set()


def populate_crawler(country_code, offset=0):
    payload = dict(q='city')
    geoname = Geoname(
        country_code=country_code['code'], startRow=offset, payload=payload)
    has_table = geoname.get_table() is not None
    if has_table:
        item = dict(url=geoname.url())
        dict_to_csv('results/url_to_crawl_with_q', item)
    if geoname.has_next():
        return populate_crawler(country_code, offset + 50)
    else:
        return None


if __name__ == "__main__":
    countryCode = CountryCode()
    countryCode.get_all_country_codes()
    if not os.path.isdir('results'):
        os.mkdir('results')
    pool = multiprocessing.Pool(8)
    pool.map(populate_crawler, countryCode.country_codes)
