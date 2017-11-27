# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
import requests
import re

products = {}
req_head = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}
url = "https://www.utkonos.ru"

def ProdAdd(goods_view_box):
    global products
    for prod in goods_view_box:
        prod_name = prod.find('div', class_='goods_view_box-caption').get_text()
        try:
            prod_price = float(str(prod.find('div', class_='goods_price-item current').get_text()).replace(' ', '').replace(',', '.'))
        except AttributeError:
            prod_price = [0,0]
        products.update({prod_name: prod_price})

def GetQuery(message):
    global url, req_head, products
    products = {}
    page = requests.get(url + '/search?query={}'.format(message), headers=req_head)
    soup = BeautifulSoup(page.text, 'html.parser')
    if soup.find('div', class_='items_not_found'):
        return 0
    ProdAdd(soup.find_all('div', class_='goods_pos_bottom'))
    return Processing()

def Processing():
    global products
    # price_list = [x[1] for x in products]
    price_list = sorted(products.items(), key=lambda x: x[1])
    max_price, min_price = price_list[len(price_list)-1], price_list[0]
    avg_price = round(sum(products.values())/len(products),2)
    return [min_price, avg_price, max_price]
