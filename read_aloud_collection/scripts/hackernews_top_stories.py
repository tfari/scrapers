from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud the titles of the top 30 Hackernews stories (frontpage)
We use fmt='8khz_8bit_mono' on tts_reader when called as __main__ because it takes too long otherwise.
"""


def hackernews():
    """
    :return: str, the titles of the top 10 Hackernews stories
    """
    # First we get the id for the threads
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    threads_ids = (rh.responses[0].json())[:30]

    # Then we get the threads titles
    titles = []
    for thread_id in threads_ids:
        url = 'https://hacker-news.firebaseio.com/v0/item/%s.json?print=pretty' % (thread_id)
        rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
        rh.run()
        titles.append(rh.responses[0].json()['title'])

    return 'The Hackernews 30 top stories for the day are: \n%s' % '.\n'.join(titles)


if __name__ == "__main__":
    read_tts_single(hackernews(), fmt='8khz_8bit_mono')
