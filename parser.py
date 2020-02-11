import pandas as pd
import requests
from bs4 import BeautifulSoup

# 'https://auto.ru/{city}/cars/{car_name}/all/?sort=fresh_relevance_1-desc&output_type=list&page={page}'

page = requests.get(
    'https://auto.ru/sankt-peterburg/cars/bmw/all/?sort=fresh_relevance_1-desc&output_type=list&page=7')
page.encoding = 'utf-8'
context = page.text

soup = BeautifulSoup(context, 'lxml')


def find_all_cars():
    return soup.find_all('div', {'class': 'ListingItem-module__container ListingCars-module__listingItem'})


def get_from_meta():
    cars = find_all_cars()
    for car in cars:
        dd = {}
        result = list(car.find('span'))
        for meta in result:
            if 'span' in str(meta):
                if meta.get('itemprop') == 'offers':
                    for info in meta.find_all('meta'):
                        if info.get('itemprop') == 'price':
                            dd.update({info.get('itemprop'): info.get('content')})
                        else:
                            continue
                if meta.get('itemprop') == 'vehicleEngine':
                    for info in meta.find_all('meta'):
                        if info.get('itemprop') == 'name':
                            dd.update({'engine_name': info.get('content')})
                        else:
                            dd.update({info.get('itemprop'): info.get('content')})
            else:
                if meta.get('itemprop') != 'image':
                    dd.update({meta.get('itemprop'): meta.get('content')})
        kmAge = car.find('div', {'class': "ListingItem-module__kmAge"}).text
        kmAge = 0 if 'Новый' in kmAge else kmAge.replace('км', '')
        dd.update({'km_age': kmAge})
        # for i in dd:
        #     print(i, '------------', dd[i])
        # print('==================> ', len(dd))


def add_to_frame(dictionary: dict):
    pd.DataFrame()


get_from_meta()
