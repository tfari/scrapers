import requests
import json
import os
import sys

from helpers.bc_helpers import is_valid_bandcamp_url, is_valid_username, get_all_info, get_album_info, get_track_info
from helpers.file_getter import get_file
from helpers.id3_wrapper import mp3_tag_file
from helpers.input_wrapper import input_wrapper
from helpers.tk_notify import NOTIFYSERVER

"""
Downloads Bandcamp tracks as .mp3. 

Usage:
    python bc_get.py URL | -v
    URL: A Bandcamp url
    -v (OPTIONAL): Verbose output
"""

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


#######################################################################################################################
#######################################################################################################################

def get_everything(all_albums_data, all_tracks_data):
    """
    Calls GET on every album and track of the user

    :param all_tracks_data: list of dicts
    :param all_albums_data: list of dicts
    :return: None
    """

    get_all_albums(all_albums_data)

    if all_tracks_data:
        # Gets artist artwork
        if all_tracks_data[0]['artist_avatar']:
            url = 'https://f4.bcbits.com/img/' + all_tracks_data[0]['artist_avatar'] + '_10.jpg'
            artist_cover = requests.get(url).content
        else:
            artist_cover = None

        get_all_tracks(all_tracks_data[0]['artist'], 'Tracks', all_tracks_data, album_release=None,
                       album_cover=artist_cover, artist_cover=artist_cover)


def get_all_albums(all_albums_data, artist_cover=None):
    """
    Calls GET on every album in all_albums_data

    :param all_albums_data: list of dicts
    :param artist_cover: file
    :return: None
    """
    for album_data in all_albums_data:
        get_specific_album(album_data, artist_cover)


def get_specific_album(playlist_data, artist_cover=None):
    """
    Calls get_all_tracks() on playlist_data track list

    :param playlist_data: dict
    :param artist_cover: file
    :return: None
    """
    # Get every track inside the playlist
    print(playlist_data)
    if playlist_data['track_info']:

        # Get the album cover
        if playlist_data['album_cover']:
            url = 'https://f4.bcbits.com/img/a' + playlist_data['album_cover'] + '_16.jpg'
            album_cover = requests.get(url).content
        else:
            album_cover = None

        get_all_tracks(playlist_data['artist'], playlist_data['album_title'], playlist_data['track_info'],
                       album_release=playlist_data['album_release'], album_cover=album_cover, artist_cover=artist_cover)

    else:  # If the playlist is empty, its blocked for our area or for non logged-in users
        if VERBOSE:
            print("[!] Blocked playlist: '%s'" % playlist_data['title'])


def get_all_tracks(username, playlist_title, track_collection_data, album_release=None, album_cover=None,
                   artist_cover=None):
    """
    Calls GET on every track on a list of them

    :param username: str
    :param playlist_title: str
    :param track_collection_data: list of dicts
    :param album_release: str
    :param album_cover: file
    :param artist_cover: file
    :return: None
    """

    # Iterate over the track list and if the track has not been already downloaded, call GET on it and increase count
    count = 1
    for track_data in track_collection_data:

        try:  # Ugly solution to work both with get_everything() and input_parse() / get_specific_playlist() calls
            track_data['track_id']
        except KeyError:
            track_data = track_data['track_info']

        if track_data['track_id'] not in DOWNLOADED:
            get_specific_track(username, playlist_title, track_data['title'], track_data['id'],
                               track_data['file']['mp3-128'], track_cover_url=None, album_release=album_release,
                               track_count=count, album_cover=album_cover, artist_cover=artist_cover)

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


def get_specific_track(username, playlist_title, track_title, track_id, track_url, track_cover_url=None,
                       album_release=None, track_count=0, album_cover=None, artist_cover=None):
    """
    Creates the output directory, downloads the track, and edits its mp3 tags.

    :param username: str
    :param playlist_title: str
    :param track_title: str
    :param track_id: str
    :param track_url: str
    :param track_cover_url: str
    :param album_release: str
    :param track_count: int
    :param album_cover: file
    :param artist_cover: file
    :return: None
    """
    # Sanitize filename
    for invalid in INVALID_FILENAME_CHARS:
        username = username.replace(invalid, '')
        playlist_title = playlist_title.replace(invalid, '')
        track_title = track_title.replace(invalid, '')

    # Create output folder if it doesn't exist
    _path_check(username + '/' + '[BC] ' + playlist_title)

    # Create filename
    filename = OUTPUT_PATH + '/' + username + '/' + '[BC] ' + playlist_title + '/' + track_title + '.mp3'

    # Downloads and edits
    try:  # If file already exits:
        x = open(filename, 'r')
        x.close()
        if VERBOSE:
            print("[!] File already exists: %s" % track_title)

    except FileNotFoundError:  # If not
        # Get track artwork
        if track_cover_url:
            url = 'https://f4.bcbits.com/img/a' + track_cover_url + '_16.jpg'
            track_cover = requests.get(url).content
        else:
            track_cover = None

        # Download
        get_file('[%s]' % track_title, track_url, filename)

        # Edit the tags of the track to match the track_data
        mp3_tag_file(filename, username, track_title, track_count=track_count, album_artist=username,
                     album_title=playlist_title, album_release=album_release, album_cover=album_cover,
                     artist_cover=artist_cover, track_cover=track_cover)

    # Append track to DOWNLOADED list (We do it here to keep track of previously downloaded tracks too.)
    DOWNLOADED.append(track_id)


