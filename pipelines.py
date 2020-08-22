# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class AvitoParsePipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client['habr_']

    def process_item(self, item, spider):
        collection_author = self.db['author']
        collection_post = self.db['post']
        if 'author_url' in item:
            collection_post.insert_one(item)
        else:
            collection_author.insert_one(item)
