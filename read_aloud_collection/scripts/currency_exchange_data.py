from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud the currency exchange price between two symbols, from CurrencyConverter API
You need a valid (free) API KEY to use this script.  https://www.currencyconverterapi.com/
"""

API_KEY = None


def currency_exchange(symbol_1, symbol_2):
    """
    :param symbol_1: str, monetary symbol
    :param symbol_2: str, monetary symbol
    :return: str, exchange rate of one symbol_1 in symbol_2 currency
    """
    if not API_KEY:
        raise NoApiKey()

    url = 'https://free.currconv.com/api/v7/convert?q=%s_%s&compact=ultra&apiKey=%s' % \
          (symbol_1.upper(), symbol_2.upper(), API_KEY)
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    price = (rh.responses[0].json()['%s_%s' % (symbol_1.upper(), symbol_2.upper())])
    return 'One %s is valued %s %s' % (symbol_1, '{0:.5}'.format(price), symbol_2)


# Exceptions

class NoApiKey(Exception):
    pass


if __name__ == "__main__":
    read_tts_single(currency_exchange('GBP', 'USD'))
