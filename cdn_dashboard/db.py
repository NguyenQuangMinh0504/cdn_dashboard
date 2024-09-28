import pymongo
from redis import Redis

mongo_client = pymongo.MongoClient(host="127.0.0.1")
domain_table_rdb = Redis(host="127.0.0.1", db=0, port=6379)
cache_key_setting_rdb = Redis(host="127.0.0.1", db=1, port=6379)
total_bytes_sent_rdb = Redis(host="127.0.0.1", db=2, port=6379)
domain_table = mongo_client["user"]["domain"]
user_table = mongo_client["user"]["user"]
