'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''

from rttbackend.defines import ALPHAVANTAGE, REFRESH_SYMBOL, EXCHANGE
from rttbackend.exchange import Exchange
from rttbackend.connection import RestEndpoint, Routes
from rttbackend.symbols import Symbol
from rttbackend.types import RefreshSymbols


from typing import Dict, List, Tuple, Union
from decimal import Decimal
import csv
from time import time
from yapic import json

from prefect import flow, task


class AlphaVantage(Exchange):
    id = ALPHAVANTAGE
    rest_endpoints = [RestEndpoint(
        'https://www.alphavantage.co/', routes=Routes(['query?function=LISTING_STATUS']))]
    key_seperator = ','

    rest_channels = {
        REFRESH_SYMBOL: REFRESH_SYMBOL
    }

    @classmethod
    def _parse_symbol_data(cls, data: dict) -> Tuple[Dict, Dict]:

        ret = {}

        for i in csv.reader(data.splitlines(), delimiter=','):
            type = i[3]
            if type == 'Stock':
                symbol = i[0]

                symbol = symbol.replace('-', '/')

                s = Symbol(symbol, 'USD')
                ret[s.normalized] = str(symbol)

        return ret

    @classmethod
    def _symbol_endpoint_prepare(cls, ep: RestEndpoint, key_id) -> Union[List[str], str]:
        """
        override if a specific exchange needs to do something first, like query an API
        to get a list of currencies, that are then used to build the list of symbol endpoints
        """
        return [ep + '&apikey=' + key_id for ep in ep.route('instruments')]

    def refresh_symbol(self):
        data = []
        for j in self.symbols():
            base, quote = j.split('-')
            data.append({'base': base, 'quote': quote, 'symbol': j})

        return json.dumps(data)

    def _refresh_symbol(self, msg, ts):
        data = []
        for j in msg:
            data.append(RefreshSymbols(
                self.id, j['symbol'], j['base'], j['quote'], ts, raw=j))
        return data

    def message_handler(self, type, msg: str):

        msg = json.loads(msg, parse_float=Decimal)

        if type == REFRESH_SYMBOL:
            return self._refresh_symbol(msg, time())

