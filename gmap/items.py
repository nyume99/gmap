# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GmapItem(scrapy.Item):
    名前 = scrapy.Field()
    電話番号 = scrapy.Field()
    住所 = scrapy.Field()
    カテゴリ = scrapy.Field()
    口コミ評価 = scrapy.Field()
    口コミ数 = scrapy.Field()
    URL = scrapy.Field()
