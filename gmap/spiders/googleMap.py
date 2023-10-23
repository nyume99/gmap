import scrapy
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

from gmap.items import GmapItem


class GooglemapSpider(scrapy.Spider):
    name = 'googleMap'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.google.com/maps/?hl=ja']
    url = 'https://www.google.com/maps/?hl=ja'

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,1024')

    driver = webdriver.Chrome(options=options)

    # def start_requests(self):
    def parse(self, response):

        self.driver.get(self.url)
        self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys('浦安　焼肉')
        self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').send_keys(Keys.ENTER)
        elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@aria-label, "の検索結果")]'))
        )

        if elements:
            # 最初の要素にスクロールします。
            self.driver.execute_script("arguments[0].scrollIntoView();", elements[0])

            count = 0
            while True:
                try:
                    end_element = self.driver.find_element(By.CSS_SELECTOR, 'span.HlvSq')

                    if end_element:
                        print(end_element.text)
                        break

                except Exception as e:
                    print(e)

                # ページの下部に移動します。
                elements[0].send_keys(Keys.PAGE_DOWN)
                count += 1

                # 要素がロードされるまで待ちます。
                time.sleep(1)  # 必要に応じて、待機時間を調整してください。
        # self.driver.save_screenshot('xxx.png')
        print(count)

        target_elements = self.driver.find_elements(By.XPATH, '//a[contains(@class, "hfpxzc")]')

        gmap_urls = []

        for element in target_elements:
            href = element.get_attribute("href")
            gmap_urls.append(href)

        for gmap_url in gmap_urls:
            self.driver.get(gmap_url)
            response = Selector(text=self.driver.page_source)

            detail_elements = response.xpath('//div[@class="AeaXub"]')
            for detail in detail_elements:
                img_src = detail.xpath('.//img[@class="Liguzb"]/@src').get()

                if 'phone' in img_src:
                    phone = detail.xpath('.//div[@class="Io6YTe fontBodyMedium kR99db "]/text()').get()
                elif 'place' in img_src:
                    place = detail.xpath('.//div[@class="Io6YTe fontBodyMedium kR99db "]/text()').get()
                elif 'public' in img_src:
                    url = detail.xpath('.//div[@class="Io6YTe fontBodyMedium kR99db "]/text()').get()

            yield GmapItem(
                名前=response.xpath('//h1/text()').get(),
                電話番号=phone,
                住所=place,
                カテゴリ=response.xpath('//button[@jsaction="pane.rating.category"]/text()').get(),
                口コミ評価=response.xpath('//div[@class="F7nice "]/span/span/text()').get(),
                口コミ数=response.xpath('//span[contains(@aria-label, "件のクチコミ")]/text()').get(),
                URL=url
            )

