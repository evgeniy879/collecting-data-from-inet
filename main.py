from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
# импорт логина и пароля из файла instagram_enter
# from avito_parse.instagram_enter import login, password

from avito_parse import settings
# from avito_parse.spiders.avito import AvitoSpider
from avito_parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule(settings)
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(InstagramSpider, login, password, ['artemzvn', 'arina_pechorina'])
    crawl_proc.start()
