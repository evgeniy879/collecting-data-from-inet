# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags


def clean_comments(comments):
    replaces = (' ', '\n')

    for itm in replaces:
        comments = comments.replace(itm, '')
    return comments


def get_info(value):
    list_params,  params = [], {}
    for i in value:
        list_params.append(remove_tags(i.replace(' ', '').replace('\n', '')))
    params_key = list_params[::2]
    list_params = list_params[1::2]

    for i, item in enumerate(params_key):
        params[item] = list_params[i]
    return params


class AvitoParseItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    author_name = scrapy.Field(output_processor=TakeFirst())
    post_url = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    comments = scrapy.Field(input_processor=MapCompose(clean_comments))
    author_url = scrapy.Field(output_processor=TakeFirst())

class AuthorParseItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    nickname = scrapy.Field(output_processor=TakeFirst())
    info = scrapy.Field(input_processor=Compose(get_info))




