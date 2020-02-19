from bs4 import BeautifulSoup as bs4
import requests
import sys
import random


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

print(user_agent())

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


try:
    for i in range(count):
        # Adding +1 to start from 1
        i+= 1
        headers = {
            'User-Agent': user_agent()
        }
        # Parsing URL for crawling authors
        req_url = url + '/?author=%d' % (i)
        # Making GET request
        r = requests.get(req_url, headers=headers)
        # Fetching page content
        soup = bs4(r.text, 'html.parser')
        # Finding error message for 404
        idenf= soup.findAll(text='Oops! That page can’t be found.')
        # Debug print
        print(idenf)
except KeyboardInterrupt:
    sys.exit()
except requests.exceptions.MissingSchema:
    print('[-] Please type url with http(s)!')
    sys.exit()
except:
    print('[-] Entered URL is invalid, please type valid url...')
    sys.exit()