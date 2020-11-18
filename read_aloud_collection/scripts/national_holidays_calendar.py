import datetime

from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single


COUNTRY_CODE = 'US'  # Default value

"""
Reads aloud national holidays for today from Nager.date api
"""


def national_holidays_calendar(country_code=COUNTRY_CODE):
    """
    :param country_code: str, country code for the country which national holidays you want to check today against
    :return: str, the name of the national holiday for the day, in english
    """
    # Get today
    year, month, day = datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day
    today = '%s-%s-%s' % (year, '{:02d}'.format(month), '{:02d}'.format(day))

    # Get all holidays
    url = 'https://date.nager.at/api/v2/PublicHolidays/%s/%s' % (year, country_code)
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()

    # Filter holidays for today's date
    today_holiday = [holiday['name'] for holiday in rh.responses[0].json() if holiday['date'] == today]

    if len(today_holiday) > 0:
        return 'Today is: %s ' % today_holiday[0]
    else:
        return 'No holidays today'


if __name__ == "__main__":
    read_tts_single(national_holidays_calendar())
