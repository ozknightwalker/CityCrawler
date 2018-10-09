from __future__ import unicode_literals

from .request import WebRequest


class CountryCode:
    base_url = 'https://countrycode.org/api/countryCode/countryMenu'

    def __init__(self, *args, **kwargs):
        self.country_codes = []

    def get_all_country_codes(self):
        response = WebRequest(url=self.base_url).request()
        for country in response.json():
            self.country_codes.append(
                dict(name=country['name'].strip().title(),
                     code=country['code'].strip().upper()))
        return self.country_codes
