import scrapy
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from selenium import webdriver

class GooglemapSpider(scrapy.Spider):
    name = 'googleMap'
    allowed_domains = ['www.google.com']
    # start_urls = ['https://www.google.com/maps/?hl=ja']
    url = 'https://www.google.com/maps/?hl=ja'

    driver = webdriver.Chrome()

    def start_requests(self):
        self.driver.get(self.url)
        self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys('浦安 焼肉')
        self.driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').send_keys(Keys.ENTER)
        sleep(1)
        elements = self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "の検索結果")]')
        self.driver.save_screenshot('xxx.png')

    def parse(self, response):
        driver = response.meta['driver']
        driver.find_element(By.XPATH, '//*[@id="searchboxinput"]').send_keys('浦安 焼肉')
        driver.find_element(By.XPATH, '//*[@id="searchbox-searchbutton"]').send_keys(Keys.ENTER)
        sleep(1)
        driver.save_screenshot('xxx.png')
        sleep(1)


    async def parse_page(self, url):
        # ブラウザと新しいページを開始
        browser = await launch(headless=False)  # ブラウザをヘッドレスモード（GUIなし）で起動するかどうか。
        page = await browser.newPage()

        # Google MapsのURLに移動
        await page.goto(url)

        await page.type('#searchboxinput', '浦安 焼肉')
        await page.click('#searchbox-searchbutton')
        await page.waitForNavigation()

        elements = await page.querySelectorAll('[aria-label*="の検索結果"]')

        if elements:  # 要素が存在するか確認
            # 最初の要素にフォーカスを当てます（他の要素にフォーカスを当てる場合、リストから選択してください）
            await elements[0].focus()

            while True:
                target_element = await page.querySelector('span.HlvSq')

                if target_element:
                    content = await page.evaluate('(element) => element.textContent', target_element)
                    if 'リストの最後に到達しました。' in content:
                        print("Target element found!")
                        break  # ターゲットが見つかったので終了ったのでループを抜ける

                # ターゲットがまだ見つからない場合、Endキーを送信してページの下部に移動
                await page.keyboard.press("PageDown")

                # キー送信後、要素がロードされるまで少し待機（ページや環境によって調整が必要）
                await asyncio.sleep(1)


        await page.screenshot({'path': 'screenshot.png'})
        # 必要な操作やデータの抽出をここで行います。
        # 例えば、特定の場所を検索したり、スクリーンショットを撮ったりすることができます。

        target_selector = 'a.hfpxzc'

        # セレクタに一致する要素を取得します。
        target_elements = await page.querySelectorAll(target_selector)

        urls = []
        for element in target_elements:
            # 'href'属性の値を取得
            href_value = await page.evaluate('(element) => element.getAttribute("href")', element)
            urls.append(href_value)

        # 作業が終了したらブラウザを閉じます。
        await browser.close()

        print(urls)
        print(len(urls))
