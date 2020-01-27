import redis
from jd.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

# decode_responses = True:写入的键值对中的value为str类型，不加则写入的为字节类型
client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

if __name__ == '__main__':
    # put jd product url in redis
    client.lpush('jd:items_urls', 'https://item.jd.com/100002355147.html')
    # client.set('100000323510', 4)
    # t = client.get('100000323510')
    # print(t)
    # print(type(t))
    # client.decr('100000323510', amount=1)
    # print(client.get('100000323510'))
