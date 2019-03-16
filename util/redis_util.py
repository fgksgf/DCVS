import redis

from settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

# decode_responses = True:写入的键值对中的value为str类型，不加则写入的为字节类型
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

if __name__ == '__main__':
    redis_client.lpush('jd:items_urls', 'https://item.jd.com/100000822969.html')
