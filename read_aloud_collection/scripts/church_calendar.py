from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud the Roman Catholic church celebrations for today, from Calapi API
"""


def church_calendar():
    """
    :return: str, the names for the Roman Catholic church celebrations for today, joined by \n
    """
    url = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/general-en/today'
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    celebrations = [celeb['title'] for celeb in rh.responses[0].json()['celebrations']]
    return 'The church calendar celebrations for today are: %s' % '\n'.join(celebrations)


if __name__ == "__main__":
    read_tts_single(church_calendar())
