"""
This program is to test if current urls and apis work,
and debug the product spider.
"""

import json

import requests
from pyquery import PyQuery as pq

from jd.items import ProductItem, PriceItem, CommentSummaryItem


def parse(url):
    d = pq(url=url)
    product_item = ProductItem()
    pid = url[20:-5]
    product_item['pid'] = pid
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
    print(product_item)


def parse_price(url):
    # url: https://p.3.cn/prices/mgets?type=1&skuIds=100003434266
    response = requests.get(url)
    if response.status_code == 200:
        price_item = PriceItem()
        pid = url[42:]
        price_item['pid'] = pid
        price_item['price'] = json.loads(response.text)[0]['p']
        print(price_item)
    else:
        print(response.status_code)


def parse_comment_summary(pid, page, score):
    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={pid}&page={page}' \
                  '&score={score}&sortType=5&pageSize=10'
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Referer': 'https://item.jd.com/1.html',
    }

    url = comment_url.format(pid=pid, page=page, score=score)
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        result = json.loads(response.text)
        summary_item = CommentSummaryItem()
        summary_item['pid'] = pid
        summary_item['comment_summary'] = result.get('productCommentSummary')
        summary_item['hot_comments'] = result.get('hotCommentTagStatistics')
        print(summary_item)
    else:
        print(response.status_code)


if __name__ == '__main__':
    parse('https://item.jd.com/100003434266.html')
    parse_price('https://p.3.cn/prices/mgets?type=1&skuIds=100003434266')
    # parse_comment_summary(100003434266, 0, 0)
