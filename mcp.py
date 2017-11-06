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


def getUserByUserName(name):

    try:
        local = localcouch['passenger']
    except Exception as e:
        local = localcouch.create('passenger')

    remote = centralcouch['passenger']

    id = "276371592"

    if id in local:
        return local[id]
    else:
        passenger = remote["276371592"]
        passenger["heating"] = {"shoulder": 0,
                                "hips": 0,
                                "feed": 0
                               }
        passenger["alarm"] = {"hour": "23",
                              "minute": "42",
                              "enabled": False}
        local.save(passenger)
        return passenger


def setAlarm(id, alarm):
    db = localcouch['passenger']
    passenger = db[id]
    passenger['alarm'] = alarm
    db.save(passenger)


def setHeating(id, heating):
    db = localcouch['passenger']
    passenger = db[id]
    passenger['heating']['shoulder'] = min(heating[0], 100)
    passenger['heating']['hips']     = min(heating[1], 100)
    passenger['heating']['feed']     = min(heating[2], 100)
    db.save(passenger)


@app.route('/api/v1.0/alarm', methods=['GET', 'POST'])
@auth.login_required
def handle_alarm():

    passenger = getUserByUserName(auth.username())

    if request.method == 'GET':
        return make_response(jsonify(passenger['alarm']), 200)
    else:
        r = request.get_json(silent=True)
        if r is not None:
            if "hour" in r and "minute" in r and "enabled" in r:
                setAlarm(passenger['_id'], r)
                return make_response(jsonify({'ok': 'Troy and Abed in the morning'}), 200)
            else:
                return make_response(jsonify({'error': 'wrong json object'}), 401)
        else:
            return make_response(jsonify({'error': 'not a json post'}), 401)


@app.route('/api/v1.0/heating', methods=['GET', 'POST'])
@auth.login_required
def handle_heating():

    passenger = getUserByUserName(auth.username())

    if request.method == 'GET':
        a = [passenger['heating']['shoulder'], passenger['heating']['hips'], passenger['heating']['feed']]
        return make_response(jsonify(a), 200)
    else:
        r = request.get_json(silent=True)
        if r is not None:
            if len(r) == 3:
                setHeating(passenger['_id'], r)
                return make_response(jsonify({'ok': 'Troy and Abed in the morning'}), 200)
            else:
                return make_response(jsonify({'error': 'wrong json object'}), 401)
        else:
            return make_response(jsonify({'error': 'not a json post'}), 401)


if __name__ == '__main__':
    app.run(host="::", port=8036)



"""

    def _check_for_alarm(self):
        if time.time() - self._update_alarm_time > 1:
            db = self._couch['blanket']

            for b in db:
                blanket = db[b]
                if "alarm" in blanket:
                    if "hour" in blanket['alarm'] and "minute" in blanket['alarm'] and "enabled" in blanket['alarm'] and blanket['alarm']['enabled'] is True:
                        print("ALARM found:%s" % b)

            self._update_alarm_time = time.time()

    def _update_heating(self):
        if time.time() - self._update_heating_time > 1:
            db = self._couch['blanket']

            for b in db:
                blanket = db[b]
                if "heating" in blanket:
                    if "shoulder" in blanket['heating']:
                        self._mqclient.publish("blanket/%s/heat/0" % b, blanket['heating']['shoulder'])
                    if "hips" in blanket['heating']:
                        self._mqclient.publish("blanket/%s/heat/1" % b, blanket['heating']['hips'])
                    if "feed" in blanket['heating']:
                        self._mqclient.publish("blanket/%s/heat/2" % b, blanket['heating']['feed'])

            self._update_heating_time = time.time()

    def _update_blouse(self):
        if time.time() - self._update_blouse_time > 1:
            self._update_blouse_time = time.time()

"""