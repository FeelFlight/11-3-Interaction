import os
import json
import time
import random
import couchdb
import threading
import paho.mqtt.client as     mqtt


class Alarm(threading.Thread):

    def _getConfig(self):
        self._COUCHDB = os.environ.get("COUCHDB_SERVER", "localhost")
        self._MQTT    = os.environ.get("MQTT_SERVER",    "localhost")

    def __init__(self):
        random.seed
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._getConfig()
        self._couch                  = couchdb.Server('http://%s:5984/' % self._COUCHDB)
        self._mqclient               = mqtt.Client(clean_session=True)
        self._mqclient.connect(self._MQTT, 1883, 60)
        self._mqclient.loop_start()
        self.start()

    def _vibrate(self, userid):

        #for i in passenger["assets"]["blanket"]:
        #    mqclient.publish("blanket/%s/vibrate" % i, 500)

        self._mqclient.publish("blanket/B2000/vibrate", 250)
        pass

    def _check_alarm(self):
        db = self._couch['passengers']
        for p in db:
            if "alarm" in db[p] and db[p]['enabled'] is True:
                print("found alarm")

    def run(self):
        print("START")
        while True:
            try:
                time.sleep(10)
                self._check_alarm()
                print("Loop")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    print("Alarm started")
    a = Alarm()
    time.sleep(42)
