'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from rttbackend.defines import *

from .alphavantage import AlphaVantage


# Maps string name to class name for use with config
EXCHANGE_MAP = {
    ALPHAVANTAGE: AlphaVantage,
}
