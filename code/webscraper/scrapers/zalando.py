import cfscrape
import json
from bs4 import BeautifulSoup
from utils.logging import Logger
import pandas as pd

request = cfscrape.CloudflareScraper()

OVERVIEW_QUERY_ID = "e368030e65564d6a0b7329ac40b16870dddca3b404c3c86ee29b34c465cd2e04"
PRODUCT_QUERY_ID = "42065a950350321d294bf6f0d60a2267042fe634956f00ef63a0a43c0db7dc38"

AVATAR_URL = "https://github.com/julianderks/Classifying-Fashion-Articles/blob/main/code/webscraper/zalando_scraper/images/zalando_label.png?raw=true"


class ZalandoScraper():
    def __init__(self, dest_path, log_path):
        self.save_path = dest_path + '/zalando_articles_raw.csv'
        self.Logger = Logger(log_path, username="Zalando Webscraper", avatar_url=AVATAR_URL,)

    def scrape_website(self):
        self.page_number = 0

        self.Logger.log_data("INFO", "Started scraping...")
        data_df = pd.DataFrame()

        while True:
            print(f' ---- Page {self.page_number} ---- \n')
            page_url = f"https://www.zalando.nl/kleding/?p={self.page_number}"

            content = self.get_page_content(page_url)
            page_articles = self.extract_articles(content)
            
            data_df = pd.concat([data_df, pd.DataFrame(page_articles)], ignore_index=True)
            data_df.to_csv(self.save_path, index=False)
            
            self.page_number += 1


    def get_page_content(self, page_url):
        response = request.get(page_url)
        self.check_response(response.status_code, page_url)

        self.Logger.log_data("INFO",
                f"Reading content of:\t{page_url}",
                details={},
                post_discord=False
            )       
        
        return response.content

    def check_response(self, status_code, url):

        if status_code == 200:
            return 
        else:
            self.Logger.log_data(
                "ERROR",
                f"while retrieving page {self.page_number}",
                {"statusCode": status_code},
                post_discord=True
            )
        exit()
    
    def get_packshot_img_url(self, article_url):
        """
        get article page content and grab the image element that is most likely to contain the packshot
        """

        content = self.get_page_content(article_url)

        bs = BeautifulSoup(content, "html.parser")
        packshot_url = bs.find("meta", property="og:image").get('content')

        return packshot_url

    def extract_articles(self, content):
        page_articles = []

        bs = BeautifulSoup(content, "html.parser")
        foundScripts = list(bs.find_all("script"))

        for script in foundScripts:
            if len(script) == 1:
                content = script.contents[0]

                if all(x in content for x in ["graphqlCache", OVERVIEW_QUERY_ID]):
                    content = json.loads(content)["graphqlCache"]

                    keys = list(content.keys())
                    for key in keys:
                        if PRODUCT_QUERY_ID in key:
                            article_data = self.extract_article(content[key]["data"]["product"])
                            article_data['image_url'] = self.get_packshot_img_url(article_data['article_url'])
                            page_articles.append(article_data)

        if len(page_articles) == 0:
            self.Logger.log_data(
                        "ERROR",
                        f"Empty article list on while retrieving page: {self.page_number}")
            exit()

        return page_articles

    def extract_article(self, article_data):
        product = {}

        product["article_id"] = article_data["sku"]
        product["article_name"] = article_data["name"]
        product["target_group"] = article_data["navigationTargetGroup"]
        product["category"] = article_data["silhouette"]
        product["supplier_name"] = article_data["supplierName"]
        product["brand"] = article_data["brand"]["name"]
        product["original_price"] = article_data["displayPrice"]["original"]["amount"]
        product["actual_price"] = article_data["displayPrice"]["current"]["amount"]
        product["article_url"] = article_data["uri"]

        return product

    