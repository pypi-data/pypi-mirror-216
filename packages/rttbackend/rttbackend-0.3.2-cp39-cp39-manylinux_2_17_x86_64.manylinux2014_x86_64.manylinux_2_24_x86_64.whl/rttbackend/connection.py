'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import logging

from typing import List, Union, AsyncIterable
from dataclasses import dataclass
import requests
import time
from yapic import json as json_parser
from decimal import Decimal

LOG = logging.getLogger('feedhandler')


class Connection:
    raw_data_callback = None

    async def read(self) -> bytes:
        raise NotImplementedError

    async def write(self, msg: str):
        raise NotImplementedError


class HTTPSync(Connection):
    def process_response(self, r, address, json=False, text=False, uuid=None):
        if self.raw_data_callback:
            self.raw_data_callback.sync_callback(
                r.text, time.time(), str(uuid), endpoint=address)
        r.raise_for_status()
        if json:

            try:
                return json_parser.loads(r.text, parse_float=Decimal)
            except json_parser.JSONDecodeError:
                return r.text

        if text:
            return r.text
        return r

    def read(self, address: str, params=None, headers=None, json=False, text=True, uuid=None):
        LOG.debug("HTTPSync: requesting data from %s", address)
        r = requests.get(address, headers=headers, params=params)
        return self.process_response(r, address, json=json, text=text, uuid=uuid)

    def write(self, address: str, data=None, json=False, text=True, uuid=None):
        LOG.debug("HTTPSync: post to %s", address)
        r = requests.post(address, data=data)
        return self.process_response(r, address, json=json, text=text, uuid=uuid)


@dataclass
class Routes:
    instruments: Union[str, list]
    currencies: str = None
    funding: str = None
    open_interest: str = None
    liquidations: str = None
    stats: str = None
    authentication: str = None
    l2book: str = None
    l3book: str = None


@dataclass
class RestEndpoint:
    address: str
    sandbox: str = None
    instrument_filter: str = None
    routes: Routes = None

    def route(self, ep, sandbox=False):
        endpoint = self.routes.__getattribute__(ep)
        api = self.sandbox if sandbox and self.sandbox else self.address
        return api + endpoint if isinstance(endpoint, str) else [api + e for e in endpoint]
