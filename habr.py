import scrapy
from avito_parse.items import AvitoParseItem
from avito_parse.items import AuthorParseItem
from scrapy.loader import ItemLoader


class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru']

    def parse(self, response):
        pagination = response.xpath('//li[contains(@class, "arrows-pagination__item")]/a/@href').extract()
        for url in pagination:
            yield response.follow(url, callback=self.parse)

        for post_link in response.xpath('//h2[contains(@class, "post__title")]/a/@href').extract():
            yield response.follow(url=post_link, callback=self.post_parse)


    def post_parse(self, response):
        item = ItemLoader(AvitoParseItem(), response)
        item.add_xpath('title', '//h1[contains(@class, "post__title")]/span/text()')
        item.add_xpath('author_name', '//header[contains(@class, "post__meta")]/a/span/text()')
        item.add_value('post_url', response.url)
        item.add_xpath('images', '//div[contains(@class, "post__body")]//img/@src')
        item.add_xpath('comments', '//h2[contains(@class, "comments-section__head-title")]/span/text()')
        item.add_xpath('author_url', '//header[contains(@class, "post__meta")]/a/@href')
        yield item.load_item()
        author_url = response.xpath('//header[contains(@class, "post__meta")]/a/@href').extract()[0]
        yield response.follow(author_url, callback=self.author_parse)


    def author_parse(self, response):
        item = ItemLoader(AuthorParseItem(), response)
        item.add_xpath('name', '//h1[contains(@class, "user-info__name")]/a/text()')
        item.add_xpath('nickname', '//a[contains(@class, "user-info__nickname")]/text()')
        item.add_xpath('info', '//li[contains(@class, "defination-list__item")]/span')
        yield item.load_item()
        author_links_posts = response.xpath('//a[contains(@class, "tabs-menu__item")]/@href').extract()[1]
        yield response.follow(author_links_posts, callback=self.parse)
