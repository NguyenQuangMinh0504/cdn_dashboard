import pymongo
import redis

mongo_client = pymongo.MongoClient(host="127.0.0.1")
domain_table_rdb = redis.Redis(host="127.0.0.1", db=0, port=6380)
domain_table = mongo_client["user"]["domain"]

