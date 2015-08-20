from flask import Flask
from flask import request
from master import Master
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
getProgramName = lambda : "Error: master unconnected"


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

def manageButtons(master):
    while True:
        btn = buttonQueue.get()
        print 'got ' + btn + '!'
        continue
        if btn == 'prevProgram':
            master.prevProgram()
        elif btn == 'nextProgram':
            master.nextProgram()
        elif btn == 'lightBtn':
            master.lightBtn()
        elif btn == 'darkBtn':
            master.darkBtn()
        elif btn == '0':
            master.btn(0)
        elif btn == '1':
            master.btn(1)
        elif btn == '2':
            master.btn(2)
        elif btn == '3':
            master.btn(3)
        elif btn == '4':
            master.btn(4)


def doStuff():
    while True:
        print connectedDevices
        time.sleep(4)
    
    


if __name__ == "__main__":
    t = threading.Thread(target=app.run, kwargs={'debug': False, 'host':'0.0.0.0'})
    t.daemon = True
    t.start()

    m = Master()
    t = threading.Thread(target=manageButtons, kwargs={'master': m})
    t.daemon = True
    t.start()

    m.runReal()
    #doStuff()

        





