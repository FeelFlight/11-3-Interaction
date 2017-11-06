import os
import json
import time
import random
import couchdb
from   flask            import Flask, jsonify, make_response, request, render_template
from   flask_httpauth   import HTTPBasicAuth
from   flask_cors       import CORS
import paho.mqtt.client as     mqtt

app          = Flask(__name__)
auth         = HTTPBasicAuth()
localcouch   = couchdb.Server('http://%s:5984/' % os.environ.get("LOCAL_COUCHDB_SERVER",   "localhost"))
centralcouch = couchdb.Server('http://%s:5984/' % os.environ.get("CENTRAL_COUCHDB_SERVER", "localhost"))
mqclient     = mqtt.Client(clean_session=True)
mqclient.connect(os.environ.get("MQTT_SERVER", "localhost"), 1883, 60)
mqclient.loop_start()

CORS(app)

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

    id = "276371592" # TODO: Query DB

    if id in local:
        return local[id]
    else:
        passenger = remote[id]
        passenger["heating"] = {"chest": 0,
                                "hip": 0,
                                "feet": 0
                                }
        passenger["alarm"] = {"hour": "23",
                              "minute": "42",
                              "enabled": False
                              }
        passenger["assets"] = {"blanket": ["B1000", "B2000"],
                               "shoe": "nix"
                               }
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
    passenger['heating']['chest'] = min(heating[0], 100)
    passenger['heating']['hip']   = min(heating[1], 100)
    passenger['heating']['feet']  = min(heating[2], 100)
    db.save(passenger)

    for i in passenger["assets"]["blanket"]:
        mqclient.publish("blanket/%s/heat/0" % i, passenger['heating']['chest'])
        mqclient.publish("blanket/%s/heat/1" % i, passenger['heating']['hip'])
        mqclient.publish("blanket/%s/heat/2" % i, passenger['heating']['feet'])

@app.route('/api/v1.0/alarm', methods=['GET', 'POST'])
@auth.login_required
def handle_alarm():

    #print(request.headers)
    #print(request.get_json(silent=True))

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
        a = [passenger['heating']['chest'], passenger['heating']['hip'], passenger['heating']['feet']]
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

    try:
        local = localcouch['passenger']
    except Exception as e:
        local = localcouch.create('passenger')

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
"""