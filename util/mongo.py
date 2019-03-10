import pymongo

if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    collection = client['jd'].products
    t = collection.find_one({"pid": "100000822969"})
    print(t)
    print(type(t))
