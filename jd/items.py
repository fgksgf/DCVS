# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ProductItem(Item):
    collection = 'products'

    pid = Field()
    desc = Field()
    img_url = Field()
    price = Field()
    # 属性名称列表，例如颜色、尺码
    attributes = Field()
    # 可选择项目列表
    choices = Field()
    comment_summary = Field()
    hot_comments = Field()
    comments = Field()


class PriceItem(Item):
    collection = 'products'

    pid = Field()
    price = Field()


class CommentSummaryItem(Item):
    collection = 'products'

    pid = Field()
    comment_summary = Field()
    hot_comments = Field()


class CommentItem(Item):
    collection = 'products'

    pid = Field()
    comments = Field()
