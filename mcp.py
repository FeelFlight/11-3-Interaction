import os
import json
import time
import random
import couchdb
from   flask          import Flask, jsonify, make_response, request, render_template
from   flask_httpauth import HTTPBasicAuth

app          = Flask(__name__)
auth         = HTTPBasicAuth()
localcouch   = couchdb.Server('http://%s:5984/' % os.environ.get("LOCAL_COUCHDB_SERVER",   "localhost"))
centralcouch = couchdb.Server('http://%s:5984/' % os.environ.get("CENTRAL_COUCHDB_SERVER", "localhost"))


@auth.get_password
def get_password(username):
    if username == 'ansi':
        return 'test'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
def hello():
    return render_template('hello.html')


def getUserIdByName(name):
    return "276371592"


@app.route('/api/v1.0/alarm', methods=['GET', 'POST'])
@auth.login_required
def handle_alarm():

    userid = getUserIdByName(auth.username())

    if request.method == 'GET':
        db = localcouch['blanket']


        a = {"hour": "23", "minute": "42", "enabled": True}
        return make_response(jsonify(a), 200)
    else:
        r = request.get_json(silent=True)
        if r is not None:
            if "hour" in r and "minute" in r and "enabled" in r:
                return make_response(jsonify({'ok': 'Troy and Abed in the morning'}), 200)
            else:
                return make_response(jsonify({'error': 'wrong json object'}), 401)
        else:
            return make_response(jsonify({'error': 'not a json post'}), 401)


@app.route('/api/v1.0/heating', methods=['GET', 'POST'])
@auth.login_required
def handle_heating():

    if request.method == 'GET':
        a = [23, 42, 5]
        return make_response(jsonify(a), 200)
    else:
        r = request.get_json(silent=True)
        if r is not None:
            if len(r) == 3:
                return make_response(jsonify({'ok': 'Troy and Abed in the morning'}), 200)
            else:
                return make_response(jsonify({'error': 'wrong json object'}), 401)
        else:
            return make_response(jsonify({'error': 'not a json post'}), 401)


if __name__ == '__main__':
    app.run(host="::", port=8036)
