# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import json
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags

def get_address(address):
    return address[:3:2]

def photo(photo):
    link_list = []
    for itm in photo:
        itm = str(itm)
        matched = re.findall('https\S+', itm)
        link = matched[-1]
        link_list.append(link)
    return link_list



class ZillowParseItem(scrapy.Item):
    _id = scrapy.Field()
    city = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(input_processor=Compose(get_address))
    photos = scrapy.Field(input_processor=Compose(photo))
#
#
# class PaginationUserInstagram(scrapy.Item):
#     _id = scrapy.Field()
#     user_name = scrapy.Field(output_processor=TakeFirst())
#     user_id = scrapy.Field(output_processor=TakeFirst())
#     post_pub_date = scrapy.Field(output_processor=TakeFirst())
#     like_count = scrapy.Field(output_processor=TakeFirst())
#     post_photos = scrapy.Field()


# def clean_comments(comments):
#     replaces = (' ', '\n')
#
#     for itm in replaces:
#         comments = comments.replace(itm, '')
#     return comments


# def get_info(value):
#     list_params,  params = [], {}
#     for i in value:
#         list_params.append(remove_tags(i.replace(' ', '').replace('\n', '')))
#     params_key = list_params[::2]
#     list_params = list_params[1::2]
#
#     for i, item in enumerate(params_key):
#         params[item] = list_params[i]
#     return params


# class AvitoParseItem(scrapy.Item):
#     _id = scrapy.Field()
#     title = scrapy.Field(output_processor=TakeFirst())
#     author_name = scrapy.Field(output_processor=TakeFirst())
#     post_url = scrapy.Field(output_processor=TakeFirst())
#     images = scrapy.Field()
#     comments = scrapy.Field(input_processor=MapCompose(clean_comments))
#     author_url = scrapy.Field(output_processor=TakeFirst())
#
# class AuthorParseItem(scrapy.Item):
#     _id = scrapy.Field()
#     name = scrapy.Field(output_processor=TakeFirst())
#     nickname = scrapy.Field(output_processor=TakeFirst())
#     info = scrapy.Field(input_processor=Compose(get_info))






