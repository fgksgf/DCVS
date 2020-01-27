# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from jd.items import ProductItem, PriceItem, CommentItem, CommentSummaryItem


class MongoPipeline(object):
    """
    Mongodb pipeline, store crawled data into mongodb.
    """

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        # self.db.authenticate(name=self.mongo_user, password=self.mongo_pwd, source="admin", mechanism="MONGODB-CR")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
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
