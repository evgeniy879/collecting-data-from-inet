# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class InstagramParsePipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client['instagram']

    def process_item(self, item, spider):
        collection_user = self.db['lenta_pagination']
        collection_user.insert_one(item)


class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item.get('post_photos', []):
            yield Request(url)
            # try:
            #     yield Request(url)
            # except ValueError as e:
            #     print(e)

    def item_completed(self, results, item, info):
        if results:
            item['post_photos'] = [itm[1] for itm in results]
        return item


# class AvitoParsePipeline:
#     def __init__(self):
#         client = MongoClient()
#         self.db = client['habr_']
#
#     def process_item(self, item, spider):
#         collection_author = self.db['author']
#         collection_post = self.db['post']
#         if 'author_url' in item:
#             collection_post.insert_one(item)
#         else:
#             collection_author.insert_one(item)