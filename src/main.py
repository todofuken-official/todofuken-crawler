from src.crawler_walkerplus import WalkerPlusCrawler
from src.scheduler import Scheduler
from src.utils import load_settings

def run_walkerplus_full():
    print("===== WalkerPlus FULL SCAN Start =====")
    crawler = WalkerPlusCrawler()
    crawler.crawl_all()
    print("===== WalkerPlus FULL SCAN Finished =====")

def run_daily_increment():
    print("===== WalkerPlus DAILY INCREMENT Start =====")
    scheduler = Scheduler()
    scheduler.crawl_daily()
    print("===== WalkerPlus DAILY INCREMENT Finished =====")

def run_all():
    print("=====================================")
    print("     Todofuken - Daily Crawler       ")
    print("=====================================")

    run_daily_increment()

    print("-------------------------------------")
    print("        Finished All Crawlers        ")
    print("-------------------------------------")

if __name__ == "__main__":
    run_all()