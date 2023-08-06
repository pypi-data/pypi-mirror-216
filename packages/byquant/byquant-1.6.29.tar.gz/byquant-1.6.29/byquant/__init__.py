# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2018 Uakeey

# ----------------------------------------------------------------------------

__version__ = '3.0.103'

# ----------------------------------------------------------------------------

from ccxt.base.exchange import Exchange                     # noqa: F401
from ccxt.base.precise import Precise                       # noqa: F401

from ccxt.base.decimal_to_precision import decimal_to_precision  # noqa: F401
from ccxt.base.decimal_to_precision import TRUNCATE              # noqa: F401
from ccxt.base.decimal_to_precision import ROUND                 # noqa: F401
from ccxt.base.decimal_to_precision import ROUND_UP              # noqa: F401
from ccxt.base.decimal_to_precision import ROUND_DOWN            # noqa: F401
from ccxt.base.decimal_to_precision import DECIMAL_PLACES        # noqa: F401
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS    # noqa: F401
from ccxt.base.decimal_to_precision import TICK_SIZE             # noqa: F401
from ccxt.base.decimal_to_precision import NO_PADDING            # noqa: F401
from ccxt.base.decimal_to_precision import PAD_WITH_ZERO         # noqa: F401

from ccxt.base import errors
from ccxt.base.errors import BaseError                                # noqa: F401
from ccxt.base.errors import ExchangeError                            # noqa: F401
from ccxt.base.errors import AuthenticationError                      # noqa: F401
from ccxt.base.errors import PermissionDenied                         # noqa: F401
from ccxt.base.errors import AccountNotEnabled                        # noqa: F401
from ccxt.base.errors import AccountSuspended                         # noqa: F401
from ccxt.base.errors import ArgumentsRequired                        # noqa: F401
from ccxt.base.errors import BadRequest                               # noqa: F401
from ccxt.base.errors import BadSymbol                                # noqa: F401
from ccxt.base.errors import MarginModeAlreadySet                     # noqa: F401
from ccxt.base.errors import BadResponse                              # noqa: F401
from ccxt.base.errors import NullResponse                             # noqa: F401
from ccxt.base.errors import InsufficientFunds                        # noqa: F401
from ccxt.base.errors import InvalidAddress                           # noqa: F401
from ccxt.base.errors import AddressPending                           # noqa: F401
from ccxt.base.errors import InvalidOrder                             # noqa: F401
from ccxt.base.errors import OrderNotFound                            # noqa: F401
from ccxt.base.errors import OrderNotCached                           # noqa: F401
from ccxt.base.errors import CancelPending                            # noqa: F401
from ccxt.base.errors import OrderImmediatelyFillable                 # noqa: F401
from ccxt.base.errors import OrderNotFillable                         # noqa: F401
from ccxt.base.errors import DuplicateOrderId                         # noqa: F401
from ccxt.base.errors import NotSupported                             # noqa: F401
from ccxt.base.errors import NetworkError                             # noqa: F401
from ccxt.base.errors import DDoSProtection                           # noqa: F401
from ccxt.base.errors import RateLimitExceeded                        # noqa: F401
from ccxt.base.errors import ExchangeNotAvailable                     # noqa: F401
from ccxt.base.errors import OnMaintenance                            # noqa: F401
from ccxt.base.errors import InvalidNonce                             # noqa: F401
from ccxt.base.errors import RequestTimeout                           # noqa: F401
from ccxt.base.errors import error_hierarchy                          # noqa: F401


