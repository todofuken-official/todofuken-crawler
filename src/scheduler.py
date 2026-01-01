from src.crawler_walkerplus import WalkerPlusCrawler
from src.database import Database
from src.utils import load_settings
from src.push import send_all

class Scheduler:
    def __init__(self):
        self.db = Database()
        self.crawler = WalkerPlusCrawler()

        settings = load_settings()
        self.daily_pages = settings["crawler"]["walkerplus"]["daily_scan_pages"]

    def is_event_exists(self, event_id):
        sql = "SELECT 1 FROM events WHERE event_id=%s AND source='walkerplus' LIMIT 1"
        self.db.cursor.execute(sql, (event_id,))
        return self.db.cursor.fetchone() is not None

    def crawl_daily(self):
        print("===== Daily Scheduler Start =====")

        new_events = []

        for page in range(1, self.daily_pages + 1):
            print(f"[Scheduler] Checking page {page}")

            events = self.crawler.get_event_list(page)

            for e in events:
                event_id = e["event_id"]

                if self.is_event_exists(event_id):
                    print(f"[STOP] Existing event found → {event_id}")
                    print("===== Scheduler Finished =====")

                    if new_events:
                        self.notify_new_events(new_events)

                    return

                print(f"[NEW] {event_id} {e['title']}")
                self.crawler.save_event(e)
                new_events.append(e)

        print("===== Scheduler Finished (Max pages scanned) =====")

        if new_events:
            self.notify_new_events(new_events)

    def notify_new_events(self, events):
        print("Sending push notifications...")

        title = f"오늘 새 일본 이벤트 {len(events)}개 업데이트"
        body = events[0]["title"]

        send_all(title, body)

        print("Push notifications sent.")