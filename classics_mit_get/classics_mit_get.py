import os
import json
from req_handler import GET, RequestData, RequestErrorData, RequestHandler, ThreadedRequestHandler
from link_extract import link_extract

"""
Script for getting all available .txt versions of the classics on The Internet Classics Archive
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

INVALID_FILENAME_CHARS = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.', '\n', '\r', '\t']

# Extract authors urls
base_url = 'http://classics.mit.edu/Browse/index.html'
rh = RequestHandler([base_url], RequestData(GET), RequestErrorData(allow_errors=False))
rh.run()
extracted_links = link_extract(rh.responses[0].text)
extracted_authors = ['http://classics.mit.edu/Browse/' + link for link in extracted_links if link.find('browse') != -1]


# Extract book list urls for each author
th = ThreadedRequestHandler(extracted_authors, RequestData(GET), RequestErrorData(expected_error_str='Server Error'),
                            thread_num=10)
th.do_threads()

book_url_list = []
for response in th.responses:
    author = response.url.split('-')[1].replace('.html', '')
    extracted_links = link_extract(response.text)
    extracted_books = ['http://classics.mit.edu' + link for link in
                       extracted_links if link.find('/' + author + '/') != -1]
    book_url_list += extracted_books

# Extract .txt files urls
th = ThreadedRequestHandler(book_url_list, RequestData(GET), RequestErrorData(expected_error_str='Perseus'),
                            thread_num=10)
th.do_threads()

txt_files_list = []
for response in th.responses:
    author = response.url.split('/')[3]
    extracted_links = link_extract(response.text)
    extracted_file_url = [link for link in extracted_links if link.find('.txt') != -1]
    if len(extracted_file_url) > 1 or len(extracted_file_url) < 1:
        print("[!!!] -> ", author, extracted_file_url, response.url)
    else:
        txt_files_list.append(str('http://classics.mit.edu/' + author + '/' + extracted_file_url[0]))

# Get .txt files
th = ThreadedRequestHandler(txt_files_list, RequestData(GET), RequestErrorData(), thread_num=10)
th.do_threads()

for response in th.responses:
    author = response.url.split('/')[3]

    # GET TITLE FROM WITHIN THE FILE
    response_split = response.text.split('\n')
    count = 0
    for line in response_split:
        if line.find('By ') != -1:
            break
        count += 1

    book_name = response_split[count - 1]

    for i in INVALID_FILENAME_CHARS:
        book_name = book_name.replace(i, '')

    filename = '%s/%s - %s.txt' % (OUTPUT_PATH, author, book_name)
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(response.text)


print('[*] ', len(th.responses), ' saved classics.')
