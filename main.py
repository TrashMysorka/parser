import requests
from bs4 import BeautifulSoup

URL = 'https://coinmarketcap.com/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.143 YaBrowser/22.5.0.1814 Yowser/2.5 Safari/537.36',
           'accept': '*/*'}


def get_html(url):
    r = requests.get(url=url, headers=HEADERS)
    return r


def get_content(html, currency_list):
    soup = BeautifulSoup(html, "html.parser")
    coins = soup.find("tbody").find_all("tr")

    for coin in coins:
        print(coin)
        name = coin.find(class_="cmc-link").get("href").replace("/currencies/", "")[:-1]
        price = coin.find(class_="sc-131di3y-0 cLgOOr").find('span')
        print(price)
        #price = price.get_text()
        market_cap = coin.find(class_="sc-1ow4cwt-1 ieFnWP")
        #market_cap = market_cap.get_text()
        if price:
            currency_list.append({
                'Name': name,
                'Price': price.text,
                'Market-Cap': market_cap.text
            })
        else:
            break
    print_list(currency_list)


def print_list(list):
    print('Name\t Price\t Market-Cap')
    for string in list:
        print(string['Name'] + ":  " + string['Price'] + "   " + string['Market-Cap'])


def parse(currency_list):
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text, currency_list)
    else:
        print("Something went wrong"
              "Traceback: parse()")


if __name__ == '__main__':
    currency_list = []
    parse(currency_list)

