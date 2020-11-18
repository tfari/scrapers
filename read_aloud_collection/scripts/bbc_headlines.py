from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single
from bs4 import BeautifulSoup


"""
Read aloud the newest BBC headlines by tag.
We use fmt='8khz_8bit_mono' on tts_reader when called as __main__ because it takes too long otherwise.
"""


def bbc_headlines(tag='world', use_descriptions=True):
    """
    :param tag:str, the type of news, default = 'world'
    :param use_descriptions: bool, if true add descriptions to each title, default= True
    :return: str, the titles, and optionally, descriptions, of the BBC headlines for tag
    """

    # Get everything
    url = 'http://feeds.bbci.co.uk/news/%s/rss.xml' % tag
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    bs = BeautifulSoup(rh.responses[0].text, 'html.parser')
    titles = [t.text for t in bs.findAll('title')][2:]
    descriptions = [d.text for d in bs.findAll('description')][1:]

    # Make them into a list
    out = []
    count = 0
    for title in titles:
        out_str = '%s' % title
        if use_descriptions:
            out_str += ': %s' % descriptions[count]
        out.append(out_str)
        count += 1

    return "BBC %s news for today: \n%s" % (tag, '.\n'.join(out))


if __name__ == "__main__":
    read_tts_single(bbc_headlines(use_descriptions=False), fmt='8khz_8bit_mono')
