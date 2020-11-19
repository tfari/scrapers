import time
import threading
import requests
from bs4 import BeautifulSoup
import timeout_builtwith
from helpers.excel_writer import ExcelWriter

"""
Filter and extract some basic information of a list of domains.

Down domains are filtered out of the result lists.

We want to save the following data:
    * Status code of domain GET call
    * Url of the domain
    * Registrar
    * Redirected URL
    * Title of the page
    * Data acquired via the builtwith module

Results are saved in .xlsx format.
"""


class LockedResultList(object):
    """
    Class for aggregating the results of the different threads, uses Lock() to prevent racing.
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.result_list = []

    def append(self, data_set):
        with self.lock:
            self.result_list.append(data_set)


class ResponseObject(object):
    """
    Class for fixing the builtwith bottleneck issue, we use this object to hold the response of the returning thread
    and secure it with Lock()
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.result = None

    def set_result(self, result):
        with self.lock:
            self.result = result

    def get_result(self):
        with self.lock:
            return self.result


def scrap_single_domain(url, registrar, callback, builtwith_timeout=360):
    """
    Scraps the data_set for a single domain.

    :param url: str, url of the domain
    :param registrar: str, registrar of the domain
    :param callback: LockedResultList instance
    :param builtwith_timeout: timeout for the builtwith calls, default is 6 minutes
    :return: True if success, False if not
    """

    #

    # Fill default data_set information
    data_set = {'status_code': 0,
                'base_url': url,
                'registrar': registrar,
                'redirected_url': '',
                'page_title': '',
                'built_with': ''}

    # Get domain response
    try:
        r = requests.get(url, timeout=5)
        data_set['status_code'] = r.status_code
        data_set['redirected_url'] = r.url
    # Handle requests Exceptions
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False
    except Exception as e:
        print("[!] REQUEST ERROR => %s" % e.__repr__())
        return False

    # Parse response title
    bs_title = BeautifulSoup(r.text, 'html.parser').title
    if bs_title:
        data_set['page_title'] = str(bs_title.string).encode('utf-8')

    # Get builtwith data
    if r.status_code < 400 or r.status_code > 600:  # builtwith returns an empty dict when its an HTTP error
        try:

            start_time = time.time()
            built_with_data = timeout_builtwith.builtwith(url, headers=r.headers, html=str(r.text).encode('utf-8'),
                                                          timeout=builtwith_timeout)
            end_time = time.time() - start_time
            print("[*] %s : %s" % (url, end_time))

            if built_with_data is False:
                print("[!] Time Out > %s" % url)
            elif built_with_data:
                data_set['built_with'] = str(built_with_data)

        except UnicodeDecodeError:
            print("[!] BUILT_WITH UNICODE ERROR AT => %s" % url)

    # Append data_set to callback
    callback.append(data_set)
    return True


def bulk_urls_check(urls_registrar_list, callback):
    """
    Thread target function for using a list of (url, registrar) pairs to call scrap_single_domain() with.

    :param urls_registrar_list: list of pairs: (url, registrar)
    :param callback: LockedResultList instance
    :return: None
    """
    for pair in urls_registrar_list:
        scrap_single_domain(pair[0], pair[1], callback)


def thread_urls_check(urls_registrar_pairs, n_threads=100, filename='output'):
    """
    Separate list of urls into threads, start them, wait for them to finish, and then sort and write data into an excel
    file

    :param urls_registrar_pairs: list of pairs: (url, registrar)
    :param n_threads: int, number of threads, 100 by default
    :param filename: str, name of the file to output results to, 'output' by default
    :return: None
    """
    start_time = time.time()
    locked_results = LockedResultList()
    excel_writer = ExcelWriter(filename, ['status_code', 'base_url', 'registrar', 'redirected_url', 'page_title',
                                          'built_with'])

    # Populate n_threads lists with urls_registrar_pairs
    urls_sub_lists = [[] for _ in range(n_threads)]
    count = 0
    for pair in urls_registrar_pairs:
        urls_sub_lists[count % n_threads].append(pair)
        count += 1

    # Create threads
    threads = []
    for i in range(n_threads):
        threads.append(threading.Thread(target=bulk_urls_check, args=(urls_sub_lists[i], locked_results)))

    # Start threads and join them
    print("[*] Starting GET of %s urls divided in %s threads  (this might take a while depending on the domains)" %
          (len(urls_registrar_pairs), n_threads))

    [t.start() for t in threads]
    [t.join() for t in threads]
    print("[*] Finish GET")

    # Add data_set into excel_writer, sort, and write
    print("[*] Writing %s results into %s" % (len(locked_results.result_list), excel_writer.filename))
    for result in locked_results.result_list:
        excel_writer.add(result)
    excel_writer.order_by('status_code')
    excel_writer.write()
    print('[*] GET took ', time.time() - start_time, ' seconds.')
