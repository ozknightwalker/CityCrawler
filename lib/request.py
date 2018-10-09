from __future__ import unicode_literals

import requests

from urllib.parse import urlencode, urlparse, parse_qs


class WebRequest:

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url', None)

    def request(self):
        if self.url is None:
            return
        msg = 'Requesting: {}'.format(self.url)
        print(msg)
        try:
            return requests.get(self.url)
        except Exception:
            print("Request for {} Failed".format(self.url))


def generate_url(base_url, payload={}):
    return '{}?{}'.format(base_url, urlencode(payload))


def decode_url(url):
    return parse_qs(urlparse(url).query)
