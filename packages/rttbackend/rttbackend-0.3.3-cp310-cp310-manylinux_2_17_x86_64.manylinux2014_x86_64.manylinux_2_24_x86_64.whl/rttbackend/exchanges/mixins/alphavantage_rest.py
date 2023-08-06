'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import asyncio
from decimal import Decimal
import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode


from yapic import json

from rttbackend.defines import GET, POST
from rttbackend.exchange import RestExchange

LOG = logging.getLogger('feedhandler')


class AlphaVantageRestMixin(RestExchange):
    api = "https://www.alphavantage.co/"

    def _request(self, method: str, endpoint: str, auth: bool = False, payload={}, api=None):
        query_string = urlencode(payload)

        if auth:
            if query_string:
                query_string = '{}&apikey={}'.format(query_string, self.key_id)
            else:
                query_string = 'apikey={}'.format(self.key_id)

        if not api:
            api = self.api

        url = f'{api}{endpoint}?{query_string}'

        if method == GET:
            return self.http_sync.read(address=url)
        elif method == POST:
            return self.http_sync.write(address=url, data=None)

    def refresh_symbol_lookup(self, symbol: str):
        return self._request(GET, 'query', auth=True, payload={'function': 'SYMBOL_SEARCH', 'keywords': symbol})
