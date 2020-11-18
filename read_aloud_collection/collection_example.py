import datetime

from helpers.tts_reader import read_tts_single
from scripts import bbc_headlines, bored_advice, church_calendar, cnn_headlines, crypto_exchange_data, currency_exchange_data, \
    design_quotes, hackernews_top_stories, national_holidays_calendar, quotes, random_advice, rt_headlines, stock_price, weather


"""
Aggregate all scripts functions returns into a single call to read_tts_single
We use fmt='8khz_8bit_mono' on tts_reader when called as __main__ because it takes too long otherwise.
"""


def collection():
    """Example"""
    print("[*] Collecting API responses")
    today = '%s-%s-%s' % (datetime.datetime.now().year, '{:02d}'.format(datetime.datetime.now().month),
                          '{:02d}'.format(datetime.datetime.now().day))

    # Header
    returns = ['Today is %s' % today]

    # Aggregate
    returns += [weather.weather('boston'),
                national_holidays_calendar.national_holidays_calendar('US'),
                church_calendar.church_calendar(),
                "Financial information:",
                currency_exchange_data.currency_exchange('EUR', 'USD'),
                crypto_exchange_data.crypto_exchange('BTC', 'USD'),
                stock_price.stock_price('AAPL'),
                "News for today:",
                bbc_headlines.bbc_headlines('world'),
                cnn_headlines.cnn_headlines(),
                rt_headlines.rt_headlines(),
                hackernews_top_stories.hackernews(),
                "Daily Quotes: ",
                design_quotes.design_quotes(),
                quotes.quotes(),
                "Daily advice: ",
                random_advice.random_advice(),
                bored_advice.bored_activity()
                ]

    out = '\n\n'.join(returns)
    print("[*] Calling tts_reader")
    return out


if __name__ == '__main__':
    read_tts_single(collection(), fmt='8khz_8bit_mono')


