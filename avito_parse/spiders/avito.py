import scrapy
import numpy as np
from pymongo import MongoClient



class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://avito.ru/orenburg/kvartiry/prodam-ASgBAgICAUSSA8YQ']

    client = MongoClient('mongodb://localhost:27017')
    data_base = client['avito']
    collection = data_base['avito_sell_propety']


    def parse(self, response):
        pagination = response.xpath('//div[contains(@class, "pagination-hidden-3jtv4")]/div/a/@href').extract()
        for url in pagination:
            yield response.follow(url=url, callback=self.parse)

        for ads_post in response.xpath('//div[contains(@class, "snippet-title-row")]/h3/a/@href').extract():
            yield response.follow(url=ads_post, callback=self.ads_parse)

    def ads_parse(self, response):
        params = {}
        title = response.xpath('//div[contains(@class, "title-info-main")]/h1/span/text()').extract_first()
        price = response.xpath('//span[contains(@class, "js-item-price")]/@content').extract_first()
        list_params_key = response.xpath('//ul[contains(@class, "item-params-list")]/li/span/text()').extract()
        list_params_value = np.array(response.xpath('//li[contains(@class, "item-params-list-item")]/text()').extract())
        list_params_value = list_params_value[list_params_value != ' ']

        for i, item in enumerate(list_params_key):
            params[item] = list_params_value[i]

        params['title'] = title
        params['price'] = price
        self.collection.insert_one(params)
        print(1)


