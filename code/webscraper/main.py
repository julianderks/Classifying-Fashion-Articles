from scrapers.zalando import ZalandoScraper


z_scraper = ZalandoScraper(dest_path="../data/data")
z_scraper.scrape_website()
