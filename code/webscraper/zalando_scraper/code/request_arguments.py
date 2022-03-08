import cfscrape
import json
import time
import colorama
from datetime import datetime
from bs4 import BeautifulSoup

# https://github.com/NotScar/zalando-scraper/blob/master/main.py

colorama.init()

request = cfscrape.CloudflareScraper()

OVERVIEW_QUERY_ID = "e368030e65564d6a0b7329ac40b16870dddca3b404c3c86ee29b34c465cd2e04"
PRODUCT_QUERY_ID = "42065a950350321d294bf6f0d60a2267042fe634956f00ef63a0a43c0db7dc38"

LOGGING_WEBHOOK = "https://discord.com/api/webhooks/950792199400992788/JBVlxAVu-9dschDF6bED0gJJCH5D-vRVc00POgAax-JqSIsFzrYLgZ6oBQxg1Kw1VpdJ"

COLOR = colorama.Fore
LOGGING_COLORS = {
    "INFO": COLOR.CYAN,
    "LOG": COLOR.BLUE,
    "WARNING": COLOR.YELLOW,
    "ERROR": COLOR.RED,
}


#    print(logDate + LOGGING_COLORS[logType] + ' [%s] ' %
#               (logType) + message + ' | ' + TABLE_TO_JSON(details) + COLOR.RESET)


def log(log_type, message, details):
    log_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    has_details = len(details) != 0
    details_txt = " | " + json.dumps(details) if has_details else ""

    with open("logs.log", "a+") as log_file:
        log_txt = (
            log_date
            + LOGGING_COLORS[log_type]
            + f" [{log_type}] "
            + message
            + details_txt
            + COLOR.RESET
            + "\n"
        )

        log_file.write(log_txt)

    data = {
        "content": None,
        "embeds": [
            {
                "color": None,
                "fields": [
                    {"name": "LOG TYPE", "value": "`%s`" % (log_type)},
                    {"name": "LOG MESSAGE", "value": "`%s`" % (message)},
                    {"name": "TIME", "value": "`%s`" % (log_date)},
                ],
            }
        ],
        "username": "Zalando Scraper Logs",
        "avatar_url": "https://avatars.githubusercontent.com/u/1564818?s=280&v=4",
    }

    if has_details:
        detailsString = ""

        for x in details:
            detailsString += f"`{str(x)} = {details[x]}`\n"

        data["embeds"][0]["fields"].insert(
            2, {"name": "LOG DETAILS", "value": detailsString}
        )

    request.post(LOGGING_WEBHOOK, json=data)


class ZalandoScraper:
    def __init__(self):
        self.page_number = 0

    def get_page_content(self):
        response = request.get(f"https://www.zalando.nl/kleding3/?p={self.page_number}")

        if response.status_code == 200:
            return response.status_code
        else:
            log(
                "ERROR",
                "Error while retrieving page",
                {"statusCode": response.status_code},
            )
            return {"error": "Invalid Status Code", "status_code": response.status_code}


scraper = ZalandoScraper()

print(scraper.get_page_content())
exit()


def extract_articles(content):
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
                        product = {}
                        prod_data = content[key]["data"]["product"]
                        product["article_id"] = prod_data["sku"]
                        product["article_name"] = prod_data["name"]
                        product["target_group"] = prod_data["navigationTargetGroup"]
                        product["category"] = prod_data["silhouette"]
                        product["supplier_name"] = prod_data["supplierName"]
                        product["brand"] = prod_data["brand"]["name"]
                        product["original_price"] = prod_data["displayPrice"][
                            "original"
                        ]["amount"]
                        product["actual_price"] = prod_data["displayPrice"]["current"][
                            "amount"
                        ]
                        product["url"] = prod_data["uri"]
                        product["image_url"] = prod_data["mediumDefaultMedia"]["uri"]

                        exit()
    # print(type(foundScripts))
    exit()
    json_script = json.loads(script)

    # id for products : 42065a950350321d294bf6f0d60a2267042fe634956f00ef63a0a43c0db7dc38
    print(list(json_script["graphqlCache"].keys())[3])
    key = list(json_script["graphqlCache"].keys())[4]
    print(json_script["graphqlCache"][key])
    # print(json_script.keys())

    #         if script.contents[0].startswith("window.feedPreloadedState="):
    #             print("?yeS")
    # #             script = script.contents[0]
    #             script = script[26:]
    #             script = script[:-1]
    #             return json.loads(script)["feed"]["items"]


# response = get_page_data()
# response_filt = filter_json(response)
# print(response_filt)
#     else:
#         log(
#             "ERROR",
#             "Error while retrieving page",
#             {"statusCode": response.status_code},
#         )
#         return {"error": "Invalid Status Code", "status_code": response.status_code}


# log("ERROR", "Invalid Country (get_page_data)", {"countryCode": countryCode})
#     return {"error": "Invalid Country"}
