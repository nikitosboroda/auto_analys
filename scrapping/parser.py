import time

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

from utils import file_worker as ps


# TODO: add docstrings
# TODO: implement functionality to get info about cars (with amount size) not only with page
# TODO: change type of some cars parameters
class ParserAuto:
    LISTING_ITEMS = "ListingItem-module__container " \
                    "ListingCars-module__listingItem"

    def __init__(self, city, mark: tuple, amount):
        self.city = city
        self.mark = mark
        self.amount = amount
        # self.context = self.page.text
        # self.df = pd.DataFrame()

    def _find_all_cars(self, context):
        soup = BeautifulSoup(context, "lxml")
        return soup.find_all(
            "div",
            {"class": self.LISTING_ITEMS},
        )

    def _get_from_meta(self, context):
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

    def _url_get_context(self, number):
        for i in range(1, number + 1):
            for car in self.mark:
                self.df = pd.DataFrame()
                page = requests.get(self._change_page(i, car))
                page.encoding = "utf-8"
                self._get_from_meta(page.text)
                ps.write_to_file(self.df)
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

    def return_data(self, pages=10):
        self._url_get_context(pages)
        return self.df


if __name__ == "__main__":
    auto = ParserAuto("sankt-peterburg", ("bmw",), 37)
    print(auto.return_data())
