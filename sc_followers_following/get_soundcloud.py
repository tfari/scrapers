import sys

from helpers.sc_helpers import get_client_id, get_user_id
from helpers.req_handler import GET, RequestData, RequestErrorData, RequestHandler
from helpers.excel_writer import ExcelWriter

VALID_MODES = FOLLOWERS, FOLLOWINGS = 'followers', 'followings'

VALID_ORDER_KEYS = ['country', 'city', 'description', 'track_count', 'discogs_name', 'public_favorites_count', 'id',
                    'reposts_count', 'myspace_name', 'website_title', 'last_modified', 'first_name', 'plan', 'website',
                    'playlist_count', 'kind', 'last_name', 'uri', 'followings_count', 'likes_count', 'full_name',
                    'avatar_url', 'comments_count', 'followers_count', 'online', 'permalink', 'permalink_url',
                    'username']

"""
Creates an .xlsx file of a followers or following list of a soundcloud.com user.

Raises MissingUsername, BadModeArgument and BadOrderHeader

Running the same request more than once will result in the request being appended to the end of the existing file, 
it won't "step" over it.

Terminal Usage:
    python get_soundcloud.py USERNAME | MODE | ORDER_HEADER

    USERNAME => string, valid soundcloud username
    
    MODE => optional string, either 'followers' or 'followings'
        "followers" by default.

    VALID_ORDER_KEYS => optional string, has to be one of the VALID_ORDER_KEYS.
            "country" by default.
            
            ['country', 'city', 'description', 'track_count', 'discogs_name', 'public_favorites_count', 'id',
            'reposts_count', 'myspace_name', 'website_title', 'last_modified', 'first_name', 'plan', 'website',
            'playlist_count', 'kind', 'last_name', 'uri', 'followings_count', 'likes_count', 'full_name',
            'avatar_url', 'comments_count', 'followers_count', 'online', 'permalink', 'permalink_url',
            'username']

    python get_soundcloud.py MyUser
    python get_soundcloud.py MyUser following
    python get_soundcloud.py MyUser followers first_name
"""


def get_data(user_name, mode, order_by):
    """
    Produces an excel comprised of either the followers or the following lists (depending on mode) of Soundcloud user
    user_name, ordered by order_header.

    :param user_name: string, valid soundcloud user_name
    :param mode: string, 'followers' or 'followings'
    :param order_by: string, element in VALID_ORDER_KEYS
    :return: None
    """

    # Get client_id and user_id
    client_id = get_client_id()
    user_id = get_user_id(user_name, client_id)
    print('[*] Scraping %s data on %s, user_id: %s, ordered by key: "%s"' % (mode, user_name, user_id, order_by))

    # Get headers
    url = 'https://api.soundcloud.com/users/%s?client_id=%s' % (user_id, client_id)
    rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    rh.run()
    jsoned = rh.responses[0].json()
    headers = [key for key in jsoned.keys()]

    headers.remove('subscriptions')  # Only key different from users/ and followers/ returns.
    xls = ExcelWriter(user_name + '_' + mode, headers)  # Init ExcelWriter()

    # Get counts
    followers_count = jsoned['followers_count']
    followings_count = jsoned['followings_count']

    # Select count based on mode
    count_using = followers_count if mode == FOLLOWERS else followings_count
    print('[*][*] %s %s' % (count_using, mode))

    # Get followers/followings list while there is a next_href url
    page_size = 200
    url = 'https://api.soundcloud.com/users/%s/%s?client_id=%s&page_size=%s&format=json' % \
          (user_id, mode, client_id, page_size)

    rd, rde = RequestData(GET), RequestErrorData(allow_errors=False)

    while url:
        rh = RequestHandler([url], rd, rde)
        rh.run()
        jsoned = rh.responses[0].json()
        [xls.add(user) for user in jsoned['collection']]
        url = jsoned['next_href']
    print('[*][*] Fetched %s of %s %s' % (len(xls.data), count_using, mode))

    # Sort and write
    xls.order_by(order_by)
    xls.write()
    print('[*][*] Saved %s data on %s' % (mode, user_name))


# EXCEPTIONS


class GetSoundcloudError(Exception):
    pass


class MissingUsername(GetSoundcloudError):
    pass


class BadModeArgument(GetSoundcloudError):
    pass


class BadOrderHeader(GetSoundcloudError):
    pass


if __name__ == '__main__':
    # Set default values
    user_name, mode, order_by = '', FOLLOWERS, 'country'

    # Check username is there
    try:
        user_name = sys.argv[1]
    except IndexError:
        raise MissingUsername()

    # Check optionals
    try:
        mode = sys.argv[2]
        if mode not in VALID_MODES:
            raise BadModeArgument(mode)

        order_by = sys.argv[3]
        if order_by not in VALID_ORDER_KEYS:
            raise BadOrderHeader(order_by)

    except IndexError:
        pass

    get_data(user_name, mode, order_by)

