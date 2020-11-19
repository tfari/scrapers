import os
import sys
import requests
import json

from helpers.sc_helpers import get_client_id, get_user_data, get_all_playlists_data, get_all_tracks_data, _resolve
from helpers.file_getter import get_file
from helpers.id3_wrapper import mp3_tag_file


"""
Downloads Soundcloud tracks as .mp3. 

Usage:
    python sc_get.py URL | -v
    URL: A Soundcloud url
    -v (OPTIONAL): Verbose output
"""


CLIENT_ID = get_client_id()
DOWNLOADED = []
OUTPUT_PATH = ''
VERBOSE = False
INVALID_FILENAME_CHARS = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.']


# LOADS OUTPUT_PATH
try:
    OUTPUT_PATH = json.loads(open('settings.json', 'r').read())['OUTPUT_PATH']
except FileNotFoundError:
    default = {'OUTPUT_PATH': os.getcwd() + '/output'}
    with open('settings.json', 'w') as f:
        f.write(json.dumps(default, indent=True))
    OUTPUT_PATH = default['OUTPUT_PATH']

if OUTPUT_PATH == '/output':
    settings = {'OUTPUT_PATH': os.getcwd() + '/output'}
    with open('settings.json', 'w') as f:
        f.write(json.dumps(settings, indent=True))
    OUTPUT_PATH = settings['OUTPUT_PATH']

# Path check
if not (os.path.isdir(OUTPUT_PATH)):
    os.makedirs(OUTPUT_PATH)


#######################################################################################################################
#######################################################################################################################

def get_everything(account_data, all_playlists_data, all_tracks_data):
    """
    Calls GET on every playlist and track of the user

    :param account_data:
    :param all_playlists_data:
    :param all_tracks_data:
    :return:
    """
    # Gets artist artwork
    if account_data['avatar_url']:
        url = account_data['avatar_url'].split('-large.jpg')[0] + '-t500x500.jpg'
        artist_cover = requests.get(url).content
    else:
        artist_cover = None

    # Gets everything
    get_all_playlists(all_playlists_data)
    get_all_tracks(account_data['username'], 'Tracks', all_tracks_data, album_release=None, album_cover=artist_cover,
                   artist_cover=artist_cover)


def get_all_playlists(playlists_data, artist_cover=None):
    """
    Calls GET on every playlist in playlists_data

    :param playlists_data: a list of playlist information
    :param artist_cover: file
    :return: None
    """
    for playlist in playlists_data:
        r = requests.get('http://api.soundcloud.com/playlists/ ' + str(playlist['id']) + '?client_id=' + CLIENT_ID)
        playlist_data = r.json()

        get_specific_playlist(playlist_data, artist_cover)


def get_specific_playlist(playlist_data, artist_cover=None):
    """
    Calls GET on every track in a specific playlist
    :param playlist_data: a dict representation of playlist information
    :param artist_cover: file
    :return: None
    """

    # Get the album release year
    album_release = playlist_data['release_year'] if playlist_data['release_year'] else playlist_data['created_at'].split('/')[0]

    # Get every track inside the playlist
    if playlist_data['tracks']:

        # Get the album cover
        if playlist_data['artwork_url']:
            url = playlist_data['artwork_url'].split('-large.jpg')[0] + '-t500x500.jpg'
            album_cover = requests.get(url).content
        else:
            album_cover = None

        get_all_tracks(playlist_data['user']['username'], playlist_data['title'], playlist_data['tracks'],
                       album_release, album_cover, artist_cover)

    else:  # If the playlist is empty, its blocked for our area or for non logged-in users
        if VERBOSE:
            print("[!] Blocked playlist: '%s'" % playlist_data['title'])


def get_all_tracks(username, playlist_title, track_collection_data, album_release=None, album_cover=None, artist_cover=None):
    """
    Calls GET on a list of tracks

    :param username: str
    :param playlist_title: str
    :param track_collection_data: list of track information
    :param album_release: str/integer, album release year
    :param album_cover: file
    :param artist_cover: file
    :return: None
    """

    # Iterate over the track list and if the track has not been already downloaded, call GET on it and increase count
    count = 1
    for track_data in track_collection_data:
        if track_data['id'] not in DOWNLOADED:
            get_specific_track(username, playlist_title, track_data, album_release, count, album_cover, artist_cover)
            count += 1  # We do it inside the check to get correct numbering for the general track list
        else:
            if VERBOSE:
                print("[!] Already downloaded: %s" % track_data['title'])


def _path_check(path):
    """
    Create the path if it does not already exist
    :param path: str
    :return: None
    """
    if not (os.path.isdir(OUTPUT_PATH + '/%s' % path)):
        os.makedirs(OUTPUT_PATH + '/%s' % path)


