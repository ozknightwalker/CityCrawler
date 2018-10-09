from __future__ import unicode_literals

from .request import WebRequest, generate_url, decode_url

from bs4 import BeautifulSoup


class Geoname:
    cityURL = 'https://www.geonames.org/advanced-search.html'
    featureClass = 'P'

    def __init__(self, *args, **kwargs):
        self.cities = []
        self.base_url = kwargs.pop('url', '')
        self.countryCode = kwargs.pop('country_code', None)
        self.startRow = kwargs.pop('startRow', 0)
        if self.base_url != '':
            params = decode_url(self.base_url)
            if params['country']:
                self.countryCode = params['country'][0]
            if params['startRow']:
                self.startRow = params['startRow'][0]
        self.payload = kwargs.pop('payload', {})

    def url(self):
        if hasattr(self, 'base_url') and self.base_url != '':
            return self.base_url
        payload = dict(
            country=self.countryCode, startRow=self.startRow,
            featureClass=self.featureClass)
        payload.update(self.payload)
        self.base_url = generate_url(self.cityURL, payload)
        return self.base_url

    def request(self):
        if hasattr(self, 'response'):
            return self.response
        if self.countryCode is None:
            return
        url = self.url()
        self.response = WebRequest(url=url).request()
        return self.response

    def has_next(self):
        response = self.request()
        if not response:
            return False
        soup = BeautifulSoup(response.text, "html.parser")
        return bool(soup.findAll('a', text='next >'))

    def get_table(self):
        response = self.request()
        if response is None:
            return
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.select('div[id=search]')
        if container is None:
            return None

        table = soup.select('div[id=search] > table.restable')
        if len(table) < 1 or bool(container[0].findAll(
                text='no records found in geonames database, showing wikipedia results')):
            return None
        return table

    def crawl(self):
        table = self.get_table()

        if not table:
            return

        table_row = table[0].select('tr')
        row_size = len(table_row)

        for idx, row in enumerate(table_row):
            is_header = idx < 1 or idx >= (row_size - 1)
            if (is_header):
                continue

            data = self.generate_data(row)
            if data is None:
                continue
            self.cities.append(data)
        return self.cities

    def generate_data(self, row):
        table_data = row.select('td')
        if not table_data:
            return None
        name_column = table_data[1]
        name = name_column.find('a').text
        # name = table_data[1].text
        wiki = name_column.find(
            'img', {'alt': 'wikipedia article'})
        if wiki:
            wiki = dict(url=wiki.parent['href'])
        feature_class_column = table_data[3]
        state_column = table_data[2]
        state = state_column.find('small')
        if state:
            state = state.text \
                .split('>')[0] \
                .strip()
        population = feature_class_column.select('small')
        if population:
            population_text = population[0].text \
                .replace('population', '') \
                .replace(',', '') \
                .replace(' ', '') \
                .split('elevation')[0]
            if population_text == '':
                population_text = 0
            population = int(population_text)
        else:
            population = 0

        geo = name_column.find('span', {'class': 'geo'})
        if geo:
            lat = geo.find('span', {'class': 'latitude'})
            lng = geo.find('span', {'class': 'longitude'})
            geo = dict(lat=float(lat.text), lng=float(lng.text))

        data = dict(
            name=name, code=self.countryCode, wiki=wiki, population=population,
            geo=geo, state=state)
        data = self.validate(data, name_column)
        # uncomment this is you want your result to be either
        # have a population greater than 100,000 or `city` in the description
        # if not (
        #         data['validation']['population'] or
        #         data['validation']['description']):
        if not data['validation']['population']:
            return None
        return data

    def validate(self, data, name_column):
        abv = name_column.find('small')
        if abv is None:
            abv = False
        else:
            abv = abv.text.lower()
            abv = 'city' in abv
        validator = dict(
            population=data['population'] >= 100000,
            description=abv)
        data.update(dict(validation=validator))
        return data
