import os
import sys
import json
import threading
from bs4 import BeautifulSoup

from req_handler import GET, POST, RequestData, RequestErrorData, RequestHandler, InvalidStatusCode, ConnectivityError

"""
Bulk download oeis.org sequences as midi files.

Raises MissingArguments and MinRangeBiggerThanMaxRange

Terminal Usage:
    python oeis_md.py RANGE_MIN RANGE_MAX THREAD_NUM | BPM | LENGTH
    RANGE_MIN => integer
    RANGE_MAX => integer
    THREAD_NUM => integer
    BPM => optional integer, default is 100
    LENGTH => optional integer representing bar length of midi file, default value is 4096

    python oeis_md.py 0 100 10 100 16
    python oeis_md.py 0 1 1 100
    python oeis_md.py 23 240 20
"""

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

INVALID_FILENAME_CHARS = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.']


def make_seq_index(num):
    """
    Format any number as oeis id.

    :param num: integer
    :return: string representation of num, of format A000000
    """

    return 'A%s' % '{:0>6d}'.format(num)


def get_name(seq_index):
    """
    Gets the name of sequence of id seq_index.

    If the HTTP request fails, an error is printed to STDOUT and the function returns an empty string.

    :param seq_index: string, sequence id
    :return: string, sanitized sequence name
    """

    url = 'https://oeis.org/search?q=id:%s&fmt=text' % seq_index

    # GET
    try:
        rh = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False, expected_status_codes=[200]))
        rh.run()
        req = rh.responses[0]

        soup = BeautifulSoup(req.text, 'html.parser')
        soup_text = soup.text

    except InvalidStatusCode as e:
        print("[!] %s failed at get_name" % e.args)
        soup_text = ''

    # EXTRACT NAME
    name = ''
    for line in soup_text.split('\n'):
        if line.find('%N') != -1:
            name = (' '.join(line.split(' ')[2:]))

    # SANITIZE NAME FOR FILENAME USAGE
    seq_name = name[:name.find('.')] if name.find('.') != -1 else name
    seq_name = seq_name[:seq_name.find(';')] if seq_name.find(';') != -1 else seq_name

    for i in INVALID_FILENAME_CHARS:
        seq_name = seq_name.replace(i, '')

    return seq_name[:50]


def get_midi(seq_name, seq_index, bpm, length):
    """
    Gets the midi file associated with sequence of id seq_index.

    If the HTTP request fails an error is printed to STDOUT and the function passes silently.

    :param seq_name: string, sequence name
    :param seq_index: string, sequence id
    :param bpm: integer
    :param length: integer, number of bars
    :return: None
    """

    post_payload = {'midi': '1', 'seq': seq_index, 'bpm': bpm, 'vol': '100', 'voice': '1', 'velon': '80',
                    'veloff': '80', 'pmod': '88', 'poff': '20', 'dmod': '1', 'doff': '0', 'cutoff': length,
                    'SAVE': 'SAVE'}

    url = 'https://oeis.org/play'

    try:
        rh = RequestHandler([url], RequestData(POST, data=post_payload), RequestErrorData(allow_errors=False,
                                                                                          expected_status_codes=[200]))
        rh.run()
        midi_file = rh.responses[0]

        with open('%s/%s - %sbpms - %s - %s.mid' % (OUTPUT_PATH, seq_index, bpm, length, seq_name), 'wb') as f:
            f.write(midi_file.content)

    except InvalidStatusCode as e:
        print("[!] %s failed at get_midi with code %s" % e.args)


def bulk_get(range_min, range_max, bpm, length):
    """
    Gets sequence id, sequence name, and downloads the corresponding midi file of a range of sequences defined by
    range_min and range_min.

    :param range_min: integer
    :param range_max: integer
    :param bpm: integer
    :param length: integer
    :return: None
    """

    for i in range(range_min, range_max):
        seq_index = make_seq_index(i)
        seq_name = get_name(seq_index)
        get_midi(seq_name, seq_index, bpm, length)


def main(range_min, range_max, num_thread, bpm, length):
    """
    Divides a range of sequences we want to download into num_thread threads.

    :param range_min: integer
    :param range_max: integer
    :param bpm: integer
    :param length: integer
    :param num_thread: integer
    :return: None
    """

    num_thread = 1 if num_thread == 0 else num_thread  # Forces no 0 num_thread.
    range_min = 1 if range_min == 0 else range_min  # Forces no 0 start.
    range_max += 1  # Forces inclusive range_max.

    range_per_thread = int((range_max - range_min) / num_thread)

    for i in range(0, num_thread):
        th_min_range = range_min + (i * range_per_thread)
        th_max_range = th_min_range + range_per_thread

        t = threading.Thread(target=bulk_get, args=(th_min_range, th_max_range, bpm, length))
        t.start()

    # TAKES CARE OF REMAINDER RANGE
    if th_max_range < range_max:
        t = threading.Thread(target=bulk_get, args=(th_max_range, range_max, bpm, length))
        t.start()

# EXCEPTIONS


class OeisMidiError(Exception):
    pass


class MissingArguments(OeisMidiError):
    pass


class MinRangeBiggerThanMaxRange(OeisMidiError):
    pass


# TERMINAL ENTRY POINT

if __name__ == '__main__':
    # SET DEFAULTS
    r_min, r_max, n_th, bpms, seq_len = 0, 1, 1, 100, 4096

    # NON_OPTIONAL ARGUMENTS
    try:
        r_min = int(sys.argv[1])
        r_max = int(sys.argv[2])
        n_th = int(sys.argv[3])
    except IndexError:
        raise MissingArguments(sys.argv[1:])

    # OPTIONAL ARGUMENTS
    try:
        bpms = int(sys.argv[4])
        seq_len = int(sys.argv[5])
    except IndexError:
        pass

    # BASIC CHECK
    if r_min > r_max:
        raise MinRangeBiggerThanMaxRange()

    main(r_min, r_max, n_th, bpms, seq_len)
