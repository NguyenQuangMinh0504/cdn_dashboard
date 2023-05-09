import pymongo
mongo_client = pymongo.MongoClient(host="127.0.0.1")
domain_table = mongo_client["user"]["domain"]

