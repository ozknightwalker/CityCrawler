from __future__ import unicode_literals

from lib.geonames import Geoname
from lib.writer import read_csv, dict_to_csv

import multiprocessing

items_to_crawl = set()


def crawl_loop(url):
    geoname = Geoname(url=url['url'])
    results = geoname.crawl()
    if results is None:
        return
    for item in results:
        dict_to_csv('results/cities_without_q', item)


if __name__ == "__main__":
    fields = ('url',)
    urls = read_csv('results/url_to_crawl', fieldnames=fields)

    pool = multiprocessing.Pool(8)
    pool.map(crawl_loop, urls)
