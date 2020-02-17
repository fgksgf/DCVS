import pymongo
import redis

from model.jd.product import Product
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, MONGODB_URL

client = pymongo.MongoClient(MONGODB_URL)

# decode_responses = True:写入的键值对中的value为str类型，不加则写入的为字节类型
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)


def get_product_by_pid(pid):
    """
    从文档数据库中获取指定pid的商品信息

    :param pid: 要查询的pid
    :return: 若找到则返回商品类对象，否则返回None
    """
    collection = client['jd'].products
    item = collection.find_one({"pid": str(pid)})
    if item:
        return Product(item)
    else:
        return None


if __name__ == '__main__':
    redis_client.lpush('jd:items_urls', 'https://item.jd.com/100005638677.html')
