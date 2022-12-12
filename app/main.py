from flask import Flask, request
import random
import os
import pymongo

DB_addr = os.getenv('DB_ADDR')
DB_port = os.getenv('DB_PORT')
DB_user = os.getenv('DB_USER')
DB_pass = os.getenv('DB_PASSWORD')
DB_database = os.getenv('DB_DATABASE')

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://{0}:{1}@{2}:{3}/{4}".format(DB_user, DB_pass, DB_addr, DB_port, DB_database))
db = client[DB_database]
pool_col = db['pool_col']
pool_col.insert_one({ "name" : "pool", "count" : 0, "list" : []})

query = { "name": "pool" }

@app.route("/add", methods=['POST'])
def add_post():
  if request.is_json:
    try:
      req = request.get_json()
    except:
      return 'bad request!', 400
    if list(req.keys()) == ['number']:
      input = req['number']
      if isinstance(input, int):
        pool = pool_col.find_one()
        pool_list = pool["list"]
        if input not in pool_list:
          pool_list.append(input)
          count = pool["count"] + 1
          pool_col.update_one(query, { "$set": { "count" : count, "list": pool_list } })
          return 'added!', 200
        else:
          return 'duplicate number!', 200
      else:
        return 'bad request!', 400
    else:
      return 'bad request!', 400
  else:
    return 'bad request!', 400
  
@app.route("/sample10", methods=['GET'])
def sample():
  pool = pool_col.find_one()
  pool_list = pool["list"]
  count = pool["count"]
  if pool_list:
    output = []
    for _ in range(10):
      output.append(pool_list[random.randrange(count)])
    out_string = '{{ "success" : True, "samples" : {} }}'.format(output)
    return out_string
  else:
    return '{ "success" : False, "samples" : [] }'

@app.route("/state", methods=['GET'])
def state():
  pool = pool_col.find_one()
  pool_list = pool["list"]
  count = pool["count"]
  return '{{ "len" : {0}, "samples" : {1} }}'.format(count, pool_list)

@app.route("/clear", methods=['GET'])
def clear():
  pool_col.update_one(query, { "$set": { "count" : 0, "list": [] } })
  return '{ "success" : True }'

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=False, port=80)