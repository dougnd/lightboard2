from flask import Flask
from flask import request
import json
import sys
import threading, Queue
import time

app = Flask(__name__)


class ConnectedDevices(dict):
    timeout = 4 # seconds
    def clean(self):
        for (d, t) in self.items():
            if time.time()-t > self.timeout:
                self.pop(d)
connectedDevices = ConnectedDevices()

buttonQueue = Queue.Queue()

@app.route("/")
def hello():
    return "Hello World!"



@app.route("/connected", methods=['GET', 'POST'])
def heartbeat():
    global connectedDevices
    if request.method == 'POST':
        connectedDevices[request.form['deviceId']] = time.time()
        return "Thanks!"
    else:
        connectedDevices.clean()
        return json.dumps(connectedDevices.keys())

@app.route("/buttonpress", methods=['POST'])
def buttonPress():
    global buttonQueue
    buttonQueue.put(request.form['buttonId'])
    return "Thanks!"


def doStuff():
    while True:
        print connectedDevices
        print buttonQueue.qsize()
        time.sleep(4)
    
    


if __name__ == "__main__":
    t = threading.Thread(target=app.run, kwargs={'debug': False})
    t.daemon = True
    t.start()
    doStuff()

        





