import os
import json
import time
import random
import couchdb
import threading
import paho.mqtt.client as     mqtt


class Alarm(threading.Thread):

    def _getConfig(self):
        self._CENTRAL_COUCHDB = os.environ.get("CENTRAL_COUCHDB_SERVER", "localhost")
        self._LOCAL_COUCHDB   = os.environ.get("LOCAL_COUCHDB_SERVER",   "localhost")
        self._MQTT            = os.environ.get("MQTT_SERVER",            "localhost")

    def __init__(self):
        random.seed
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._getConfig()
        self._central_couch          = couchdb.Server('http://%s:5984/' % self._CENTRAL_COUCHDB)
        self._local_couch            = couchdb.Server('http://%s:5984/' % self._LOCAL_COUCHDB)
        self._mqclient               = mqtt.Client(clean_session=True)
        self._mqclient.connect(self._MQTT, 1883, 60)
        self._mqclient.loop_start()
        self.start()

    def _vibrate(self, userid):
        #for i in passenger["assets"]["blanket"]:
        #    mqclient.publish("blanket/%s/vibrate" % i, 500)
        pass

    def _check_alarm(self):
        db = self._local_couch['passenger']
        for p in db:
            if "alarm" in db[p] and db[p]['alarm']['enabled'] is True:
                print("found alarm")

    def _check_display(self):
        db = self._central_couch['orders']
        for i in db:
            o = db[i]
            if o['new'] is True:
                print(json.dumps(db[i], indent=2))
                self._mqclient.publish("blouse/000186A0/display/intensity", 100)
                self._mqclient.publish("blouse/000186A0/display/txt/0", "================")
                self._mqclient.publish("blouse/000186A0/display/txt/1", "||  NEW ORDER ||")
                self._mqclient.publish("blouse/000186A0/display/txt/2", "||            ||")
                self._mqclient.publish("blouse/000186A0/display/txt/3", "||    Coke    ||")
                self._mqclient.publish("blouse/000186A0/display/txt/4", "||  Seat: 23F ||")
                self._mqclient.publish("blouse/000186A0/display/txt/5", "||Ansi Schmidt||")
                self._mqclient.publish("blouse/000186A0/display/txt/6", "||            ||")
                self._mqclient.publish("blouse/000186A0/display/txt/7", "================")
                o['new'] = False
                db.save(o)

    def run(self):
        print("START")
        while True:
            self._check_alarm()
            self._check_display()
            time.sleep(1)


if __name__ == '__main__':
    print("Alarm started")
    a = Alarm()
    time.sleep(120000)
