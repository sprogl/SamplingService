import psycopg2
import numpy.random as rnd
import os
import logging

DB_addr = os.getenv('DB_ADDR')
DB_port = os.getenv('DB_PORT')
DB_user = os.getenv('DB_USER')
DB_pass = os.getenv('DB_PASSWORD')
DB_database = os.getenv('DB_DATABASE')
Table_name = os.getenv('TABLE_NAME')

Query_Initial = f"""CREATE TABLE IF NOT EXISTS {Table_name} (
  id INT PRIMARY KEY,
  num INT UNIQUE NOT NULL
);"""
Query_Available_ID = f"SELECT count(id) FROM {Table_name}"
Query_Select = f"SELECT id, num FROM {Table_name} WHERE id IN %s;"
Query_Add = f"""INSERT INTO {Table_name} VALUES (
  ({Query_Available_ID}), %s
);"""
Query_Clear = f"DROP TABLE {Table_name};\n{Query_Initial}"

logging.basicConfig(filename='/var/log/db.log', encoding='utf-8', level=logging.DEBUG)

try:
  conn = psycopg2.connect(f"dbname='{DB_database}' user='{DB_user}' host='{DB_addr}' password='{DB_pass}'")
except:
  logging.error("unable to connect to the database")
  raise
else:
  cur = conn.cursor()

def init():
  try:
    cur.execute(Query_Initial)
  except:
    conn.commit()
    logging.error("unable to initialize the database")
    return False
  else:
    conn.commit()
    return True

def add(num):
  try:
    cur.execute(Query_Add, (num,))
  except psycopg2.errors.UniqueViolation:
    conn.commit()
    return False
  else:
    conn.commit()
    return True

def clear():
  try:
    cur.execute(Query_Clear)
  except:
    conn.commit()
    return False
  else:
    conn.commit()
    return True

def count():
  try:
    cur.execute(Query_Available_ID)
  except:
    logging.error("count function encountered an error")
    return None
  else:
    return cur.fetchone()[0]

def sample(indices):
  if not isinstance(indices, list):
    logging.error("wrong input format into sample function")
    return []
  try:
    list_of_indices = (tuple(indices),)
    cur.execute(Query_Select, list_of_indices)
  except:
    logging.error("sample function encountered an error")
    return []
  else:
    rows = cur.fetchall()
    samples = map(dict(rows).get, indices, indices)
    return list(samples)

def random_sample10():
  c = count()
  if c > 0:
    indices = rnd.randint(0, c, 10).tolist()
    return sample(indices)
  else:
    return []

init()