# -*- coding: utf-8 -*-
import json
import scrapy
from urllib import parse
from scrapy_redis.spiders import RedisCrawlSpider
from jd.items import CommentItem
from jd.util.redis_util import client


class CommentSpider(RedisCrawlSpider):
    """
    The JD comment spider is designed to crawling products' detailed comments.
    """

    name = 'comment_spider'
    redis_key = 'jd:comment_urls'
    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={pid}&page={page}' \
                  '&score={score}&sortType=5&pageSize=10'

    def parse(self, response):
        # get parameter dict from url
        param_dict = parse.parse_qs(parse.urlparse(response.url).query)
        pid = param_dict['productId'][0]
        page = int(param_dict['page'][0])
        score = int(param_dict['score'][0])

        result = json.loads(response.text)
        comment_item = CommentItem()
        comment_item['pid'] = pid

        if len(result['comments']) != 0:
            comment_item['comments'] = result['comments']
            yield comment_item
            yield scrapy.Request(url=self.comment_url.format(pid=pid, page=page + 1, score=score),
                                 callback=self.parse)
        else:
            # when certain type of comments are crawled, the flag in redis is decreased by 1
            client.decr(pid, amount=1)