from byquant.exchange.ace import ace                                              # noqa: F401
from byquant.exchange.alpaca import alpaca                                        # noqa: F401
from byquant.exchange.ascendex import ascendex                                    # noqa: F401
from byquant.exchange.bequant import bequant                                      # noqa: F401
from byquant.exchange.bigone import bigone                                        # noqa: F401
from byquant.exchange.binance import binance                                      # noqa: F401
from byquant.exchange.binancecoinm import binancecoinm                            # noqa: F401
from byquant.exchange.binanceus import binanceus                                  # noqa: F401
from byquant.exchange.binanceusdm import binanceusdm                              # noqa: F401
from byquant.exchange.bit2c import bit2c                                          # noqa: F401
from byquant.exchange.bitbank import bitbank                                      # noqa: F401
from byquant.exchange.bitbay import bitbay                                        # noqa: F401
from byquant.exchange.bitbns import bitbns                                        # noqa: F401
from byquant.exchange.bitcoincom import bitcoincom                                # noqa: F401
from byquant.exchange.bitfinex import bitfinex                                    # noqa: F401
from byquant.exchange.bitfinex2 import bitfinex2                                  # noqa: F401
from byquant.exchange.bitflyer import bitflyer                                    # noqa: F401
from byquant.exchange.bitforex import bitforex                                    # noqa: F401
from byquant.exchange.bitget import bitget                                        # noqa: F401
from byquant.exchange.bithumb import bithumb                                      # noqa: F401
from byquant.exchange.bitmart import bitmart                                      # noqa: F401
from byquant.exchange.bitmex import bitmex                                        # noqa: F401
from byquant.exchange.bitopro import bitopro                                      # noqa: F401
from byquant.exchange.bitpanda import bitpanda                                    # noqa: F401
from byquant.exchange.bitrue import bitrue                                        # noqa: F401
from byquant.exchange.bitso import bitso                                          # noqa: F401
from byquant.exchange.bitstamp import bitstamp                                    # noqa: F401
from byquant.exchange.bitstamp1 import bitstamp1                                  # noqa: F401
from byquant.exchange.bittrex import bittrex                                      # noqa: F401
from byquant.exchange.bitvavo import bitvavo                                      # noqa: F401
from byquant.exchange.bkex import bkex                                            # noqa: F401
from byquant.exchange.bl3p import bl3p                                            # noqa: F401
from byquant.exchange.blockchaincom import blockchaincom                          # noqa: F401
from byquant.exchange.btcalpha import btcalpha                                    # noqa: F401
from byquant.exchange.btcbox import btcbox                                        # noqa: F401
#from byquant.exchange.btcex import btcex                                          # noqa: F401
from byquant.exchange.btcmarkets import btcmarkets                                # noqa: F401
from byquant.exchange.btctradeua import btctradeua                                # noqa: F401
from byquant.exchange.btcturk import btcturk                                      # noqa: F401
from byquant.exchange.bybit import bybit                                          # noqa: F401
from byquant.exchange.cex import cex                                              # noqa: F401
from byquant.exchange.coinbase import coinbase                                    # noqa: F401
from byquant.exchange.coinbaseprime import coinbaseprime                          # noqa: F401
from byquant.exchange.coinbasepro import coinbasepro                              # noqa: F401
from byquant.exchange.coincheck import coincheck                                  # noqa: F401
from byquant.exchange.coinex import coinex                                        # noqa: F401
from byquant.exchange.coinfalcon import coinfalcon                                # noqa: F401
from byquant.exchange.coinmate import coinmate                                    # noqa: F401
from byquant.exchange.coinone import coinone                                      # noqa: F401
from byquant.exchange.coinsph import coinsph                                      # noqa: F401
from byquant.exchange.coinspot import coinspot                                    # noqa: F401
from byquant.exchange.cryptocom import cryptocom                                  # noqa: F401
from byquant.exchange.currencycom import currencycom                              # noqa: F401
from byquant.exchange.delta import delta                                          # noqa: F401
from byquant.exchange.deribit import deribit                                      # noqa: F401
from byquant.exchange.digifinex import digifinex                                  # noqa: F401
from byquant.exchange.exmo import exmo                                            # noqa: F401
from byquant.exchange.fmfwio import fmfwio                                        # noqa: F401
from byquant.exchange.gate import gate                                            # noqa: F401
from byquant.exchange.gateio import gateio                                        # noqa: F401
from byquant.exchange.gemini import gemini                                        # noqa: F401
from byquant.exchange.hitbtc import hitbtc                                        # noqa: F401
from byquant.exchange.hitbtc3 import hitbtc3                                      # noqa: F401
from byquant.exchange.hollaex import hollaex                                      # noqa: F401
from byquant.exchange.huobi import huobi                                          # noqa: F401
from byquant.exchange.huobijp import huobijp                                      # noqa: F401
from byquant.exchange.huobipro import huobipro                                    # noqa: F401
from byquant.exchange.idex import idex                                            # noqa: F401
from byquant.exchange.independentreserve import independentreserve                # noqa: F401
from byquant.exchange.indodax import indodax                                      # noqa: F401
from byquant.exchange.kraken import kraken                                        # noqa: F401
from byquant.exchange.krakenfutures import krakenfutures                          # noqa: F401
from byquant.exchange.kucoin import kucoin                                        # noqa: F401
from byquant.exchange.kucoinfutures import kucoinfutures                          # noqa: F401
from byquant.exchange.kuna import kuna                                            # noqa: F401
from byquant.exchange.latoken import latoken                                      # noqa: F401
from byquant.exchange.lbank import lbank                                          # noqa: F401
from byquant.exchange.lbank2 import lbank2                                        # noqa: F401
from byquant.exchange.luno import luno                                            # noqa: F401
from byquant.exchange.lykke import lykke                                          # noqa: F401
from byquant.exchange.mercado import mercado                                      # noqa: F401
from byquant.exchange.mexc import mexc                                            # noqa: F401
from byquant.exchange.mexc3 import mexc3                                          # noqa: F401
from byquant.exchange.ndax import ndax                                            # noqa: F401
from byquant.exchange.novadax import novadax                                      # noqa: F401
from byquant.exchange.oceanex import oceanex                                      # noqa: F401
from byquant.exchange.okcoin import okcoin                                        # noqa: F401
from byquant.exchange.okex import okex                                            # noqa: F401
from byquant.exchange.okex5 import okex5                                          # noqa: F401
from byquant.exchange.okx import okx                                              # noqa: F401  Uakeey
from byquant.exchange.paymium import paymium                                      # noqa: F401
from byquant.exchange.phemex import phemex                                        # noqa: F401
from byquant.exchange.poloniex import poloniex                                    # noqa: F401
from byquant.exchange.poloniexfutures import poloniexfutures                      # noqa: F401
from byquant.exchange.probit import probit                                        # noqa: F401
#from byquant.exchange.stex import stex                                            # noqa: F401
from byquant.exchange.tidex import tidex                                          # noqa: F401
from byquant.exchange.timex import timex                                          # noqa: F401
from byquant.exchange.tokocrypto import tokocrypto                                # noqa: F401
from byquant.exchange.upbit import upbit                                          # noqa: F401
from byquant.exchange.wavesexchange import wavesexchange                          # noqa: F401
from byquant.exchange.wazirx import wazirx                                        # noqa: F401
from byquant.exchange.whitebit import whitebit                                    # noqa: F401
from byquant.exchange.woo import woo                                              # noqa: F401
#from byquant.exchange.xt import xt                                                # noqa: F401
from byquant.exchange.yobit import yobit                                          # noqa: F401
from byquant.exchange.zaif import zaif                                            # noqa: F401
from byquant.exchange.zonda import zonda                                          # noqa: F401

