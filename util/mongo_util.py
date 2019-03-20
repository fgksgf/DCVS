import pymongo

from model.jd.product import Product

client = pymongo.MongoClient('mongodb://localhost:27017/')


def get_product_by_pid(pid):
    collection = client['jd'].products
    item = collection.find_one({"pid": str(pid)})
    if item:
        return Product(item)
    else:
        return None

