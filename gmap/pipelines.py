# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import gspread


class GmapPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append([item['名前'], item['電話番号'], item['住所'], item['カテゴリ'], item['口コミ評価'], item['口コミ数'], item['URL']])
        return item

    def close_spider(self, spider):
        print(self.items)
        gc = gspread.service_account(filename="./plexiform-bot-401901-1342afaaece7.json")
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/1MlRxiUULtv7csD8XPbByIKzXgZMJVgx6EinqS08lU0I"

        spreadsheet = gc.open_by_url(spreadsheet_url)
        spreadsheet.sheet1.append_rows(self.items)
