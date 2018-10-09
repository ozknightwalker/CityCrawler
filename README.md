## Geonames City Crawler
crawls all cities found in the geonames.org


### Installation

create a virtualenv for this project
```commandline
virtualenv venv
# then activate the environment
source venv/bin/activate
```

install python packages
```commandline
pip install -r requirements.txt
```


Scrape all possible urls to be scraped in geonames.org for city listing
```
python crawl_sites.py
```
this script will generate a csv of all the urls that have a resulting table
that might be useful to us.

now we can iterate and visit those urls and start scraping data
```
python crawl.py
```
this script will iterate all item in the search table and only record item
whose population is greater than or equal to 100,000.

the results are aggregated in a csv file with
columns:
'name', 'country_code', 'wiki', 'population', 'geo', 'state_name', 'validator'
 - name -- the name of the possible city
 - country_code -- country code of the record
 - wiki -- wiki url of the possible city
 - population -- the population of the instance
 - geo -- geolocation of the instance (latitude and longitude)
 - state_name -- the possible name of the state where this city is located
 - validator -- a dict of validation (population, via description)