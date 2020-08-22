from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avito_parse import settings
from avito_parse.spiders.habr import HabrSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(HabrSpider)
    crawl_proc.start()