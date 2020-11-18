from helpers.req_handler import GET, RequestHandler, RequestData, RequestErrorData
from helpers.tts_reader import read_tts_single

"""
Reads aloud the weather from MetaWeather API
"""


def weather(city):
    """
    :param city: str, a valid city name
    :return: str, the weather information for city
    """
    # First we get the id for the city
    url = 'https://www.metaweather.com/api/location/search/?query=%s' % city.lower().replace(' ', '+')
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    weather_id = rh.responses[0].json()[0]['woeid']

    # Get weather information
    url = 'https://www.metaweather.com/api/location/%s' % weather_id
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    weather_data = (rh.responses[0].json()['consolidated_weather'][0])

    return "Weather state for %s: %s. " \
           "Temperature is: %s °, With a min of: %s °, and a max of: %s °. Humidity is: %s percent" % \
           (city, weather_data['weather_state_name'], weather_data['the_temp'], weather_data['min_temp'],
            weather_data['max_temp'], weather_data['humidity'])


if __name__ == "__main__":
    read_tts_single(weather('boston'))
