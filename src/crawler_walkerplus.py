import requests
import time
from bs4 import BeautifulSoup

from src.database import Database
from src.parser import parse_period
from src.utils import load_settings

class WalkerPlusCrawler:
    def __init__(self):
        settings = load_settings()
        self.db = Database()

        self.BASE_URL = settings["crawler"]["walkerplus"]["base_url"]
        self.full_scan_pages = settings["crawler"]["walkerplus"]["full_scan_pages"]
        self.daily_scan_pages = settings["crawler"]["walkerplus"]["daily_scan_pages"]

    def request_page(self, url):
        for retry in range(3):
            try:
                response = requests.get(url, timeout=10)
                response.encoding = 'utf-8'
                return response.text
            except Exception as e:
                print(f"[ERROR] Retry {retry+1}/3 for {url}: {e}")
                time.sleep(2)
        print(f"[FATAL] Failed to load {url}")
        return None

    def parse_event_block(self, event):
        title_tag = event.select_one(".m-mainlist-item__ttl > span")
        if not title_tag:
            return None

        title = title_tag.text.strip()

        link_tag = event.select_one(".m-mainlist-item__ttl")
        detail_link = link_tag.get("href")
        detail_url = self.BASE_URL + detail_link
        event_id = detail_link.strip("/").split("/")[-1]

        period_tag = event.select_one(".m-mainlist-item-event__period")
        if period_tag:
            end_tag = period_tag.select_one(".m-mainlist-item-event__end")
            if end_tag:
                end_tag.decompose()
            open_tag = period_tag.select_one(".m-mainlist-item-event__open")
            if open_tag:
                open_tag.decompose()
            period_raw = period_tag.text.strip()
        else:
            period_raw = ""

        start_date, end_date = parse_period(period_raw)

        desc_tag = event.select_one(".m-mainlist-item__txt")
        desc = desc_tag.text.strip() if desc_tag else ""

        map_tag = event.select_one(".m-mainlist-item__map")
        if map_tag:
            a_tags = map_tag.select("a")

            prefecture = ""
            city = ""
            if len(a_tags) >= 2:
                prefecture = a_tags[0].text.strip()
                city = a_tags[1].text.strip()

            elif len(a_tags) == 1:
                prefecture = a_tags[0].text.strip()
                text_nodes = map_tag.find_all(string=True)
                flat_text = " ".join([t.strip().replace('"', "") for t in text_nodes if t.strip()])
                city = flat_text.replace(prefecture, "").strip()

            area_text = f"{prefecture} {city}".strip()
        else:
            area_text = ""

        stations = event.select(".m-mainlist-item__station > a")
        stations_text = ", ".join([s.text.strip() for s in stations])

        place_tag = event.select_one(".m-mainlist-item-event__place")
        place = place_tag.text.strip() if place_tag else ""

        tags = event.select(".m-mainlist-item__tagsitemlink")
        tags_text = ", ".join([t.text.strip() for t in tags])

        return {
            "event_id": event_id,
            "source": "walkerplus",
            "title": title,
            "description": desc,
            "period": period_raw,
            "start_date": start_date,
            "end_date": end_date,
            "area": area_text,
            "location": place,
            "station": stations_text,
            "tags": tags_text,
            "detail_url": detail_url,
            "image_url": None
        }

    def get_event_list(self, page):
        url = f"{self.BASE_URL}/event_list/{page}.html" if page > 1 else f"{self.BASE_URL}/event_list/"
        html = self.request_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        events = soup.select(".m-mainlist__item")

        results = []
        for event in events:
            try:
                data = self.parse_event_block(event)
                if data:
                    results.append(data)
            except Exception as e:
                print(f"[ERROR] parsing event: {e}")

        return results

    def save_event(self, event_data):
        self.db.conn.ping(reconnect=True)
        self.db.save_event(event_data)

    def crawl_page(self, page):
        print(f"[INFO] Full-scan crawling page {page}")
        events = self.get_event_list(page)
        for e in events:
            self.save_event(e)
            print(f"[SAVE] {e['event_id']} {e['title']}")

    def crawl_all(self):
        print("------ FULL SCAN START ------")
        for page in range(1, self.full_scan_pages + 1):
            self.crawl_page(page)
            time.sleep(1)
        print("------ FULL SCAN FINISHED ------")