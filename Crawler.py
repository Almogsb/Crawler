
import time
import requests
from bs4 import BeautifulSoup


#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
#response = requests.get('https://coinmarketcap.com/', headers=headers)

my_session = requests.session()
for_cookies = my_session.get("https://coinmarketcap.com/")
cookies = for_cookies.cookies
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
my_url = 'https://coinmarketcap.com/all'

#check first if there is response from the server
#because there are a lot of blocks from this server
#i also put "sleep for 1" second to not get banned.
response = my_session.get(my_url, headers=headers, cookies=cookies)
print(response.status_code)

#from urllib.request import Request, urlopen
#req = Request('https://coinmarketcap.com/', headers=headers)
#webpage = urlopen(req).read()

def trade_spider(max_pages, choose, limit_price=3):
    page = 1
    while page <= int(max_pages):
        if page == 1:
            url = 'https://coinmarketcap.com/'
        else:
            url = 'https://coinmarketcap.com/' + str(page)
        source_code = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        plain_text = source_code.text.encode('ascii', 'replace')
        soup = BeautifulSoup(plain_text, 'html.parser')
        for link in soup.find_all('a', {'class': 'currency-name-container link-secondary'}):
            href = 'https://coinmarketcap.com' + str(link.get('href'))
            time.sleep(1)
            if choose == '1':
                get_single_item_data1(href)
            elif choose == '2':
                get_single_item_data2(href, limit_price)
            elif choose == '3':
                get_single_item_data3(href, limit_price)
        page += 1


def get_single_item_data1(item_url):
    save_file = open('MineableOnly.txt','a')
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for link in soup.find_all('span', {'class': 'label label-warning'}):
        name = link.string
        if name == 'Mineable':
            save_file.write(str(item_url) + "\n")
    save_file.close()


def get_single_item_data2(item_url, limit_price):
    save_file = open('LimitPrice.txt','a')
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for link in soup.find_all('span', {'id': 'quote_price'}):
        usd = float(link.get('data-usd'))
        if usd < float(limit_price):
            save_file.write(str(item_url) + "\n")
    save_file.close()

def get_single_item_data3(item_url, limit_price):
    save_file = open('LimitPriceJOINMinable.txt','a')
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for link in soup.find_all('span', {'class': 'label label-warning'}):
        name = link.string
        if name == 'Mineable':
            for link2 in soup.find_all('span', {'id': 'quote_price'}):
                usd = float(link2.get('data-usd'))
                if usd < float(limit_price):
                    save_file.write(str(item_url) + "\n")
    save_file.close()


pages = input('Choose number of pages to CRAWL: ')
choose = input('For mineables only            PRESS 1 \nFor limit price               PRESS 2 \nFor mineables and limit       PRESS 3\n')
limit_price = 0
if choose != '1':
    limit_price = float(input('Choose limit price: '))
trade_spider(pages, choose, limit_price)

