import json
import requests


class ZalandoScraper:
    def __init__(self):
        self.page_number = 0
        self.uri = "/kleding/?p=0"
        self.base_url = "https://www.zalando.nl/api/graphql/"

        self.headers = {
            "authority": "www.zalando.nl",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            "x-xsrf-token": "AAAAACwhZ8Ze_Ih7fvS997AnOKEXKdRC2aZqEaeb9wL0MHqrOAPf1gCKKgQd0wdR2ZHeNFQd2SSM2sAFgFIj0TuKjrfyKaDb5MR3nxkxn00GbuQYdPA1VaBKi9S9dRaaHdT_CaEXVigxrHJIQFhe1Ig=",
        
            "x-zalando-feature": "catalog",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            # "x-zalando-intent-context": "navigationTargetGroup=MEN",
            "content-type": "application/json",
            "x-zalando-request-uri": "/kleding/",
            "dpr": "1",
            "viewport-width": "800",
            "sec-ch-ua-platform": '"Windows"',
            "accept": "*/*",
            "origin": "https://www.zalando.nl",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.zalando.nl/kleding/?p=0",
            "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5",
        }

        self.payloads = """[
                {
                    "id": "e368030e65564d6a0b7329ac40b16870dddca3b404c3c86ee29b34c465cd2e04",
                    "variables": {
                        "id": "ern:collection:cat:categ:kleding",
                        "orderBy": "POPULARITY",
                        "filters": {
                            "discreteFilters": [],
                            "rangeFilters": [],
                            "toggleFilters": []
                        },
                        "after": "WzkyNCwyNzIxMjU3MDg5XQ==",
                        "first": 84,
                        "uri": "/kleding/?p=0",
                        "isPaginationRequest": true,
                        "isFDBEDisabled": true,
                        "width": 2079,
                        "height": 1000,
                        "notLoggedIn": true,
                        "disableTopTeasers": false,
                        "disableInCatalogTeasers": false
                    }
                }
            ]"""

    def update_page(self):
        next_page = self.page_number + 1

        args = (f"/?p={self.page_number}", f"/?p={next_page}")

        self.payloads = self.payloads.replace(*args)
        self.headers["referer"] = self.headers["referer"].replace(*args)

        self.page_number = next_page

    def get_product_ids(self):
        response = requests.post(
            self.base_url, headers=self.headers, data=self.payloads
        )
        edges = response.json()[0]["data"]["collection"]["entities"]["edges"]

        product_list = []
        for edge in edges:
            edge = edge["node"]

            if edge["__typename"] == "Product":
                product = {
                    "id": "11a7d00da8620ffe586ba647d2424f220a7f973f38dcc9e17fd22687d3345134",  # 11a7d00da8620ffe586ba647d2424f220a7f973f38dcc9e17fd22687d3345134, 42065a950350321d294bf6f0d60a2267042fe634956f00ef63a0a43c0db7dc38
                    "variables": {
                        "id": edge["id"],
                    },  # "skipHoverData": False},
                }

            product_list.append(product)

        return product_list

    def get_products(self):
        product_list = self.get_product_ids()

        response = requests.post(self.base_url, headers=self.headers, json=product_list)

        return response.json()

    def scrape(self):

        while True:
            print(f"-- PAGE {self.page_number} -- ")

            products = self.get_products()

            for product in products:
                product = product["data"]["product"]["family"]  # ["products"]

                print(product)

            scraper.update_page()

            if self.page_number > 3:
                exit()


if __name__ == "__main__":

    scraper = ZalandoScraper()

    scraper.scrape()
