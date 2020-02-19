from bs4 import BeautifulSoup as bs4
import requests
import sys
import random
from colored import fg, attr
from time import time


# Setting variables
users = 0 # Active Users
broken = 0 # Broken Users

# Randomizing User-Agent's
def user_agent():
    agents = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3833.101 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3833.141 Safari/537.36',
        'Mozilla/5.0 (X11; Gentoo; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.143 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    ]
    i = random.randrange(0, len(agents))
    return agents[i]

# Requesting user to input website url to crawl
try:
    url = input('Type website url to crawl: ')
except KeyboardInterrupt:
    sys.exit()

# Requesting user to input how many users want to crawl
try:
    count = int(input('How many users you want to crawl? '))
except KeyboardInterrupt:
    sys.exit()
except ValueError:
    print('[-] Please type an integer!')
    sys.exit()

# Start crawling page
try:
    start = time()
    for i in range(count):
        # Adding +1 to start from 1
        i+= 1
        headers = {
            'User-Agent': user_agent()
        }
        # Setting proxy
        proxies = {
            'http':'socks5h://127.0.0.1:9050',
            'https':'socks5h://127.0.0.1:9050'
        }
        # Parsing URL for crawling authors
        req_url = url + '/?author=%d' % (i)
        # Making GET request
        r = requests.get(req_url, headers=headers, proxies=proxies)
        # Fetching page content
        soup = bs4(r.text, 'html.parser')
        # Finding error message for 404
        found = soup.find('body', attrs={'class':'author'})
        if found != None:
            if r.history:
                users = users + 1
                name = r.url.split('/')[4]
                print(f'%s[+] Found user {name} with id {i}, url: {r.url}%s' % (fg(2), attr('reset')))
            else:
                broken = broken + 1
                print(f'%s[/] Found broken user with id {i}, url: {r.url}%s' % (fg(3), attr('reset')))
        else:
            print(f'%s[-] User with id {i} not found...%s' % (fg(1), attr('reset')))
    finish = time() - start
    minutes = round(finish / 60)
    seconds = round(finish % 60)
    print(f'{minutes} min. {seconds} sec. elapsed, found {users} users')
except KeyboardInterrupt:
    sys.exit()
except requests.exceptions.MissingSchema:
    print('[-] Please type url with http(s)!')
    sys.exit()