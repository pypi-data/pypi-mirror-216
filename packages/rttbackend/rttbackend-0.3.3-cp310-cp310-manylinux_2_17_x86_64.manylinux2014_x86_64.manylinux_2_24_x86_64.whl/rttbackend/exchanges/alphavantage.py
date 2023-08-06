'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''

from rttbackend.defines import ALPHAVANTAGE, REFRESH_SYMBOL, REFRESH_SYMBOL_LOOKUP
from rttbackend.exchange import Exchange
from rttbackend.connection import RestEndpoint, Routes
from rttbackend.symbols import Symbol
from rttbackend.exchanges.mixins.alphavantage_rest import AlphaVantageRestMixin
from rttbackend.exceptions import UnsupportedSymbol
from rttbackend.types import RefreshSymbols, RefreshSymbolLookup


from typing import Dict, List, Tuple, Union
from decimal import Decimal
import csv
from time import time
from yapic import json

from prefect import flow, task


class AlphaVantage(Exchange, AlphaVantageRestMixin):
    id = ALPHAVANTAGE
    rest_endpoints = [RestEndpoint(
        'https://www.alphavantage.co/', routes=Routes(['query?function=LISTING_STATUS']))]
    key_seperator = ','

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

    def _refresh_symbol_lookup(self, msg, ts):
        data = []
        for i in msg['bestMatches']:
            try:
                base, quote = self.exchange_symbol_to_std_symbol(
                    i['1. symbol']).split('-')
                # name = i['2. name']
                data.append(RefreshSymbolLookup(
                    exchange=self.id,
                    base_symbol=base,
                    quote_symbol=quote,
                    name=i['2. name'],
                    type=i['3. type'],
                    region=i['4. region'],
                    market_open=i['5. marketOpen'],
                    market_close=i['6. marketClose'],
                    time_zone=i['7. timezone'],
                    timestamp=ts,
                    raw=i
                ))

            except UnsupportedSymbol:
                pass

        return data

    def message_handler(self, type, msg: str):

        msg = json.loads(msg, parse_float=Decimal)

        if type == REFRESH_SYMBOL:
            return self._refresh_symbol(msg, time())
        elif type == REFRESH_SYMBOL_LOOKUP:
            return self._refresh_symbol_lookup(msg, time())
