from bs4 import BeautifulSoup
import json

from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud the updated price of a stock, from Financial Modelling Prep API
"""


def stock_price(symbol):
    """
    :param symbol: str, stock symbol
    :return: str, exchange rate of one symbol_1 in symbol_2 currency
    """
    url = 'https://financialmodelingprep.com/api/company/real-time-price/%s' % (symbol.upper())

    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    bs = BeautifulSoup(rh.responses[0].text, 'html.parser')

    return '%s is valued at %s USD' % (symbol, json.loads(bs.find('pre').text)['price'])


if __name__ == "__main__":
    read_tts_single(stock_price('AAPL'))
