import json
import requests
import re
from bs4 import BeautifulSoup


# v 0.0.2


"""
Bandcamp related helper functions. 
"""


def __clean_json_strs(s):
    """
    Clean instances when the json is URI encoded.
    :param s: str
    :return: {'data': json}
    """
    # Clean
    s = s.replace('&quot;', '"').strip()
    s = s[1:] if s[0] == '"' else s
    s = s[:-1] if s[-1] == '"' else s

    return {'data': json.loads(s)}


def is_valid_bandcamp_url(url):
    """
    :param url: str
    :return: True/False depending on if url is a valid Bandcamp URL
    """
    r = requests.get(url, allow_redirects=False)
    if r.status_code == 200:
        return True
    return False


def is_valid_username(username):
    """
    :param username: str
    :return: True/False depending on if url is a valid Bandcamp username
    """
    return is_valid_bandcamp_url('https://%s.bandcamp.com' % username)


def get_all_info(username):
    """
    Gets a list of relative links to all albums and tracks in username's Bandcamp profile
    :param username:
    :return:
    """
    r = requests.get('https://%s.bandcamp.com/music' % username)
    bs = BeautifulSoup(r.text, 'html.parser')
    regex = re.compile('.*music-grid-item .*')
    urls = []
    for a in bs.find_all("li", {"class": regex}):
            urls.append(a.find('a').get('href'))

    return urls


def get_album_info(username, album_relative_url):
    """
    :param username: str
    :param album_relative_url: str
    :return: dict. representation of album information
    """
    response = {}
    r = requests.get('https://%s.bandcamp.com%s' % (username, album_relative_url))
    bs = BeautifulSoup(r.text, 'html.parser')
    scripts = bs.findAll('script')
    for s in scripts:
        if str(s).find('data-tralbum') != -1:
            s = str(s).split('data-tralbum=')[1].replace("'", '').split('data-tralbum-collect-info')[0]
            jsoned = __clean_json_strs(s)

            response['artist'] = jsoned['data']['artist']
            response['artist_avatar'] = None
            response['album_title'] = jsoned['data']['current']['title']
            response['album_cover'] = str(jsoned['data']['art_id'])
            response['track_info'] = jsoned['data']['trackinfo']
            try:
                response['album_release'] = str(jsoned['data']['current']['release_date']).split(' ')[2]
            except SyntaxError:
                response['album_release'] = None

    return response


def get_track_info(username, track_relative_url):
    """
    :param username: str
    :param track_relative_url: str
    :return: dict. representation of track information
    """
    response = {}
    r = requests.get('https://%s.bandcamp.com%s' % (username, track_relative_url))
    bs = BeautifulSoup(r.text, 'html.parser')
    scripts = bs.findAll('script')
    for s in scripts:
        if str(s).find('data-tralbum') != -1:
            s = str(s).split('data-tralbum=')[1].replace("'", '').split('data-tralbum-collect-info')[0]
            jsoned = __clean_json_strs(s)

            response['artist'] = jsoned['data']['artist']
            response['artist_avatar'] = None
            response['album_cover'] = str(jsoned['data']['art_id'])
            response['track_info'] = jsoned['data']['trackinfo'][0]

            try:
                response['album_url'] = jsoned['data']['album_url']
            except IndexError:
                response['album_url'] = None

    return response
