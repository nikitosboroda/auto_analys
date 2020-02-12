import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils import pandas_settings as ps


class ParserAuto:
    LISTING_ITEMS = "ListingItem-module__container " \
                    "ListingCars-module__listingItem"

    def __init__(self, city, mark):
        self.city = city
        self.mark = mark
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
            km_age = car.find("div", {"class": "ListingItem-module__kmAge"}).text
            km_age = 0 if "Новый" in km_age else km_age.replace("км", "")
            car_meta_info.update({"km_age": km_age})
            self.df = self.df.append(car_meta_info, ignore_index=True)

    def _url_get_context(self, number):
        for i in range(1, number + 1):
            self.df = pd.DataFrame()
            page = requests.get(self._change_page(i))
            page.encoding = "utf-8"
            self._get_from_meta(page.text)
            ps.write_to_file(self.df)
            time.sleep(10)
            print('awake up')

    def _change_page(self, page_val):
        address = (
            f"https://auto.ru/{self.city}/cars/{self.mark}/"
            f"all/?sort=fresh_relevance_1-desc&output_type=list&page={page_val}"
        )
        return address

    def return_data(self, pages=10):
        self._url_get_context(pages)
        return self.df


if __name__ == "__main__":
    auto = ParserAuto("sankt-peterburg", "bmw")
    # print(auto.return_data())
