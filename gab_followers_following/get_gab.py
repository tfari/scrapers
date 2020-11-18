import os
import sys
import time
import json

start = time.time()

from req_handler import GET, RequestData, RequestErrorData, RequestHandler, ThreadedRequestHandler
from excel_writer import ExcelWriter

"""
Creates an .xlsx file of a followers or following list of a gab.ai user.

Raises MissingUsername and BadModeArgument.

Running the same request more than once will result in the request being appended to the end of the existing file, 
it won't "step" over it.

Terminal Usage:
	python get_gab.py USERNAME | MODE | ORDER_HEADER | NUM_THREADS | MAX_PASSES | SLEEP_PASS
	
	USERNAME => string, valid gab username
	
	MODE => optional string, either 'followers' or 'following'
			"followers" by default.
			
	ORDER_HEADER => optional string, has to be one of the TABLE_HEADERS.
				"bio" by default.
				
				['id', 'created_at_month_label', 'name', 'username', 'follower_count', 'following_count', 'post_count',
				 'verified', 'is_pro', 'is_donor', 'is_investor', 'is_premium', 'is_tippable', 'is_private', 'bio',
				 'cover_url', 'picture_url', 'picture_url_full', 'following', 'followed', 'is_accessible',
				 'follow_pending']
	
	NUM_THREADS =>  number of threads.
					10 by default.
	
	MAX_PASSES => number of passes over the urls before accepting errors (used to account for HTTP's error code 429)
					20 by default.
	
	SLEEP_PASS => number of seconds to sleep between passes
					5 by default.
						
	python get_gab.py MyUser
	python get_gab.py MyUser following
	python get_gab.py MyUser followers name
	python get_gab.py MyUser followers verified
	python get_gab.py MyUser followers bio 200
	python get_gab.py MyUser followers bio 200 10
	python get_gab.py MyUser following following 200 10 2

"""

FOLLOWERS = 'followers'
FOLLOWING = 'following'

TABLE_HEADERS = ['id', 'created_at_month_label', 'name', 'username', 'follower_count', 'following_count', 'post_count',
                 'verified', 'is_pro', 'is_donor', 'is_investor', 'is_premium', 'is_tippable', 'is_private', 'bio',
                 'cover_url', 'picture_url', 'picture_url_full', 'following', 'followed', 'is_accessible',
                 'follow_pending']

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


def get_info(username, mode, order_header, thread_num, max_passes, sleep_pass):
    """
	Produces an excel comprised of either the followers or the following lists (depending on mode) of gab user
	username, ordered by order_header.

	Raises BadOrderHeader if order_header isn't a header specified in TABLE_HEADERS. By default its ordered by the 'bio'
	field.

	:param username: string
	:param mode: string, FOLLOWERS or FOLLOWING
	:param order_header: string, one of the TABLE_HEADERS
	:param thread_num: integer, number of threads to use
	:return: None
	"""
    xlw = ExcelWriter(('%s/%s_%s' % (OUTPUT_PATH, username, mode)), TABLE_HEADERS)

    # Checking of order_header
    if order_header not in TABLE_HEADERS:
        raise BadOrderHeader(order_header)

    # Get follower count
    url = 'https://gab.ai/users/%s' % username
    req_handler = RequestHandler([url], RequestData(GET), RequestErrorData(allow_errors=False))
    req_handler.run()
    response_object = req_handler.responses[0]
    json = response_object.json()
    count = json['follower_count'] if mode == FOLLOWERS else json['following_count']
    print("[*] %s links for %s" % (count / 30, username))

    # Make all urls
    urls = [('https://gab.ai/users/%s/%s?before=%s' % (username, mode, str(i))) for i in range(0, count, 30)]

    # Perform bulk requests
    req_pool = ThreadedRequestHandler(urls, RequestData(GET), RequestErrorData(), thread_num=thread_num,
                                      max_passes=max_passes, sleep_pass=sleep_pass)
    req_pool.do_threads()
    responses = req_pool.responses
    errors = req_pool.errors

    # Extract data from response_list and store in ExcelWriter
    print('Responses: ', len(responses))
    print('Errors: ', len(errors), errors[:5])
    unique_entries = 0

    for response in responses:
        json = response.json()
        unique_entries += len(json['data'])
        for j in json['data']:
            xlw.add(j)

    print('Unique entries: ', unique_entries)

    # Sort and save data stored in ExcelWriter
    xlw.order_by(order_header)
    xlw.write()


# EXCEPTIONS


class GetGabError(Exception):
    pass


class MissingUsername(GetGabError):
    pass


class BadModeArgument(GetGabError):
    pass


class BadOrderHeader(GetGabError):
    pass


# TERMINAL ENTRY POINT

if __name__ == '__main__':

    # Set default values
    un, fm, oh, tn, mp, sp = '', FOLLOWERS, 'bio', 10, 20, 5

    # Check username is there
    try:
        un = sys.argv[1]
    except IndexError:
        raise MissingUsername()

    # Check optionals
    try:
        fm = sys.argv[2]
        # Argument 2 MUST be either FOLLOWERS or FOLLOWING
        if fm != FOLLOWERS and fm != FOLLOWING:
            raise BadModeArgument(fm)

        oh = sys.argv[3]
        tn = int(sys.argv[4])
        mp = int(sys.argv[5])
        sp = int(sys.argv[6])
    except IndexError:
        pass

    get_info(un, fm, oh, tn, mp, sp)

end = time.time()

print(end - start)
