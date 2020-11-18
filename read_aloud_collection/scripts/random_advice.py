from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud a random advice from Advice Slip API
"""


def random_advice(n=1):
    """
    :param n: int, number of advices to read
    :return: str, n random advices, joined by \n
    """
    url = 'https://api.adviceslip.com/advice'

    advices = []
    for i in range(n):
        rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
        rh.run()
        advices.append(rh.responses[0].json()['slip']['advice'])

    return '\n'.join(advices)


if __name__ == "__main__":
    read_tts_single(random_advice(5))
