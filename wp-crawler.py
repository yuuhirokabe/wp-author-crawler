from bs4 import BeautifulSoup as bs4
import requests
import sys, os
import random
from colored import fg, attr
from time import time

# Clearing...
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
print(r"""
%snezuko%s@%skamado%s%s~%s > ./wp-crawler.py

                            o       o o--o        o-o o--o    O  o       o o    o--o o--o  
                            |       | |   |      /    |   |  / \ |       | |    |    |   | 
                            o   o   o O--o  o-o O     O-Oo  o---oo   o   o |    O-o  O-Oo  
                             \ / \ /  |          \    |  \  |   | \ / \ /  |    |    |  \  
                              o   o   o           o-o o   o o   o  o   o   O---oo--o o   o     
                            
                             ./Author Yuu Hirokabe
                             ./Facebook https://facebook.com/yuuhirokabe
                             ./Twitter  https://twitter.com/yuuhirokabe
                             ./Version 1.0.0
""" % ((fg(108), attr('reset'), fg(68), attr('reset'), fg(9), attr('reset'))))

# Setting variables
user_count   = 0 # Active Users
broken_count = 0 # Broken Users

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
    # Randomizing User Agent
    i = random.randrange(0, len(agents))
    # Returning random generated User Agent
    return agents[i]

# Requesting user to input website url to crawl
try:
    url = input('Type website url to crawl: ')
# If user pressed CTRL + C or CTRL + Z
except KeyboardInterrupt:
    # Stopping script
    sys.exit()

# Requesting user to input how many users want to crawl
try:
    count = int(input('How many users you want to crawl? '))
# If user pressed CTRL + C or CTRL + Z
except KeyboardInterrupt:
    sys.exit()
# If typed value is not integer
except ValueError:
    # Printing message
    print('%s[-] Please type an integer!%s' % (fg(1), attr('reset')))
    # Stopping script
    sys.exit()

# Start crawling page
try:
    # Counting time
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
        req_url = url + '/?author=%d' % i
        # Making GET request
        r = requests.get(req_url, headers=headers, proxies=proxies)
        # Fetching page content
        soup = bs4(r.text, 'html.parser')
        # Finding error message for 404
        found = soup.find('body', attrs={'class':'author'})
        if found != None:
            # Checking if have redirect
            if r.history:
                # Counting found users
                user_count = user_count + 1
                # Getting author name from url - http://website.com/author/name
                name = r.url.split('/')[4]
                # Printing message
                print(f'%s[+] Found user {name} with id {i}, url: {r.url}%s' % (fg(2), attr('reset')))
            else:
                # Counting broken users
                broken_count = broken_count + 1
                # Printing message
                print(f'%s[/] Found broken user with id {i}, url: {r.url}%s' % (fg(3), attr('reset')))
        else:
            print(f'%s[-] User with id {i} not found...%s' % (fg(1), attr('reset')))
    # Finish time
    finish = time() - start
    # Calculating minutes
    minutes = round(finish / 60)
    # Calculating seconds
    seconds = round(finish % 60)
    # Printing elapsed time
    print(f'{minutes} min. {seconds} sec. elapsed, found {user_count} users, {broken_count} broken users')

# If user pressed CTRL + C or CTRL + Z
except KeyboardInterrupt:
    # Stopping script
    sys.exit()

# If user don't know how to type url with http(s)://
except requests.exceptions.MissingSchema:
    # Printing message
    print('%s[-] Please type url with http(s)!%s' % (fg(1), attr('reset')))
    # Stopping script
    sys.exit()