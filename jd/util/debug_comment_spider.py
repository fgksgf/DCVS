"""
This program is to test if current urls and apis work,
and debug the comment spider.
"""

import json
import requests

from jd.items import CommentItem


def parse_comment(pid, page, score):
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
        comment_item = CommentItem()
        comment_item['pid'] = pid
        comment_item['comments'] = result['comments']
        print(comment_item)


if __name__ == '__main__':
    parse_comment(100003434266, 0, 0)
