import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://coinmarketcap.com/'


def get_html(url):
    browser = webdriver.Chrome()
    browser.get(url)

    return browser


def scroll(elem):
    for i in range(10):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)


def get_content(browser: webdriver, cur_list):
    close = browser.find_element(By.XPATH, value='//*[@id="cmc-cookie-policy-banner"]/div[2]')
    close.click()
    browser.maximize_window()
    coins = browser.find_element(by=By.TAG_NAME, value='body')
    scroll(coins)

    coins = browser.find_element(by=By.TAG_NAME, value='tbody')
    coins = coins.text.split('\n')
    iter = 1
    xpath = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[7]/div[1]/div/ul/li[10]/a'
    while True:
        time.sleep(0.5)
        if iter == 5:
            xpath = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[7]/div[1]/div/ul/li[11]/a'
        try:
            button = browser.find_element(by=By.XPATH,
                                          value=xpath)# browser.find_element(by=By.CLASS_NAME, value='chevron')

            button.click()
        except selenium.common.exceptions.NoSuchElementException:
            break
        next_coins = browser.find_element(by=By.TAG_NAME, value='body')
        scroll(next_coins)
        next_coins = browser.find_element(by=By.TAG_NAME, value='tbody')
        next_coins = next_coins.text.split('\n')
        for elem in next_coins:
            coins.append(elem)
        iter += 1
    i = 0
    while True:
        try:
            coins.remove('Buy')
        except ValueError:
            break
    print(coins)
    while i < 10045:
        i += 1
        try:
            name_index = coins.index(str(i)) + 1
            name = coins[name_index]

            price_index = coins.index(str(i)) + 3
            price = coins[price_index]

            market_cap_index = coins.index(str(i)) + 5
            market_cap = coins[market_cap_index]

            cur_list.append({
                'Name': name,
                'Price': price,
                'Market-Cap': market_cap,
            })
        except ValueError:
            continue


def write(cur_list):
    cur_list = pd.DataFrame(cur_list)
    #print(cur_list)
    cur_list.to_csv('result.csv')


def parse(cur_list):
    html = get_html(URL)
    get_content(html, cur_list)
    write(cur_list)


if __name__ == '__main__':
    currency_list = []
    parse(currency_list)
