from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud the crypto exchange price between two symbols, from Cryptonator API
"""


def crypto_exchange(symbol_1, symbol_2):
    """
    :param symbol_1: str, monetary(or crypto) symbol
    :param symbol_2: str, monetary(or crypto) symbol
    :return: str, exchange rate of one symbol_1 in symbol_2 currency
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'
    }
    url = 'https://api.cryptonator.com/api/ticker/%s-%s' % (symbol_1.lower(), symbol_2.lower())
    rh = RequestHandler([url], RequestData(GET, headers=headers), RequestErrorData(allow_errors=True))
    rh.run()
    if rh.errors:
        print("[!] Crypto exchange returned error: %s" % rh.errors)
        return 'Crypto exchange returned error: %s' % rh.errors[0]['response'].status_code

    return 'One %s is valued %s %s.' % (symbol_1, '%.1f' % float(rh.responses[0].json()['ticker']['price']), symbol_2)


if __name__ == "__main__":
    read_tts_single(crypto_exchange('BTC', 'USD'))