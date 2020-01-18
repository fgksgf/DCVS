# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from jd.items import ProductItem, PriceItem, CommentItem, CommentSummaryItem


class MongoPipeline(object):
    # def __init__(self, mongo_host, mongo_port, mongo_db, mongo_user, mongo_pwd):
    #     self.mongo_host = mongo_host
    #     self.mongo_port = mongo_port
    #     self.mongo_db = mongo_db
    #     self.mongo_user = mongo_user
    #     self.mongo_pwd = mongo_pwd
    #     self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
    #     self.db = self.client[self.mongo_db]
    #     self.db.authenticate(name=self.mongo_user, password=self.mongo_pwd, source="admin", mechanism="MONGODB-CR")

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        # self.db.authenticate(name=self.mongo_user, password=self.mongo_pwd, source="admin", mechanism="MONGODB-CR")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # mongo_host=crawler.settings.get('MONGO_HOST'),
            # mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            # mongo_user=crawler.settings.get('MONGO_USERNAME'),
            # mongo_pwd=crawler.settings.get('MONGO_PASSWORD'),
            mongo_url=crawler.settings.get('MONGODB_URL')
        )

    def open_spider(self, spider):
        self.db[ProductItem.collection].create_index([('pid', pymongo.ASCENDING)])
        self.db[PriceItem.collection].create_index([('pid', pymongo.ASCENDING)])
        self.db[CommentItem.collection].create_index([('pid', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ProductItem) or isinstance(item, PriceItem) or isinstance(item, CommentSummaryItem):
            self.db[item.collection].update({'pid': item.get('pid')},
                                            {'$set': item}, True)
        elif isinstance(item, CommentItem):
            self.db[item.collection].update({'pid': item.get('pid')},
                                            {'$addToSet': {'comments': {'$each': item['comments']}}}, True)
        return item
