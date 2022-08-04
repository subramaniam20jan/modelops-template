import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from tqdm.auto import tqdm
from tqdm.contrib.itertools import product
import pickle


def safe_load(d, e):
    if e in d:
        return d[e]
    else:
        return None


def get_attr_in_array(array, attribute_name):
    return [safe_load(element, attribute_name) for element in array]


def get_attr(dic, attribute_name):
    return safe_load(dic, attribute_name)


class BoligScrapper:
    columns_of_interest = [
        "addressID",
        "cityName",
        "coordinates",
        "door",
        "floor",
        "houseNumber",
        "roadName",
        "weightedArea",
        "zipCode",
        "registrations",
        "energyLabelImprovement",
    ]

    def __init__(self, base_url, min_area=10, max_area=250):
        self.errored_urls = []
        self.base_url = base_url
        self.min_area = min_area
        self.max_area = max_area
        self.min_price = 10000
        self.max_price = 20000000
        self.min_year = 1993
        self.max_year = 2022

    def _vary_by_year(self, url: str, year: int):
        url += f"&yearSoldFrom={year}&yearSoldTo={year+1}"
        return url

    def _vary_by_area(self, url: str, area: int):
        url += f"&areaMin={area}&areaMax={area+10}"
        return url

    def _vary_by_price(self, url: str, price: int):
        url += f"&priceMin={price}&priceMax={price+1000000}"
        return url

    def _add_handle_type(self, handle: str):
        self.base_url += f"&registrationTypes={handle}"

    def compute_all_url(self):
        print("Getting all URLs")
        all_urls = []
        area = self.min_area
        year = self.min_year

        iterator = product(
            range(self.min_year, self.max_year), range(self.min_area, self.max_area, 10)
        )
        # range(self.min_price, self.max_price, 1000000)
        for year, area in iterator:
            new_url = self._vary_by_area(self.base_url, area)
            new_url = self._vary_by_year(new_url, year)
            # new_url = self._vary_by_price(new_url, price)
            all_urls.append(new_url)
        return all_urls

    def get_url_content(self, url):
        try:
            html = requests.get(url).content
            soup = BeautifulSoup(html, "html.parser")
            data_content = soup.find_all("script")
            data_content = data_content[len(data_content) - 1]
            json_content = json.loads(data_content.contents[0])
            json_data = json_content.get("props").get("pageProps").get("addresses")
            df = pd.DataFrame(json_data)
            return df
        except Exception:
            print(f"Error occured in URL {url}")
            self.errored_urls.append(url)

        return None

    def load_all_content(self):
        all_urls = self.compute_all_url()
        self.all_urls = all_urls
        full_df = None
        print("Loading URL content")
        for url in tqdm(all_urls):
            df = self.get_url_content(url)
            if df is not None:
                if full_df is None:
                    full_df = df
                else:
                    full_df = pd.concat([full_df, df])
        self.full_df = full_df.reset_index(drop=True)
        return True

    def extract_meaningful_data(self, interesting_df=None):
        if interesting_df is None:
            interesting_df = self.full_df.copy()

        interesting_df = interesting_df[self.columns_of_interest].copy()
        interesting_df["amount"] = interesting_df.apply(
            lambda x: get_attr_in_array(x["registrations"], "amount"), axis=1
        )
        interesting_df["date"] = interesting_df.apply(
            lambda x: get_attr_in_array(x["registrations"], "date"), axis=1
        )
        interesting_df["perAreaPrice"] = interesting_df.apply(
            lambda x: get_attr_in_array(x["registrations"], "perAreaPrice"), axis=1
        )
        interesting_df["type"] = interesting_df.apply(
            lambda x: get_attr_in_array(x["registrations"], "type"), axis=1
        )
        interesting_df["lat"] = interesting_df.apply(
            lambda x: get_attr(x["coordinates"], "lat"), axis=1
        )
        interesting_df["lon"] = interesting_df.apply(
            lambda x: get_attr(x["coordinates"], "lon"), axis=1
        )
        interesting_df["coordinate_type"] = interesting_df.apply(
            lambda x: get_attr(x["coordinates"], "type"), axis=1
        )
        interesting_df["energy_label_improvement"] = interesting_df.apply(
            lambda x: get_attr(x["energyLabelImprovement"], "improvementCase"), axis=1
        )
        interesting_df = interesting_df.drop(columns=["registrations"])
        interesting_df = interesting_df.drop(columns=["coordinates"])
        interesting_df = interesting_df.drop(columns=["energyLabelImprovement"])
        interesting_df = interesting_df.explode(
            ["amount", "date", "perAreaPrice", "type"]
        )
        really_interesting_df = interesting_df.drop_duplicates().reset_index(drop=True)

        # Convert to right datatypes
        numeric_columns = ["amount", "perAreaPrice", "perAreaPrice", "zipCode", "floor"]
        for col in numeric_columns:
            really_interesting_df[col] = pd.to_numeric(really_interesting_df[col])

        self.really_interesting_df = really_interesting_df
        return really_interesting_df

    def persist_to_pickle(self, file_name):
        raw_file = file_name + "_raw.pkl"
        cleaned_file = file_name + "_clean.pkl"
        self.full_df.to_pickle(raw_file)
        self.really_interesting_df.to_pickle(cleaned_file)

    def load_from_pickle(self, file_name):
        raw_file = file_name + "_raw.pkl"
        cleaned_file = file_name + "_clean.pkl"
        self.full_df = pd.read_pickle(raw_file)
        self.really_interesting_df = pd.read_pickle(cleaned_file)
        self.all_urls = self.compute_all_url()


class BoligMarket:
    def __init__(self, scraper_list):
        self.scraper_list = scraper_list
        all_interesting_dfs = [
            scraper.really_interesting_df for scraper in scraper_list
        ]
        really_interesting_df = pd.concat(all_interesting_dfs)
        self.really_interesting_df = really_interesting_df.reset_index(drop=True)

    def persist_to_pickle(self, file):
        with open(file, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_pickle(cls, file):
        with open(file, "rb") as f:
            obj = pickle.load(f)
        return obj

    def clean_data(self):
        df = self.really_interesting_df

        # Change numeric data types
        numeric_columns = ["amount", "perAreaPrice", "perAreaPrice", "floor"]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col])

        # Sort and filter annoying data
        df.sort_values(axis=0, by=["date"]).copy()
        df = df[df["type"] == "normal"].reset_index(drop=True)
        df = df[df["perAreaPrice"] <= 150000].reset_index(drop=True)

        # Add some extra columns
        def size_category(size):
            if size < 50:
                return "small"
            if size < 100:
                return "medium"
            if size < 150:
                return "large"
            else:
                return "extra-large"

        def size_cat_fine(size):
            try:
                base = 10
                nearest_multiple = base * round(size / base)
            except Exception:
                nearest_multiple = 0
            return nearest_multiple

        def to_month(date):
            return date[:-2] + "01"

        def to_year(date):
            return date[:-5] + "01-01"

        df["apt_size"] = df.apply(lambda x: size_category(x["weightedArea"]), axis=1)
        df["apt_size_fine"] = df.apply(
            lambda x: size_cat_fine(x["weightedArea"]), axis=1
        )
        df["date_agg"] = df.apply(lambda x: to_month(x["date"]), axis=1)
        df["date_yr"] = df.apply(lambda x: to_year(x["date"]), axis=1)
        df["date"] = pd.to_datetime(df["date"])

        self.really_interesting_df = df