from byquant.exchange.buda import buda                                            # noqa: F401
from byquant.exchange.flowbtc import flowbtc                                      # noqa: F401
from byquant.exchange.itbit import itbit                                          # noqa: F401
from byquant.exchange.ripio import ripio                                          # noqa: F401
from byquant.exchange.zb import zb                                                # noqa: F401

exchanges = [
    'ace',
    'alpaca',
    'ascendex',
    'bequant',
    'bigone',
    'binance',
    'binancecoinm',
    'binanceus',
    'binanceusdm',
    'bit2c',
    'bitbank',
    'bitbay',
    'bitbns',
    'bitcoincom',
    'bitfinex',
    'bitfinex2',
    'bitflyer',
    'bitforex',
    'bitget',
    'bithumb',
    'bitmart',
    'bitmex',
    'bitopro',
    'bitpanda',
    'bitrue',
    'bitso',
    'bitstamp',
    'bitstamp1',
    'bittrex',
    'bitvavo',
    'bkex',
    'bl3p',
    'blockchaincom',
    'btcalpha',
    'btcbox',
    #'btcex',
    'btcmarkets',
    'btctradeua',
    'btcturk',
    'bybit',
    'cex',
    'coinbase',
    'coinbaseprime',
    'coinbasepro',
    'coincheck',
    'coinex',
    'coinfalcon',
    'coinmate',
    'coinone',
    'coinsph',
    'coinspot',
    'cryptocom',
    'currencycom',
    'delta',
    'deribit',
    'digifinex',
    'exmo',
    'fmfwio',
    'gate',
    'gateio',
    'gemini',
    'hitbtc',
    'hitbtc3',
    'hollaex',
    'huobi',
    'huobijp',
    'huobipro',
    'idex',
    'independentreserve',
    'indodax',
    'kraken',
    'krakenfutures',
    'kucoin',
    'kucoinfutures',
    'kuna',
    'latoken',
    'lbank',
    'lbank2',
    'luno',
    'lykke',
    'mercado',
    'mexc',
    'mexc3',
    'ndax',
    'novadax',
    'oceanex',
    'okcoin',
    'okex',
    'okex5',
    'okx',
    'paymium',
    'phemex',
    'poloniex',
    'poloniexfutures',
    'probit',
#    'stex',
    'tidex',
    'timex',
    'tokocrypto',
    'upbit',
    'wavesexchange',
    'wazirx',
    'whitebit',
    'woo',
    #'xt',
    'yobit',
    'zaif',
    'zonda',
]

