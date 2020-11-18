from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single
from bs4 import BeautifulSoup


"""
Read aloud the newest RT headlines by tag.
We use fmt='8khz_8bit_mono' on tts_reader when called as __main__ because it takes too long otherwise.
"""


def rt_headlines(tag='news', use_descriptions=True, limit=None):
    """
    :param tag:str, the type of news, default = 'world'
    :param use_descriptions: bool, if true add descriptions to each title, default= True
    :param limit: if not None, limit number of results, default=None
    :return: str, the titles, and optionally, descriptions, of the RT headlines for tag
    """

    # Get everything
    url = 'https://www.rt.com/rss/%s' % tag
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    bs = BeautifulSoup(rh.responses[0].text, 'lxml')
    titles = [t.text for t in bs.findAll('title')][2:]
    descriptions = [d.text for d in bs.findAll('description')][1:]

    # Make them into a list
    out = []
    count = 0
    for title in titles:
        out_str = '%s' % title
        if use_descriptions:
            # Fix for "Read Full Article at RT.com" inside description
            desc = descriptions[count]
            end_pos = desc.find('Read Full Article at')
            if end_pos != -1:
                desc = desc[:end_pos]

            out_str += ': %s' % desc
        out.append(out_str)
        count += 1

    if limit:
        print('[*] Reducing RT from: %s to %s' % (len(out), limit))
        out = out[:limit]

    return "RT %s news for today: \n%s" % (tag, '.\n'.join(out))


if __name__ == "__main__":
    read_tts_single(rt_headlines(use_descriptions=False), fmt='8khz_8bit_mono')
