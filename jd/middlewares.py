import logging
import random
import time

import requests
from random_useragent.random_useragent import Randomize

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


# 代理中间件
class ProxyMiddleware:
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'http://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理: ' + proxy)
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


# 随机User-Agent中间件
class RandomUserAgentMiddleware:
    def __init__(self):
        self.r_agent = Randomize()
        self.platform = ['windows', 'mac', 'linux']

    def process_request(self, request, spider):
        random_user_agent = self.r_agent.random_agent('desktop', random.choice(self.platform))
        request.headers['User-Agent'] = random_user_agent


# 重试中间件
class MyRetryMiddleware(RetryMiddleware):
    logger = logging.getLogger(__name__)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            time.sleep(random.randint(3, 5))
            self.logger.warning('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            time.sleep(random.randint(3, 5))
            self.logger.warning('连接异常, 进行重试...')
            return self._retry(request, exception, spider)