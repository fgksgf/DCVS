import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
collection = client['jd'].products


def find_one_by_pid(pid):
    return collection.find_one({"pid": str(pid)})


if __name__ == '__main__':
    print(find_one_by_pid(100000822969))
