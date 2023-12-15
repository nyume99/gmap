import scrapy
import json
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from gmap.items import GmapItem


class GooglemapSpider(scrapy.Spider):
    name = 'googleMap'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.google.com/maps/?hl=ja']
    url = 'https://www.google.com/maps/?hl=ja'

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    #options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    def __init__(self, array=None, *args, **kwargs):
        super(GooglemapSpider, self).__init__(*args, **kwargs)
        if array:
            self.array = json.loads(array)
        else:
            self.array = []

    # def start_requests(self):
    def parse(self, response):

        print(self.array)
        key1 = self.array[0][0]

        for kw in self.array:
            self.driver.get(self.url)
            print(kw[1])

            self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys(key1 + ' ' + kw[1])
            self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').send_keys(Keys.ENTER)
            elements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@aria-label, "の検索結果")]'))
            )

            if elements:
                # 最初の要素にスクロールします。
                self.driver.execute_script('arguments[0].scrollIntoView();', elements[0])

                count = 0
                while True:
                    try:
                        end_element = self.driver.find_element(By.CSS_SELECTOR, 'span.HlvSq')

                        if end_element:
                            #print(end_element.text)
                            break

                    except Exception as e:
                        pass

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


# デプロイで発行されたURL
#json_file = 'https://script.google.com/macros/s/AKfycbwm20_bxQ305UGExZiuUbvYdTh_5wxGbOoO-Ck8V8lzM5-WtGJIl6rcDRdn5Kh6MyGu/exec'

#scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# URLの情報を辞書型へ変換
#key = json.loads(requests.get(json_file).text)

# credentialsを読み込む
#credentials = ServiceAccountCredentials.from_json_keyfile_dict(key, scope)

#gc = gspread.authorize(credentials)

#workbook = gc.open_by_key(ss_id)
#worksheet = workbook.worksheet(sht_name)
#  worksheet.append_rows(reserve_list)
