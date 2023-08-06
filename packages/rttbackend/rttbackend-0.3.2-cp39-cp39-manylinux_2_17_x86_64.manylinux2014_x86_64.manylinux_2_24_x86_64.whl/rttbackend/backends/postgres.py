
import asyncpg
from typing import Tuple
from rttbackend.defines import POSTGRES, REFRESH_SYMBOL, TABLE, EXCHANGE, BASE_SYMBOL, QUOTE_SYMBOL, SYMBOL, RAW
from datetime import datetime as dt
from rttbackend.config import Config
import json

class CredsPostgres():
    def __init__(self):
        pass


class TargetPostgres(CredsPostgres):
    id = POSTGRES
    def __init__(self, config=None):
        if config is None:
            config = 'config.yaml'
        
        self.config = Config(config=config)
        keys = self.config[self.id.lower()] 
        self.host = keys.host
        self.user = keys.user
        self.pw = keys.pw
        self.db = keys.db
        self.port = keys.port
        


class Postgres():
    def __init__(self, conn: CredsPostgres):
        self.table = self.default_table
        self.raw_table = TABLE + RAW

        self.host = conn.host
        self.user = conn.user
        self.pw = conn.pw
        self.db = conn.db
        self.port = conn.port


    def _raw(self, data: Tuple):
        timestamp, data = data
        return f"('{timestamp}','{json.dumps(data)}')"
    
    async def _connect(self):
        self.conn = await asyncpg.connect(user=self.user, password=self.pw, database=self.db, host=self.host, port=self.port)

    async def read(self):
        await self._connect()
        args_str = self._read()
        async with self.conn.transaction():
            try:
                return await self.conn.fetch(f"SELECT {args_str} FROM {self.table}")
            except Exception as a:
                print(a)
                  # when restarting a subscription, some exchanges will re-publish a few messages
                pass
     
    async def write(self, updates: list):
        await self._connect()

        batch = []

        for data in updates:
            data = data.to_dict()
            ts = dt.utcfromtimestamp(
                data['timestamp']) if data['timestamp'] else None
            batch.append((ts, data))
        
        args_str = ','.join([self._write(u) for u in batch])
        args_raw_str = ','.join([self._raw(u) for u in batch])

        async with self.conn.transaction():
            try:
                await self.conn.execute(f"INSERT INTO {self.table} VALUES {args_str} ON CONFLICT DO NOTHING")
                await self.conn.execute(f"INSERT INTO {self.raw_table} VALUES {args_raw_str}")
            except Exception as a:
                print(a)
                # when restarting a subscription, some exchanges will re-publish a few messages
                pass


class RefreshSymbolPostgres(Postgres):
    default_table = TABLE + REFRESH_SYMBOL

    def _read(self):
        return f"timestamp,exchange,symbol,base_symbol,quote_symbol"

    def _write(self, data: Tuple):

        timestamp, data = data
        return f"('{timestamp}','{data['exchange']}','{data['symbol']}','{data['base_symbol']}','{data['quote_symbol']}')"


class ExchangePostgres(Postgres):
    default_table = TABLE + EXCHANGE

    def _read(self):
        return f"id,exchange"

    def _write(self, data: Tuple):
        timestamp, data = data
        return f"(DEFAULT,'{data['exchange']}','{timestamp}')"
    


class BaseSymbolPostgres(Postgres):
    default_table = TABLE + BASE_SYMBOL

    def _read(self):
        return f"id,base_symbol"

    def _write(self, data: Tuple):
        timestamp, data = data
        return f"(DEFAULT,'{data['base_symbol']}','{timestamp}')"
    

class QuoteSymbolPostgres(Postgres):
    default_table = TABLE + QUOTE_SYMBOL

    def _read(self):
        return f"id,quote_symbol"

    def _write(self, data: Tuple):
        timestamp, data = data
        return f"(DEFAULT,'{data['quote_symbol']}','{timestamp}')"
    
class SymbolPostgres(Postgres):
    default_table = TABLE + SYMBOL

    def _read(self):
        return NotImplemented

    def _write(self, data: Tuple):
        timestamp, data = data
        return f"(DEFAULT, '{data['exchange_id']}', '{data['base_symbol_id']}', '{data['quote_symbol_id']}', '{data['symbol']}', '{timestamp}')"
    
