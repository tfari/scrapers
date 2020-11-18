from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud an activity to do when bored from Bored API
"""


def bored_activity(participants=1):
    """
    :param participants: int, number of participants
    :return: str, an activity and its type
    """
    url = 'https://www.boredapi.com/api/activity/?participants=%s' % participants
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    return "%s activity: %s" % (rh.responses[0].json()['type'], rh.responses[0].json()['activity'])


if __name__ == "__main__":
    read_tts_single(bored_activity())
