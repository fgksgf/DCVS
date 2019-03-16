import pymongo

from model.jd.product import Product

client = pymongo.MongoClient('mongodb://localhost:27017/')


def get_product_by_pid(pid):
    collection = client['jd'].products
    return Product(collection.find_one({"pid": str(pid)}))
