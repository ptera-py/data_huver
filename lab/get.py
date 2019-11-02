import requests, json, time, datetime
from bs4 import BeautifulSoup

#Функция создания файла на yandex.disk
def create_yadisk(token, path, filename, data):
    headers = {
        'Authorization': 'OAuth ' + token, #Авторизация на yadisk
    }
    params = {
        'path': '/' + path + '/' + filename, #Путь и название файла, который создаётся
    }
    UrlForDownload = requests.get('https://cloud-api.yandex.net:443/v1/disk/resources/upload', headers=headers, params=params) #Запрашиваем URL для загрузки
    requests.put(UrlForDownload.json()['href'], data=data) #Создаём файл


#Функция получения перечня магазинов
def get_stores():
    r_stores = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r_stores_list = r_stores.get('https://lenta.com/api/v1/stores', headers=headers)
    string_stores = r_stores_list.text
    list_stores = json.loads(string_stores)  # Список словарей с магазинами
    return list_stores


#Функция получения цены товара
def get_price(store, productLink):
    r_price = requests.Session()  # Общая сессия
    r_price.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' #Чтобы лента не блокировала запросы
    }
    r_setcook_store = r_price.put('https://lenta.com/api/v1/me/store', json={"storeId": store['id']}) #Устанавливаем магазин
    r_prod_site = r_price.get(productLink)
    soup = BeautifulSoup(r_prod_site.text)
    # Пытаемся распарсить цену
    try:
        price = soup.find('dd', {'class': 'price__primary'}).text
        price = price.replace(' ', '')
        price = ''.join([c for c in price if ord(c) > 31 or ord(c) == 9])
    except AttributeError:  # если такого товара нет в магазине
        price = 'na'
    # Пытаемся распарсить наименование товара
    try:
        productName = soup.find('div', {'class': 'sku-card__title'}).text
        productName = ''.join([c for c in productName if ord(c) > 31 or ord(c) == 9])
        productName = productName.replace('  ', '')
    except AttributeError:  # если такого товара нет в каталоге
        productName = 'na'
    return {'productName': productName.encode('utf-8'), 'price': price.encode('utf-8')}


#Перечень товаров
list_productsLinks = [
    'https://lenta.com/catalog/myaso-ptica-kolbasa/myaso-ohlazhdennoe/svinina/pf-svinina-korejjka-nk-kata-ohl-ves-rossiya/',
    'https://lenta.com/catalog/hlebobulochnye-izdeliya/hleb/baton/baton-365-dnejj-nareznojj-1s-narezka-rossiya-300g/',
    'https://lenta.com/catalog/moloko-syr-yajjco/molochnaya-produkciya/pasterizovannoe/moloko-prostokvashino-past-pitevoe-25-pet-rossiya-930ml/',
    'https://lenta.com/catalog/frukty-i-ovoshchi/frukty/citrusovye/grejjpfruty-ves-1kg/'
]


token = '---' #Авторизация для YaDisk
path = 'data_sets' #Папка на YaDisk
list_stores = get_stores() #Получаем список магазинов

#Запускаем цикл по магазинам
for (count, store) in enumerate(list_stores):
    now = str(datetime.datetime.now()) #Текущее время
    nowС = now.replace(' ', '').replace('-', '').replace(':', '').replace('.', '')  # Текущее время, очищенное от знаков препинания
    filename = nowС + '.txt'  # Формируем имя файла из текущего времени
    ###### Часть для тестирования
    if count > 5:
        break
    ######
    result = get_price(store,list_productsLinks[0]) #Получаем цену и название продукта
    inputStr = nowС.encode('utf-8') + '<>'.encode('utf-8') + result['price'] + '<>'.encode('utf-8') + result['productName'] + '<>'.encode('utf-8') + str(store['id']).encode('utf-8') #Строка для записи в Файл
    create_yadisk(token, path, filename, inputStr) #Записываем цену и название продукта на YaDisk
    time.sleep(2) #Засыпаем на 2сек, чтоб не дидосить сайт

#Записываем перечень магазинов на YaDisk
create_yadisk(token,path,'stores.txt',str(list_stores).encode('utf-8'))