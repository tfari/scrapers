from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single
from bs4 import BeautifulSoup

"""
Reads aloud a design quote from Quotes on Design API
"""


def design_quotes():
    """
    :return: str, a design Quote
    """
    url = 'https://quotesondesign.com/wp-json/wp/v2/posts/?orderby=rand'
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    jsoned = rh.responses[0].json()[0]
    bs = BeautifulSoup(jsoned['content']['rendered'], 'html.parser')
    quote = bs.text.replace('\n', '')
    return "%s said: %s" % (jsoned['title']['rendered'], quote)


if __name__ == "__main__":
    read_tts_single(design_quotes())
