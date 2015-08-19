import requests, time, subprocess, threading
import Adafruit_BBIO.GPIO as GPIO

address = 'http://192.168.7.1:5000'


def tellServerButtonPress(btn):
    try:
        requests.post(address + '/buttonpress', data={'buttonId': btn})
    except requests.exceptions.ConnectionError:
        print "Connection Error, did not send " + btn + " press info!"

class ButtonHandler:
    def __init__(self, pin, callback):
        self.pin = pin
        self.callback = callback
        self.state = 0
        self.stateLock = threading.Lock()

    def handler(self, x):
        #print x + ':  ' + str(GPIO.input(x)) +   ' :   ' + str(time.time() - self.lastEventTime)
        self.stateLock.acquire()
        if self.state == 0 and GPIO.input(x) == 1:
            #print x + " was pressed"
            self.callback()
        self.state = GPIO.input(x)
        self.stateLock.release()


def setupPins(pins):
    # build node script to set pin direction:
    mux = 7
    pud = "pulldown"
    script = "var b = require('bonescript');"
    for (p, _) in pins:
        script += " b.pinMode('%s',b.INPUT,%i,'%s','fast');" % (p, mux, pud)
    command = ["node", "-e", script]
    subprocess.call(command, cwd="/usr/local/lib")

    # now use adafruit python lib
    for (p, callback) in pins:
        GPIO.setup(p, GPIO.IN)
        GPIO.add_event_detect(p, GPIO.BOTH)
        GPIO.add_event_callback(p, ButtonHandler(p, callback).handler)


print "Doing pin initialization..."
setupPins([
    ("P8_15", lambda : tellServerButtonPress('prevProgram')),
    ("P8_16", lambda : tellServerButtonPress('nextProgram')),
    ("P8_17", lambda : tellServerButtonPress('frontBtn')),
    ("P8_18", lambda : tellServerButtonPress('darkBtn')),
    ("P8_9", lambda : tellServerButtonPress('0')),
    ("P8_10", lambda : tellServerButtonPress('1')),
    ("P8_11", lambda : tellServerButtonPress('2')),
    ("P8_12", lambda : tellServerButtonPress('3')),
    ("P8_14", lambda : tellServerButtonPress('4'))
])
print "Done with pin initialization!"

while True:
    try:
        requests.post(address + '/connected', data={'deviceId': 'buttonBoard'})
    except requests.exceptions.ConnectionError:
        print "Connection Error..."
        time.sleep(5)

    time.sleep(1)





