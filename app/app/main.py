from flask import Flask, request
import app.core.database as DBCall

DBCall.init()

app = Flask(__name__)

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
        if DBCall.add(input):
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
def sample10():
  output = DBCall.random_sample10()
  if output:
    return '{{ "success" : True, "samples" : {} }}'.format(output)
  else:
    return '{ "success" : False, "samples" : [] }'

@app.route("/clear", methods=['GET'])
def clear():
  if DBCall.clear():
    return '{ "success" : True }'
  else:
    return '{ "success" : False }'

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=False, port=80)
  DBCall.cur.close()
  DBCall.conn.close()