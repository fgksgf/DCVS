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


if __name__ == '__main__':
    product = get_product_by_pid(100000822981)
    good = []
    general = []
    poor = []
    for c in product.good_comments:
        good.append(c.votes)
    for c in product.general_comments:
        general.append(c.votes)
    for c in product.poor_comments:
        poor.append(c.votes)

    print(set(good))
    print(set(general))
    print(set(poor))
