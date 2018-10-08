from __future__ import unicode_literals

import logging
import requests

logger = logging.getLogger(__name__)


class WebRequest:

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url', None)

    def request(self):
        if self.url is None:
            return
        logger.info('Requesting: {}'.format(self.url))
        try:
            return requests.get(self.url)
        except Exception:
            logger.exception("Request for {} Failed".format(self.url))
