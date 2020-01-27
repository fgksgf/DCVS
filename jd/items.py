# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ProductItem(Item):
    # the collection name in mongodb
    collection = 'products'

    # product id
    pid = Field()
    # description
    desc = Field()
    # image url
    img_url = Field()
    # price
    price = Field()
    # list of product's attributes, such as color and size
    attributes = Field()
    # options of above each attribute, such as 'red' or 'XL'
    choices = Field()
    # summary of comments
    comment_summary = Field()
    # list of hot comments
    hot_comments = Field()
    # detailed comments
    comments = Field()


class PriceItem(Item):
    # the collection name in mongodb
    collection = 'products'

    pid = Field()
    price = Field()


class CommentSummaryItem(Item):
    # the collection name in mongodb
    collection = 'products'

    pid = Field()
    comment_summary = Field()
    hot_comments = Field()


class CommentItem(Item):
    # the collection name in mongodb
    collection = 'products'

    pid = Field()
    comments = Field()