def get_specific_track(username, playlist_title, track_data, album_release=None, track_count=0, album_cover=None,
                       artist_cover=None):
    """
    Creates the output directory, downloads the track, and edits its mp3 tags.

    :param username: str
    :param playlist_title: str
    :param track_data: dict representation of track information
    :param album_release: str/integer, album release year
    :param track_count: int
    :param album_cover: file
    :param artist_cover: file
    :return: None
    """

    # Sanitize filename
    for invalid in INVALID_FILENAME_CHARS:
        username = username.replace(invalid, '')
        playlist_title = playlist_title.replace(invalid, '')

    # Create output folder if it doesn't exist
    _path_check(username + '/' + playlist_title)

    # Create filename
    filename = OUTPUT_PATH + '/' + username + '/' + playlist_title + '/' + track_data['title'] + '.mp3'

    # If file already exits:
    try:
        x = open(filename, 'r')
        x.close()
        if VERBOSE:
            print("[!] File already exists: %s" % (track_data['title']))

    # If not
    except FileNotFoundError:
        # Get track artwork
        if track_data['artwork_url']:
            url = track_data['artwork_url'].split('-large.jpg')[0] + '-t500x500.jpg'
            track_cover = requests.get(url).content
        else:
            track_cover = None

        # Download
        get_file('[%s]' % track_data['user']['username'], track_data['stream_url'] + '?client_id=%s' % CLIENT_ID, filename)

        # Edit the tags of the track to match the track_data
        mp3_tag_file(filename, track_data['user']['username'], track_data['title'], track_genre=track_data['genre'],
                     track_count=track_count, album_artist=username, album_title=playlist_title, album_release=album_release,
                     album_cover=album_cover, artist_cover=artist_cover, track_cover=track_cover)

    # Append track to DOWNLOADED list (We do it here to keep track of previously downloaded tracks too.)
    DOWNLOADED.append(track_data['id'])


#######################################################################################################################
#######################################################################################################################


def input_parse(input_url):
    """
    Parses an input url and calls the corresponding function

    :param input_url: str, a Soundcloud url called to be downloaded
    :return: None
    """

    # TODO => Change printing for raises, return list of downloaded stuff

    # Split and clean the input so we can reason about it
    splited_input = input_url.split('/')
    splitted_input = [i for i in splited_input if i != 'http:' and i != 'https:' and i != '']

    # Check for non soundcloud links
    if splitted_input[0] != 'www.soundcloud.com' and splitted_input[0] != 'soundcloud.com':
        print('[!] The link is not a Soundcloud link: %s ' % input_url)
        return False

    # Check for 'soundcloud.com' inputs
    if len(splitted_input) == 1:
        print("[!] The link is not downloadable: %s" % input_url)
        return False

    # Gets info for function calls
    user_data = get_user_data(splitted_input[1], CLIENT_ID)
    username = user_data['username']
    all_playlists_data = get_all_playlists_data(user_data['id'], CLIENT_ID)
    all_tracks_data = get_all_tracks_data(user_data['id'], CLIENT_ID)

    # We reverse the general track list to ensure track counting does not change when new tracks are added
    all_tracks_data.reverse()

    if len(splitted_input) == 2:
        print("[*] Download everything from user: %s" % username)
        get_everything(user_data, all_playlists_data, all_tracks_data)

    elif len(splitted_input) == 3:
        # Full-collection urls
        types = ['tracks', 'albums', 'sets', 'reposts']
        if splitted_input[2] in types:
            print("[*] Download all %s from user: %s" % (splitted_input[2], username))

            if splitted_input[2] == 'tracks':
                get_all_tracks(username, 'Tracks', all_tracks_data)

            elif splitted_input[2] == 'sets':
                get_all_playlists(all_playlists_data)

            # Not implemented collections
            elif splitted_input[2] == 'albums':
                print("[!] Not implemented => Albums")
            elif splitted_input[2] == 'reposts':
                print("[!] Not implemented => Reposts")

        # Direct track urls
        else:
            print("[*] Download track %s from user: %s" % (splitted_input[2], username))
            get_specific_track(username, 'Tracks', _resolve(input_url, CLIENT_ID))

    # Direct set urls
    elif len(splitted_input) == 4:
        if splitted_input[2] != 'sets':
            print("[!] Non-recognized url type: %s" % input_url)
        else:
            print("[*] Download set %s from user: %s" % (splitted_input[3], username))
            get_specific_playlist(_resolve(input_url, CLIENT_ID))

    # Extra urls
    else:
        if splitted_input[2].find('?in=') != -1:  # Combined urls
            print("[!] Not implemented url type: %s" % input_url)
        else:
            print("[!] Non-recognized url type: %s " % input_url)


# Exceptions


class GetSCTrackError(Exception):
    pass


class MissingURL(GetSCTrackError):
    pass


class InvalidOption(GetSCTrackError):
    pass


# Entry point

if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        raise MissingURL()

    try:
        if sys.argv[2] == '-v':
            VERBOSE = True
        else:
            raise InvalidOption(sys.argv[2])
    except IndexError:
        pass

    input_parse(url)
