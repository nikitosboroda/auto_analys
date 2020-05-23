import time
from math import floor, ceil

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

from utils import file_worker as ps

# TODO: add timestamp (get date when auto was posted on site) for excluding duplicates
# TODO: add docstrings
# TODO: change type of some cars parameters
# TODO: if got tuple of cars --> for each car get dataset with got amount (mb it's already done)
# TODO: add new column for city in dataset

cities = {"moskva": 0,
          "sankt-peterburg": 1,
          "novosibirsk": 2,
          "samara": 3,
          "murmansk": 4,
          "vladivostok": 5,
          "perm": 6,
          }

cars = [
    "bmw", "vaz", "audi",
    "ford", "hyundai", "kia",
    "mercedes", "mitsubishi", "toyota",
    "volkswagen", "honda", "mazda",
    "lexus", "porsche", "volvo"
]


class ParserAuto:
    """
    Class which parses metadata from site 'auto.ru'
    """
    LISTING_ITEMS = "ListingItem-module__container"

    # REACT_PAGE = "react-page body_controller_listing"
    # LISTING_CARS = "ListingCars-module__container ListingCars-module__list"

    def __init__(self, city, mark: tuple, amount=None, pages=10):
        self.city = city
        self.mark = mark
        self.amount = amount
        self.pages = pages
        self.filename = f'results_for_city_{city}_mark_{mark}_{amount}'
        # self.context = self.page.text
        # self.df = pd.DataFrame()

    def _find_all_cars(self, context):
        soup = BeautifulSoup(context, "lxml")
        list_of_cars = soup.find_all("div", {"class": self.LISTING_ITEMS})
        return list_of_cars

    def _get_from_meta(self, context, sliser=None):
        if sliser:
            cars = self._find_all_cars(context)[:sliser]
        else:
            cars = self._find_all_cars(context)
        for car in cars:
            car_meta_info = {}
            result = list(car.find("span"))
            for meta in result:
                if "span" in str(meta):
                    if meta.get("itemprop") == "offers":
                        for info in meta.find_all("meta"):
                            if info.get("itemprop") == "price":
                                car_meta_info.update(
                                    {info.get("itemprop"): info.get("content")}
                                )
                            else:
                                continue
                    if meta.get("itemprop") == "vehicleEngine":
                        for info in meta.find_all("meta"):
                            if info.get("itemprop") == "name":
                                car_meta_info.update(
                                    {"engine_name": info.get("content")}
                                )
                            else:
                                car_meta_info.update(
                                    {info.get("itemprop"): info.get("content")}
                                )
                else:
                    if meta.get("itemprop") != "image":
                        car_meta_info.update(
                            {meta.get("itemprop"): meta.get("content")}
                        )
            car_meta_info.update({'metro': self._get_metro_stations(car)})
            km_age = car.find("div", {"class": "ListingItem-module__kmAge"}).text
            km_age = '0' if "Новый" in km_age else km_age.replace("км", "")
            # print(km_age.split())
            car_meta_info.update({"km_age": int(''.join(km_age.split()))})
            self.df = self.df.append(car_meta_info, ignore_index=True)

    def _url_get_context(self, number, remainder=None):
        # print(number)
        for i in range(1, number + 1):
            for car in self.mark:
                self.df = pd.DataFrame()
                page = requests.get(self._change_page(i, car))
                page.encoding = "utf-8"
                if i == number:
                    self._get_from_meta(page.text, remainder)
                else:
                    self._get_from_meta(page.text)
                ps.write_to_file(self.df, filename=self.filename)
                time.sleep(10)  # just for not to be blocked by server

    def _change_page(self, page_val, car):
        address = (
            f"https://auto.ru/{self.city}/cars/{car}/"
            f"all/?sort=fresh_relevance_1-desc&output_type=list&page={page_val}"
        )
        return address

    @staticmethod
    def _get_metro_stations(car):
        main = car.find('div', {'class': "ListingItem-module__main"})
        metros = [metro.text for metro in main.find_all('span', {'class': 'MetroList__stationFirstName'})] or np.nan
        return metros

    def generate_dataset(self):
        if self.amount:
            pages = round(self.amount / 37)
            remainder = ceil(self.amount % 37) if self.amount > 37 else 0
            # print(pages, remainder)
            self._url_get_context(pages, remainder)
            return "Got all cars"
        else:
            self._url_get_context(self.pages)
        return 'Got info by pages'


def main():
    for city in cities:
        for car in cars:
            auto = ParserAuto(city, (car,))
            auto.generate_dataset()
            print(f"Got dataset for {car} in {city}")


if __name__ == "__main__":
    # auto = ParserAuto("sankt-peterburg", ("bmw",), 64)
    # print(auto.generate_dataset())
    main()