def getExchange(exName):
    #print(exName)
    exName=exName.lower()
    if exName == 'ace': result = ace()
    elif exName == 'alpaca': result = alpaca()
    elif exName == 'ascendex': result = ascendex()
    elif exName == 'bequant': result = bequant()
    elif exName == 'bigone': result = bigone()
    elif exName == 'binance': result = binance()
    elif exName == 'binancecoinm': result = binancecoinm()
    elif exName == 'binanceus': result = binanceus()
    elif exName == 'binanceusdm': result = binanceusdm()
    elif exName == 'bit2c': result = bit2c()
    elif exName == 'bitbank': result = bitbank()
    elif exName == 'bitbay': result = bitbay()
    elif exName == 'bitbns': result = bitbns()
    elif exName == 'bitcoincom': result = bitcoincom()
    elif exName == 'bitfinex': result = bitfinex()
    elif exName == 'bitfinex2': result = bitfinex2()
    elif exName == 'bitflyer': result = bitflyer()
    elif exName == 'bitforex': result = bitforex()
    elif exName == 'bitget': result = bitget()
    elif exName == 'bithumb': result = bithumb()
    elif exName == 'bitmart': result = bitmart()
    elif exName == 'bitmex': result = bitmex()
    elif exName == 'bitopro': result = bitopro()
    elif exName == 'bitpanda': result = bitpanda()
    elif exName == 'bitrue': result = bitrue()
    elif exName == 'bitso': result = bitso()
    elif exName == 'bitstamp': result = bitstamp()
    elif exName == 'bitstamp1': result = bitstamp1()
    elif exName == 'bittrex': result = bittrex()
    elif exName == 'bitvavo': result = bitvavo()
    elif exName == 'bkex': result = bkex()
    elif exName == 'bl3p': result = bl3p()
    elif exName == 'blockchaincom': result = blockchaincom()
    elif exName == 'btcalpha': result = btcalpha()
    elif exName == 'btcbox': result = btcbox()
    #elif exName == 'btcex': result = btcex()
    elif exName == 'btcmarkets': result = btcmarkets()
    elif exName == 'btctradeua': result = btctradeua()
    elif exName == 'btcturk': result = btcturk()
    elif exName == 'buda': result = buda()
    elif exName == 'bybit': result = bybit()
    elif exName == 'cex': result = cex()
    elif exName == 'coinbase': result = coinbase()
    elif exName == 'coinbaseprime': result = coinbaseprime()
    elif exName == 'coinbasepro': result = coinbasepro()
    elif exName == 'coincheck': result = coincheck()
    elif exName == 'coinex': result = coinex()
    elif exName == 'coinfalcon': result = coinfalcon()
    elif exName == 'coinmate': result = coinmate()
    elif exName == 'coinone': result = coinone()
    elif exName == 'coinspot': result = coinspot()
    elif exName == 'cryptocom': result = cryptocom()
    elif exName == 'currencycom': result = currencycom()
    elif exName == 'delta': result = delta()
    elif exName == 'deribit': result = deribit()
    elif exName == 'digifinex': result = digifinex()
    elif exName == 'exmo': result = exmo()
    elif exName == 'flowbtc': result = flowbtc()
    elif exName == 'fmfwio': result = fmfwio()
    elif exName == 'gate': result = gate()
    elif exName == 'gateio': result = gate() #gateio
    elif exName == 'gemini': result = gemini()
    elif exName == 'hitbtc': result = hitbtc()
    elif exName == 'hitbtc3': result = hitbtc3()
    elif exName == 'hollaex': result = hollaex()
    elif exName == 'huobi': result = huobi()
    elif exName == 'huobijp': result = huobijp()
    elif exName == 'huobipro': result = huobipro()
    elif exName == 'idex': result = idex()
    elif exName == 'independentreserve': result = independentreserve()
    elif exName == 'indodax': result = indodax()
    elif exName == 'itbit': result = itbit()
    elif exName == 'kraken': result = kraken()
    elif exName == 'krakenfutures': result = krakenfutures()
    elif exName == 'kucoin': result = kucoin()
    elif exName == 'kucoinfutures': result = kucoinfutures()
    elif exName == 'kuna': result = kuna()
    elif exName == 'latoken': result = latoken()
    elif exName == 'lbank': result = lbank()
    elif exName == 'lbank2': result = lbank2()
    elif exName == 'luno': result = luno()
    elif exName == 'lykke': result = lykke()
    elif exName == 'mercado': result = mercado()
    elif exName == 'mexc': result = mexc()
    elif exName == 'mexc3': result = mexc3()
    elif exName == 'ndax': result = ndax()
    elif exName == 'novadax': result = novadax()
    elif exName == 'oceanex': result = oceanex()
    elif exName == 'okcoin': result = okcoin()
    elif exName == 'okex': result = okex()
    elif exName == 'okex5': result = okex5()
    elif exName == 'okx': result = okx()
    elif exName == 'paymium': result = paymium()
    elif exName == 'phemex': result = phemex()
    elif exName == 'poloniex': result = poloniex()
    elif exName == 'poloniexfutures': result = poloniexfutures()
    elif exName == 'probit': result = probit()
    elif exName == 'ripio': result = ripio()
#    elif exName == 'stex': result = stex()
    elif exName == 'tidex': result = tidex()
    elif exName == 'timex': result = timex()
    elif exName == 'tokocrypto': result = tokocrypto()
    elif exName == 'upbit': result = upbit()
    elif exName == 'wavesexchange': result = wavesexchange()
    elif exName == 'wazirx': result = wazirx()
    elif exName == 'whitebit': result = whitebit()
    elif exName == 'woo': result = woo()
    elif exName == 'yobit': result = yobit()
    elif exName == 'zaif': result = zaif()
    elif exName == 'zb': result = zb()
    elif exName == 'zonda': result = zonda()
    else:
        print('No %s' % (exName))
    return result

base = [
    'Exchange',
    'Precise',
    'exchanges',
    'decimal_to_precision',
]

__all__ = base + errors.__all__ + exchanges
