import mysql.connector
from mysql.connector import Error
from src.utils import load_settings

class Database:
    def __init__(self):
        settings = load_settings()
        db_config = settings["database"]

        try:
            self.conn = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
                charset="utf8mb4"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("MySQL Connected!")

        except Error as e:
            print("Database connection error:", e)
            raise

    def save_event(self, data):
        sql = """
        INSERT INTO events (
            event_id, source, title, description, period,
            start_date, end_date, area, location, station,
            tags, detail_url, image_url
        )
        VALUES (
            %(event_id)s, %(source)s, %(title)s, %(description)s, %(period)s,
            %(start_date)s, %(end_date)s, %(area)s, %(location)s, %(station)s,
            %(tags)s, %(detail_url)s, %(image_url)s
        )
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            description = VALUES(description),
            period = VALUES(period),
            start_date = VALUES(start_date),
            end_date = VALUES(end_date),
            area = VALUES(area),
            location = VALUES(location),
            station = VALUES(station),
            tags = VALUES(tags),
            detail_url = VALUES(detail_url),
            image_url = VALUES(image_url),
            updated_at = CURRENT_TIMESTAMP;
        """
        self.cursor.execute(sql, data)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()