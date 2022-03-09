from scrapers.zalando import ZalandoScraper


dest_path = "code\data\data"
z_scraper = ZalandoScraper(
    dest_path=r"C:\Users\derks\OneDrive\Bureaublad\Classifying Fashion Articles\code\data\data",
    log_path=r"C:\Users\derks\OneDrive\Bureaublad\Classifying Fashion Articles\code\webscraper\scrapers\logs",
)

z_scraper.scrape_website()
