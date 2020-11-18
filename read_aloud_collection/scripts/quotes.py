from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

import time
"""
Reads aloud a quote from Forismatic API
"""


def quotes():
    """
    :return: str, a Quote
    """
    url = 'http://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json'
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()

    try:
        jsoned = rh.responses[0].json()
    except:
        time.sleep(2)  # We do this cause sometimes the json is malformed
        return quotes()

    return "%s said: %s" % (jsoned['quoteAuthor'], jsoned['quoteText'])


if __name__ == "__main__":
    read_tts_single(quotes())
