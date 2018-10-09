# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
import requests

products = {}
req_head = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'Cookie': 'Utk_DvcGuid=4927058B8BEE38001B022A69176346FA; _ga=GA1.2.312638321.1527269139; cto_lwid=e0fdaa37-fc74-4aaf-a0f8-6b73830a13a8; _ym_uid=1527269140425788495; flocktory-uuid=35f03722-df32-494f-87a8-17d44d988a9f-4; Utk_SssTkn=2D876BED1D6B350EEF17BC66F87CBCD8; _ym_d=1535295132; rerf=AAAAAFu52h5Cg9dWA5IEAg==; Utk_MrkGrpTkn=0569FCEB1BD367CC198CD91E99FFA97A; ipp_uid2=LWPiOVVs1jIFBcnO/da4E6AOcZEhSNUjdlz9krg==; ipp_uid1=1538906654472; ipp_uid=1538906654472/LWPiOVVs1jIFBcnO/da4E6AOcZEhSNUjdlz9krg==; SOURCE_ID=; SOURCE_ID_client=312638321.1527269139; _gcl_au=1.1.189900668.1538906657; Utk_LncTime=2018-10-10+00%3A57%3A16%7C9D8DD9D279EB3E01446CF90F93C4AD90; SGM=74; _gid=GA1.2.2074156099.1539122238; _ym_visorc_942065=w; _ym_isad=1; ipp_static_key=1539122244485/M6Kz/O7uC35a/5Vx6YodUA==; ipp_key=v1539122248781/v3394724575ded878b223b2d5/dLv5O9QD0Z+7ZMengR/png==; _gaexp=GAX1.2.09pMEHJvTpywnk-4OGzj8A.17900.0!UlyVt_iVRGOeeOL4lQ1Z-w.17894.1'
    }
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
    # print(soup.prettify())
    if soup.find('div', class_='items_not_found'):
        return 0
    ProdAdd(soup.find_all('div', class_='goods_pos_bottom'))
    return Processing()

def Processing():
    global products
    price_list = sorted(products.items(), key=lambda x: x[1])
    max_price, min_price = price_list[len(price_list)-1], price_list[0]
    avg_price = round(sum(products.values())/len(products),2)
    return [min_price, avg_price, max_price]
