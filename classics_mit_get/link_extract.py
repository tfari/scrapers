import sys
from bs4 import BeautifulSoup


# v 0.1


DICT_TYPES = {'a': 'href', 'area': 'href', 'base': 'href', 'blockquote': 'cite', 'button': 'formaction', 'embed': 'src',
              'form': 'action', 'frame': 'src', 'head': 'profile', 'html': 'xmlns', 'iframe': 'src', 'img': 'src',
              'input': 'formaction', 'ins': 'cite', 'source': 'src', 'link': 'href', 'q': 'cite', 'script': 'src',
              'track': 'src', 'video': 'src', 'object': 'data', 'meta': 'content'}


"""
link_extract extracts link fields from the tags specified. 
Terminal Usage:
    python link_extract.py URL TYPES |  -a
    URL => URL to extract the links from
    TYPES => string or strings of DICT_TYPES. If no types are specified, and -a is not used, it defaults to <a>.
                ['a', 'area', 'base', 'blockquote', 'button', 'embed', 'form', 'frame', 'head', 'html', 'iframe', 
                'img', 'input', 'ins', 'source', 'link', 'q', 'script', 'track', 'video', 'object']
    -a => Use instead of writing any types, checks for all DICT_TYPES
    
     python link_extract.py http://google.com -a
     python link_extract.py http://google.com
     python link_extract.py http://google.com a img script link video
     
"""


def link_extract(http_response, types=[], verbose=False, all=False):
    """
    Function to extract links from specified html tags.

    Raises BadType

    :param http_response: string, html document
    :param types: list of strings, correspond to keys in DICT_TYPES, represent html tags.
                  If types is not provided <a> is used.
    :param verbose: bool, if True result is also printed to the screen
    :param all: bool, if True all types in DICT_TYPES are checked for
    :return: list of strings, the extracted links
    """
    def _get_list(bs, first_var, second_var):
        """
        Helper function that searches the BeautifulSoup object for the second_var field of all first_var tags.

        :param bs: BeautifulSoup object
        :param first_var: string, tag name
        :param second_var: string, field name
        :return: list of strings, the extracted fields
        """
        return [i.get(second_var) for i in bs.find_all(first_var) if i.get(second_var) is not None]

    # CONTROL FOR EMPTY TYPES LIST OR ALL=TRUE OPTION
    if all:
        types = []  # <-
        for key in DICT_TYPES.keys():
            types.append(key)

    elif len(types) < 1:
        types.append('a')

    # VALIDATE TYPES LIST
    for type_elem in types:
        if type_elem not in DICT_TYPES.keys():
            raise BadType(type_elem)

    #

    if verbose:
        print("[*] Extracting the following types : %s " % (', '.join(types)))

    soup = BeautifulSoup(http_response.encode('utf-8'), 'html.parser')

    # EXTRACT LINKS
    extracted = []
    for type_elem in types:
        r_list = _get_list(soup, type_elem, DICT_TYPES[type_elem])
        extracted += r_list

        if verbose:
            print("[*][*] Extracted by type, keyword : '%s', '%s'" % (type_elem, DICT_TYPES[type_elem]))
            print('\n'.join(_get_list(soup, type_elem, DICT_TYPES[type_elem])))
            print("\n %s \n" % ("#" * 80))

    return extracted


# EXCEPTIONS

class LinkExtractError(Exception):
    pass


class BadType(LinkExtractError):
    pass


class NoUrl(LinkExtractError):
    pass


# TERMINAL ENTRY POINT

if __name__ == '__main__':
    from req_handler import GET, RequestData, RequestErrorData, RequestHandler

    # CHECK FOR -a OPTION
    all_args = False
    for arg in sys.argv:
        if arg == '-a':
            all_args = True

    try:
        print("[*] Requesting %s" % (sys.argv[1]))
        rh = RequestHandler([sys.argv[1]], RequestData(GET), RequestErrorData())
        rh.run()
        x = rh.responses[0]
        link_extract(x.text, types=sys.argv[2:], verbose=True, all=all_args)

    except IndexError:
        raise NoUrl()
