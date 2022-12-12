from flask import Flask, request
import DBCall

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
        success = DBCall.add_to_DB(input)
        if success:
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
  output = DBCall.sample()
  if output:
    return '{{ "success" : True, "samples" : {} }}'.format(output)
  else:
    return '{ "success" : False, "samples" : [] }'

@app.route("/state", methods=['GET'])
def state():
  count, pool_list = DBCall.state()
  return '{{ "len" : {0}, "samples" : {1} }}'.format(count, pool_list)

@app.route("/clear", methods=['GET'])
def clear():
  DBCall.clear_DB()
  return '{ "success" : True }'

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=False, port=80)