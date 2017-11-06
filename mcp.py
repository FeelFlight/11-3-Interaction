import os
import json
import time
import random
import couchdb
from   flask          import Flask, jsonify, make_response, request
from   flask_httpauth import HTTPBasicAuth

app   = Flask(__name__)
auth  = HTTPBasicAuth()
couch = couchdb.Server('http://couchdb:5984/')


@auth.get_password
def get_password(username):
    if username == 'ansi':
        return 'test'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/api/v1.0/wakeup/', methods=['GET'])
@auth.login_required
def get_wakeup():
    return make_response(jsonify({'error': 'Not yet implemented'}), 418)


@app.route('/api/v1.0/wakeup/', methods=['POST'])
@auth.login_required
def set_wakeup():
    return make_response(jsonify({'error': 'Not yet implemented'}), 418)


@app.route('/api/v1.0/heating/', methods=['GET'])
@auth.login_required
def get_heating():
    return make_response(jsonify({'error': 'Not yet implemented'}), 418)


@app.route('/api/v1.0/heating/', methods=['POST'])
@auth.login_required
def set_heating():
    return make_response(jsonify({'error': 'Not yet implemented'}), 418)


if __name__ == '__main__':
    app.run(host="::", port=8036)
