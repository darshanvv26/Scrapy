# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

class QuotesElementsDatabase4Pipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("myquotes.db")
        self.curr = self.conn.cursor()
    
    def create_table(self):
        # 🚨 WARNING: This deletes old data each run (good for demos)
        self.curr.execute("DROP TABLE IF EXISTS quotes_tb")
        self.curr.execute("""
            CREATE TABLE quotes_tb (
                title TEXT,
                author TEXT,
                tag TEXT
            )
        """)

    def process_item(self, item, spider):
        self.store_db(item, spider)
        return item

    def store_db(self, item, spider):
        self.curr.execute("""
            INSERT INTO quotes_tb (title, author, tag)
            VALUES (?, ?, ?)
        """, (item['title'], item['author'], item['tag']))
        self.conn.commit()
        spider.logger.info(f"Inserted: {item['title']} by {item['author']}")

