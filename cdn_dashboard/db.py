import pymongo
from redis import Redis

mongo_client = pymongo.MongoClient(host="mongo")
domain_table_rdb = Redis(host="redis", db=0, port=6379)
cache_key_setting_rdb = Redis(host="redis", db=1, port=6379)
total_bytes_sent_rdb = Redis(host="redis", db=2, port=6379)
domain_table = mongo_client["user"]["domain"]
user_table = mongo_client["user"]["user"]
