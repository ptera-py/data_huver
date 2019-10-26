import requests
from bs4 import BeautifulSoup
import json

#Функция составления выходного файла - Магазины+Продукты+Цены
def make_dataset(stores, products):
    r_price = requests.Session() #Общая сессия
    #Перебираем список магазинов
    for store in stores:
        r_setcook_store = r_price.put('https://lenta.com/api/v1/me/store', json={"storeId": store['id']})
        #Перебираем список товаров
        for product in products:
            r_prod_site = r_price.get(product)
            soup = BeautifulSoup(r_prod_site.text)
            #Пытаемся распарсить цену
            try:
                price = soup.find('dd', {'class': 'price__primary'}).text
                price = price.replace(' ', '')
                price = ''.join([c for c in price if ord(c) > 31 or ord(c) == 9])
            except AttributeError: #если такого товара нет в магазине
                price = 'na'
            print(store['id'], ' - ' , price)


#Перечень магазинов
r_stores = requests.Session()
r_stores_list = r_stores.get('https://lenta.com/api/v1/stores')
string_stores = r_stores_list.text
list_stores = json.loads(string_stores) #Список словарей с магазинами

#Перечень товаров
list_products = [
    'https://lenta.com/catalog/myaso-ptica-kolbasa/myaso-ohlazhdennoe/svinina/pf-svinina-korejjka-nk-kata-ohl-ves-rossiya/',
    'https://lenta.com/catalog/hlebobulochnye-izdeliya/hleb/baton/baton-365-dnejj-nareznojj-1s-narezka-rossiya-300g/',
    'https://lenta.com/catalog/moloko-syr-yajjco/molochnaya-produkciya/pasterizovannoe/moloko-prostokvashino-past-pitevoe-25-pet-rossiya-930ml/',
    'https://lenta.com/catalog/frukty-i-ovoshchi/frukty/citrusovye/grejjpfruty-ves-1kg/'
]


make_dataset(list_stores, list_products)