from datetime import datetime
import json
import requests
import colorama
import os


class Logger:
    colorama.init()

    COLOR = colorama.Fore

    LOGGING_COLORS = {
        "INFO": COLOR.CYAN,
        "LOG": COLOR.BLUE,
        "WARNING": COLOR.YELLOW,
        "ERROR": COLOR.RED,
    }

    # read discord webhook api (currently turned off for simplicity, its just a nerdy gadget)
    with open("./utils/discord_webhook.json", 'r') as myfile:
        logging_webhook = json.load(myfile)['logging_webhook']

    def __init__(self, log_path, username="bot", avatar_url=""):
        self._log_path = log_path + "\log.log"

        self._username = username
        self._avatar_url = avatar_url

        if os.path.exists(self._log_path):
            os.remove(self._log_path)
            
    def log_data(self, log_type, message, details={}, post_discord=False):
        log_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        log_txt = (
            log_date
            + f" [{log_type}] "
            + message
            + (f" | {json.dumps(details)}" if len(details) != 0 else "")
        )

        print(
            log_txt.replace(
                f" [{log_type}] ",
                Logger.LOGGING_COLORS[log_type]
                + f" [{log_type}] "
                + Logger.COLOR.RESET,
            )
        )
        with open(self._log_path, "a+") as log_file:
            log_file.write(log_txt + "\n")

    #     if post_discord:
    #         self.log_discord(log_type, message, log_date, details)

    # def log_discord(self, log_type, message, log_date, details):

    #     data = {
    #         "content": None,
    #         "embeds": [
    #             {
    #                 "color": None,
    #                 "fields": [
    #                     {"name": "LOG TYPE", "value": "`%s`" % (log_type)},
    #                     {"name": "LOG MESSAGE", "value": "`%s`" % (message)},
    #                     {"name": "TIME", "value": "`%s`" % (log_date)},
    #                 ],
    #             }
    #         ],
    #         "username": self._username,
    #         "avatar_url": self._avatar_url,
    #     }

    #     if len(details) != 0:
    #         detailsString = ""

    #         for x in details:
    #             detailsString += f"`{str(x)} = {details[x]}`\n"

    #         data["embeds"][0]["fields"].insert(
    #             2, {"name": "LOG DETAILS", "value": detailsString}
    #         )

    #     requests.post(Logger.logging_webhook, json=data)
