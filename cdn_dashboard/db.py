import pymongo
mongo_client = pymongo.MongoClient(host="127.0.0.1")
domain_table = mongo_client["user"]["domain"]
# domain_table.insert_one({"foo": "bar"})
print(domain_table.find_one({}))
