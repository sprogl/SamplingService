import pymongo
import random
import os

DB_addr = os.getenv('DB_ADDR')
DB_port = os.getenv('DB_PORT')
DB_user = os.getenv('DB_USER')
DB_pass = os.getenv('DB_PASSWORD')
DB_database = os.getenv('DB_DATABASE')


client = pymongo.MongoClient("mongodb://{0}:{1}@{2}:{3}/{4}".format(DB_user, DB_pass, DB_addr, DB_port, DB_database))
db = client[DB_database]
pool_col = db['pool_col']
pool_col.insert_one({ "name" : "pool", "count" : 0, "list" : []})

query = { "name": "pool" }

def add_to_DB(input):
  pool = pool_col.find_one()
  pool_list = pool["list"]
  if input not in pool_list:
    pool_list.append(input)
    count = pool["count"] + 1
    pool_col.update_one(query, { "$set": { "count" : count, "list": pool_list } })
    return True
  else:
    return False

def sample():
  pool = pool_col.find_one()
  pool_list = pool["list"]
  count = pool["count"]
  if pool_list:
    output = []
    for _ in range(10):
      output.append(pool_list[random.randrange(count)])
  return output

def state():
  pool = pool_col.find_one()
  pool_list = pool["list"]
  count = pool["count"]
  return count, pool_list

def clear_DB():
  pool_col.update_one(query, { "$set": { "count" : 0, "list": [] } })