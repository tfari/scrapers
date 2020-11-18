from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single
from bs4 import BeautifulSoup


"""
Read aloud the newest El Mundo headlines by tag.
We use fmt='8khz_8bit_mono' on tts_reader when called as __main__ because it takes too long otherwise.
"""


def elmundo_headlines(tag='internacional'):
    """
    :param tag:str, the type of news, default = 'edition_world'
    :return: str, the titles of the El Mundo headlines for tag
    """

    # Get everything
    url = 'https://e00-elmundo.uecdn.es/elmundo/rss/%s.xml' % tag
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    bs = BeautifulSoup(rh.responses[0].text, 'html.parser')
    items = [i for i in bs.findAll('item')]

    # Make them into a list
    out = []
    for item in items:
        out_str = '%s' % item.find('title').text
        out.append(out_str)

    return "Noticias de El Mundo de hoy, %s: \n%s" % (tag, '.\n'.join(out))


if __name__ == "__main__":
    read_tts_single(elmundo_headlines(), fmt='8khz_8bit_mono', language='es-es')
