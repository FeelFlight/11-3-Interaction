import os
import json
import time
import random
import couchdb
from   flask          import Flask, jsonify, make_response, request
from   flask_httpauth import HTTPBasicAuth

app   = Flask(__name__)
auth  = HTTPBasicAuth()
couch = couchdb.Server('http://%s:5984/' % os.environ.get("COUCHDB_SERVER", "localhost"))


@auth.get_password
def get_password(username):
    if username == 'ansi':
        return 'test'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/api/v1.0/alarm/', methods=['GET'])
@auth.login_required
def get_wakeup():
    a = {"hour": "23", "minute": "42", "eabled": True}
    return make_response(jsonify(a), 200)


@app.route('/api/v1.0/alarm/', methods=['POST'])
@auth.login_required
def set_wakeup():
    a = {"hour": "12", "minute": "21", "eabled": True}
    return make_response(jsonify({'ok': 'Troy and Abed in the morning'}), 200)


@app.route('/api/v1.0/heating/', methods=['GET'])
@auth.login_required
def get_heating():
    a = [23, 42, 5]
    return make_response(jsonify(a), 200)


@app.route('/api/v1.0/heating/', methods=['POST'])
@auth.login_required
def set_heating():
    a = [0, 0, 0]
    return make_response(jsonify({'ok': 'Troy and Abed in the morning'}), 200)


if __name__ == '__main__':
    app.run(host="::", port=8036)
