import requests, json, time
from bs4 import BeautifulSoup

#Функция составления выходного файла - Магазины+Продукты+Цены
def make_dataset(stores, productsLinks):
    list_dataset = [['prod_name', 'price', 'store'],] #Выходной датасет

    r_price = requests.Session() #Общая сессия
    r_price.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    #Перебираем список магазинов
    for (count, store) in enumerate(stores):
        ###### Часть для тестирования
        if count==5:
            break
        ######
        r_setcook_store = r_price.put('https://lenta.com/api/v1/me/store', json={"storeId": store['id']})
        #Перебираем список товаров
        for productLink in productsLinks:
            r_prod_site = r_price.get(productLink)
            soup = BeautifulSoup(r_prod_site.text)
            #Пытаемся распарсить цену
            try:
                price = soup.find('dd', {'class': 'price__primary'}).text
                price = price.replace(' ', '')
                price = ''.join([c for c in price if ord(c) > 31 or ord(c) == 9])
            except AttributeError: #если такого товара нет в магазине
                price = 'na'
            #Пытаемся распарсить наименование товара
            try:
                productName = soup.find('div', {'class': 'sku-card__title'}).text
                productName = ''.join([c for c in productName if ord(c) > 31 or ord(c) == 9])
                productName = productName.replace('  ', '')
            except AttributeError: #если такого товара нет в каталоге
                productName = 'na'

            list_dataset.append([productName, price, store])

            time.sleep(2) #Чтоб не дидосить сайт
    return list_dataset


#Перечень магазинов
r_stores = requests.Session()
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
r_stores_list = r_stores.get('https://lenta.com/api/v1/stores', headers = headers)
string_stores = r_stores_list.text
list_stores = json.loads(string_stores) #Список словарей с магазинами

#Перечень товаров
list_productsLinks = [
    'https://lenta.com/catalog/myaso-ptica-kolbasa/myaso-ohlazhdennoe/svinina/pf-svinina-korejjka-nk-kata-ohl-ves-rossiya/',
    'https://lenta.com/catalog/hlebobulochnye-izdeliya/hleb/baton/baton-365-dnejj-nareznojj-1s-narezka-rossiya-300g/',
    'https://lenta.com/catalog/moloko-syr-yajjco/molochnaya-produkciya/pasterizovannoe/moloko-prostokvashino-past-pitevoe-25-pet-rossiya-930ml/',
    'https://lenta.com/catalog/frukty-i-ovoshchi/frukty/citrusovye/grejjpfruty-ves-1kg/'
]

#Получаем датасет и записываем в файл
with open('dataset.csv', 'w') as out:
    out.write(str(make_dataset(list_stores, list_productsLinks)))


#ID: 945084edff1040a28d0b8462a5d43718
#Пароль: 36ef9f00a9d143b1b8605bd93c2047bd