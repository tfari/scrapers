from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single
from bs4 import BeautifulSoup


"""
Read aloud the newest CNN headlines by tag.
We use fmt='8khz_8bit_mono' on tts_reader when called as __main__ because it takes too long otherwise.
"""


def cnn_headlines(tag='edition_world', use_descriptions=True):
    """
    :param tag:str, the type of news, default = 'edition_world'
    :param use_descriptions: bool, if true add descriptions to each title, default= True
    :return: str, the titles, and optionally, descriptions, of the CNN headlines for tag
    """

    # Get everything
    url = 'http://rss.cnn.com/rss/%s.rss' % tag
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
            # # Fix for img tags inside description that don't get parsed by BeautifulSoup
            desc = descriptions[count]
            end_pos = desc.find('<')
            if end_pos != -1:
                desc = desc[:end_pos]

            out_str += ': %s' % desc
        out.append(out_str)
        count += 1

    return "CNN %s news for today: \n%s" % (tag, '.\n'.join(out))


if __name__ == "__main__":
    read_tts_single(cnn_headlines(use_descriptions=False), fmt='8khz_8bit_mono')
