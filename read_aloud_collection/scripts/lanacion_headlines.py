from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single
from bs4 import BeautifulSoup


"""
Read aloud the newest La Nacion headlines for latest news.
We use fmt='8khz_8bit_mono' on tts_reader when called as __main__ because it takes too long otherwise.
"""


def lanacion_headline(use_descriptions=True):
    """
    :param use_descriptions: bool, if true add descriptions to each title, default= True
    :return: str, the titles of the La Nacion headlines for latest news
    """

    # Get everything
    url = 'http://contenidos.lanacion.com.ar/herramientas/rss/categoria_id=30'
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    bs = BeautifulSoup(rh.responses[0].text, 'html.parser')
    items = [i for i in bs.findAll('entry')]

    # Make them into a list
    out = []
    for item in items:
        out_str = '%s' % item.find('title').text
        if use_descriptions:
            out_str += ': %s' % item.find('div').text
        out.append(out_str)

    return "Noticias de La Nacion de hoy: \n%s" % ('.\n'.join(out))


if __name__ == "__main__":
    read_tts_single(lanacion_headline(use_descriptions=False), fmt='8khz_8bit_mono', language='es-mx')
