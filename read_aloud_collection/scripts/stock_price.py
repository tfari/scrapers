from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud the updated price of a stock, from Financial Modelling Prep API
"""

API_KEY = None


def stock_price(symbol):
    """
    :param symbol: str, stock symbol
    :return: str, exchange rate of one symbol_1 in symbol_2 currency
    """
    if not API_KEY:
        raise NoApiKey()

    url = 'https://financialmodelingprep.com/api/v3/quote/%s?apikey=%s' % (symbol.upper(), API_KEY)

    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()

    return '%s stocks are valued at %s USD.' % (rh.responses[0].json()[0]['name'],
                                                rh.responses[0].json()[0]['price'])


class NoApiKey(Exception):
    pass


if __name__ == "__main__":
    read_tts_single(stock_price('AAPL'))
