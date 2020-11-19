import os
import sys
import json
from check_urls import thread_urls_check


"""
Use check_urls.py with the partial .csv data of the NICathon domain's data.

Usage:
    - check_ar_csv.py | NUM THREAD_NUM
    Optional arguments:
        NUM -> Number of domains to check.
        THREAD_NUM -> Number of threads to use.
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

# Open domains
ALL_DOMAINS = open('data/csv_partial_nicathon.csv', 'r', encoding="utf8").read().split('\n')[
              1:]  # Take out initial line

# Open markers
try:
    MARKER = int(open('%s/check_ar_csv_marker' % OUTPUT_PATH, 'r').read())
except FileNotFoundError:
    open('check_ar_csv_marker', 'w').write('0')
    MARKER = 0


def nicathon_parse_csv(domains, p, n):
    """
    Parse a list of domains taken out of csv_partial_nicathon.csv into (url, registrar) pairs.

    :param domains: list, comma separated values of csv_partial_nicathon.csv file
    :param p: int, number of register to start from
    :param n: int, number of registers to take out
    :return: list of pairs: (url, registrar)
    """
    # Take url and registrar information out of next n domains, starting from register number p
    pairs = []
    for i in range(n):
        pairs.append(['http://' + domains[p + i].split(',')[1].replace('"', ''),
                      domains[p + i].split(',')[6].replace('"', '')])
    return pairs


# ENTRY POINT
if __name__ == '__main__':
    NUM, THREAD_NUM = 10, 10
    try:
        NUM = int(sys.argv[1])
        THREAD_NUM = int(sys.argv[2])
    except IndexError:
        pass

    thread_urls_check(nicathon_parse_csv(ALL_DOMAINS, MARKER, NUM), n_threads=THREAD_NUM,
                      filename='%s/check_ar_csv_output' % OUTPUT_PATH)

    MARKER += NUM
    open('%s/check_ar_csv_marker' % OUTPUT_PATH, 'w').write(str(MARKER))
