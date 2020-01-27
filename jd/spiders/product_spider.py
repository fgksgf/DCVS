# -*- coding: utf-8 -*-
import json
from urllib import parse

import scrapy
from pyquery import PyQuery as pq
from scrapy_redis.spiders import RedisCrawlSpider

from jd.items import ProductItem, PriceItem, CommentSummaryItem
from jd.util.redis_util import client


class ProductSpider(RedisCrawlSpider):
    """
    The JD product spider is designed to crawling products' basic information,
    including description, price, image url and summary of comments.
    """

    name = 'product_spider'

    # set job queue's key
    redis_key = 'jd:items_urls'

    PRICE_URL = 'https://p.3.cn/prices/mgets?type=1&skuIds={pid}'
    COMMENT_URL = 'https://sclub.jd.com/comment/productPageComments.action?productId={pid}&page={page}' \
                  '&score={score}&sortType=5&pageSize=10'

    def parse(self, response):
        # url of jd product: https://item.jd.com/100000822969.html
        pid = response.url[20:-5]

        product_item = ProductItem()
        product_item['pid'] = pid
        d = pq(response.text)
        product_item['desc'] = d('.sku-name').text().strip()
        product_item['img_url'] = 'http:' + d('#spec-img').attr('data-origin').strip()
        attributes = []
        choices = []
        for i in range(1, 10):
            v = []
            query = '#choose-attr-' + str(i)
            if len(d(query)) != 0:
                attributes.append(d(query).attr('data-type'))
                for div in d(query + ' .item'):
                    v.append(pq(div).attr('data-value'))
                choices.append(v)
            else:
                break
        product_item['attributes'] = attributes
        product_item['choices'] = choices
        yield product_item
        yield scrapy.Request(self.PRICE_URL.format(pid=pid), callback=self.parse_price)

    def parse_price(self, response):
        # url of price: https://p.3.cn/prices/mgets?type=1&skuIds=100003434266
        pid = response.url[42:]

        price_item = PriceItem()
        price_item['pid'] = pid
        price_item['price'] = json.loads(response.text)[0]['p']
        yield price_item
        yield scrapy.Request(self.COMMENT_URL.format(pid=pid, page=0, score=0), callback=self.parse_comment_summary)

    def parse_comment_summary(self, response):
        param_dict = parse.parse_qs(parse.urlparse(response.url).query)
        pid = param_dict['productId'][0]

        result = json.loads(response.text)
        summary_item = CommentSummaryItem()
        summary_item['pid'] = pid
        summary_item['comment_summary'] = result.get('productCommentSummary')
        summary_item['hot_comments'] = result.get('hotCommentTagStatistics')
        yield summary_item

        # set a flag in redis to indicate that there are three types of comments to be crawled
        client.set(pid, 3)

        # add url of good comments, average comments and bad comments to redis, start from page 1
        client.lpush('jd:comment_urls', self.COMMENT_URL.format(pid=pid, page=1, score=1))
        client.lpush('jd:comment_urls', self.COMMENT_URL.format(pid=pid, page=1, score=2))
        client.lpush('jd:comment_urls', self.COMMENT_URL.format(pid=pid, page=1, score=3))
