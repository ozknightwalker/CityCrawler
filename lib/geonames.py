from __future__ import unicode_literals

from .request import WebRequest

BASE_URL = 'https://countrycode.org'


class Geoname:
    country_url = f'{BASE_URL}/api/countryCode/countryMenu'

    def __init__(self, *args, **kwargs):
        self.country_codes = []

    def get_all_country_codes(self):
        response = WebRequest(url=self.country_url).request()
        for country in response.json():
            self.country_codes.append(
                dict(name=country['name'].strip().title(),
                     code=country['code'].strip().upper()))
