from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.loader import ItemLoader
from avito_parse.items import ZillowParseItem
from bs4 import BeautifulSoup as bs

import scrapy

class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ['http://www.zillow.com/homes/']
    # start_urls = ['http://www.zillow.com/homes/San-Francisco-ca/']

    browser = webdriver.Firefox()

    def __init__(self, cities: list, *args, **kwargs):
        self.cities = cities
        super().__init__(*args, **kwargs)


    def parse(self, response):
        for cities in self.cities:
            yield response.follow(f'{cities}', callback=self.city_parse, cb_kwargs={'cities': cities})


    def city_parse(self, response, cities):
        pagination = response.xpath('//li[contains(@class, "PaginationNumberItem-bnmlxt-0 kdxFbt")]/a/@href').extract()
        for url in pagination:
            yield response.follow(url, callback=self.parse)

        for ad_url in response.xpath(
                '//ul[contains(@class, "photo-cards")]/li/article//a[contains(@class, "list-card-link")]/@href').extract():
            yield response.follow(ad_url, callback=self.ad_parse, cb_kwargs={'cities': cities})



    def ad_parse(self, response, cities):
        self.browser.get(response.url)
        media_col = self.browser.find_element_by_xpath('//div[contains(@class, "ds-media-col")]')
        len_images = len(self.browser.find_elements_by_xpath('//ul[contains(@class, "media-stream")]/li//picture/source[@type="image/jpeg"]'))

        while True:
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            sleep(2)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            sleep(2)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            sleep(2)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            sleep(2)
            tmp_len = len(self.browser.find_elements_by_xpath('//ul[contains(@class, "media-stream")]/li//picture/source[@type="image/jpeg"]'))
            if tmp_len == len_images:
                break
            len_images = tmp_len

        selen_html = self.browser.page_source
        soup = bs(selen_html, 'html.parser')
        photos = soup.find_all('source', {"type": "image/jpeg"})

        item = ItemLoader(ZillowParseItem(), response, cities)
        item.add_value('city', cities)
        item.add_xpath('price', '//div[@class="ds-summary-row"]/h3//span[@class="ds-value"]/text()')
        item.add_xpath('address', '//h1[@class="ds-address-container"]//span/text()')
        item.add_value('photos', photos)
        yield item.load_item()

