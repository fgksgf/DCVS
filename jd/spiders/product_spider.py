# -*- coding: utf-8 -*-
import json
from urllib import parse

import scrapy
from pyquery import PyQuery as pq
from scrapy_redis.spiders import RedisCrawlSpider

from jd.items import ProductItem, PriceItem, CommentSummaryItem
from jd.util.redis_util import client


# Master
class ProductSpider(RedisCrawlSpider):
    name = 'product_spider'
    redis_key = 'jd:items_urls'
    price_url = 'https://p.3.cn/prices/mgets?type=1&skuIds={pid}'
    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={pid}&page={page}' \
                  '&score={score}&sortType=5&pageSize=10'

    def parse(self, response):
        # url: https://item.jd.com/100000822969.html
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
        yield scrapy.Request(self.price_url.format(pid=pid), callback=self.parse_price)

    def parse_price(self, response):
        # url: https://p.3.cn/prices/mgets?type=1&skuIds=100003434266
        pid = response.url[42:]

        price_item = PriceItem()
        price_item['pid'] = pid
        price_item['price'] = json.loads(response.text)[0]['p']
        yield price_item
        yield scrapy.Request(self.comment_url.format(pid=pid, page=0, score=0), callback=self.parse_comment_summary)

    def parse_comment_summary(self, response):
        param_dict = parse.parse_qs(parse.urlparse(response.url).query)
        pid = param_dict['productId'][0]

        result = json.loads(response.text)
        summary_item = CommentSummaryItem()
        summary_item['pid'] = pid
        summary_item['comment_summary'] = result.get('productCommentSummary')
        summary_item['hot_comments'] = result.get('hotCommentTagStatistics')
        yield summary_item

        # 在数据库中设置一个标志，表示该商品的评论信息正在爬取
        client.set(pid, 3)

        # 分别将好评、中评、差评评论url加入redis队列
        client.lpush('jd:comment_urls', self.comment_url.format(pid=pid, page=1, score=1))
        client.lpush('jd:comment_urls', self.comment_url.format(pid=pid, page=1, score=2))
        client.lpush('jd:comment_urls', self.comment_url.format(pid=pid, page=1, score=3))