#######################################################################################################################
#######################################################################################################################


def input_parse(input_url):
    """
    Parses an input url and calls the corresponding function

    :param input_url: str, a Bandcamp url called to be downloaded
    :return: None
    """
    #  TODO: Return list of downloaded stuff

    # Urls with no http/https break requests module, ones with it difficult parsing. Fix that:
    input_url = input_url.replace('https://', '').replace('http://', '')
    full_url = 'https://%s' % input_url

    # Split the input so we can reason about it
    first_split = input_url.split('.')

    # Check for correct URL length
    if len(first_split) != 3:
        raise InvalidUrl(input_url)

    # Check for bandcamp and com
    if first_split[1] != 'bandcamp' or first_split[2].split('/')[0] != 'com':
        raise InvalidUrl(input_url)

    # Grab username
    username = first_split[0]
    if not is_valid_username(username):
        raise InvalidUsername(username)

    # Grab url kind
    second_split = first_split[2].split('/')

    # Parse
    if len(second_split) < 3:  # Normal URL or /music URL
        if len(second_split) == 2 and second_split[1] != 'music':
            raise InvalidUrl(input_url)

        # Get everything
        all_urls = get_all_info(username)
        print("[*] Getting information on %s elements " % len(all_urls))
        all_albums_data = [get_album_info(username, url) for url in all_urls if url.find('/album/') != -1]
        all_tracks_data = [get_track_info(username, url) for url in all_urls if url.find('/track/') != -1]
        all_tracks_data.reverse()  # So new orphan tracks(singles) will always be on the bottom of the playlist

        get_everything(all_albums_data, all_tracks_data)

    elif len(second_split) == 3:  # /track or /album URL
        if second_split[1] == 'track':  # Get track
            if not is_valid_bandcamp_url(full_url):
                raise InvalidTrackUrl(full_url)

            track_info = get_track_info(username, '/track/' + second_split[2])

            # If there is an album_url, ask user if he would rather download the entire album the track belongs to
            if track_info['album_url']:
                print(track_info['track_info']['title'] + ' belongs to an album.')
                answer = input_wrapper('Would you rather download the entire album instead?', ('yes', 'no'))
                if answer == 'no':
                    get_specific_track(track_info['artist'], 'Tracks', track_info['track_info']['title'],
                                       track_info['track_info']['track_id'],
                                       track_info['track_info']['file']['mp3-128'], track_info['album_cover'])
                else:
                    get_specific_album(get_album_info(username, track_info['album_url']))

            else:
                get_specific_track(track_info['artist'], 'Tracks', track_info['track_info']['title'],
                                   track_info['track_info']['track_id'],
                                   track_info['track_info']['file']['mp3-128'], track_info['album_cover'])

        elif second_split[1] == 'album':  # Get album
            if not is_valid_bandcamp_url(full_url):
                raise InvalidAlbumUrl(full_url)

            get_specific_album(get_album_info(username, '/album/' + second_split[2]))
        else:
            raise InvalidUrl(input_url)


# Exceptions


class GetBCTrackError(Exception):
    pass


class MissingURL(GetBCTrackError):
    pass


class InvalidOption(GetBCTrackError):
    pass


class InvalidUrl(GetBCTrackError):
    pass


class InvalidUsername(GetBCTrackError):
    pass


class InvalidTrackUrl(GetBCTrackError):
    pass


class InvalidAlbumUrl(GetBCTrackError):
    pass


# Entry point


if __name__ == '__main__':
    try:
        bc_url = sys.argv[1]
    except IndexError:
        raise MissingURL()

    try:
        if sys.argv[2] == '-v':
            VERBOSE = True
        else:
            raise InvalidOption(sys.argv[2])
    except IndexError:
        pass

    input_parse(bc_url)
    NOTIFYSERVER.notify('Download finished.', 'bc_get')  # TODO -> Make it optional
