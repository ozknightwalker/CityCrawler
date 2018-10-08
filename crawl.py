from __future__ import unicode_literals

from lib.geonames import Geoname


if __name__ == "__main__":
    geoname = Geoname()
    geoname.get_all_country_codes()
