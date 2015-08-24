import lights
from clicktrack import *
import threading
import time, math
import alsaseq


class Program(object):
    def __init__(self, allLights):
        self.allLights = allLights

    def buttonPressed(self, n):
        print "Error, this function should be overridden!"

    def reset(self):
        pass

    def dark(self):
        for name, l in self.allLights.items():
            l.setController(
                lights.ConstantRGBController(0, 0, 0))

    def light(self):
        for name, l in self.allLights.items():
            l.setController(
                lights.ConstantRGBController(255, 255, 255))

    def setLights(self, lightList, controllerFunc):
        for l in lightList:
            self.allLights[l].setController(
                controllerFunc())

    def setLightsExcept(self, lightExceptList, controllerFunc):
        for name, l in self.allLights.items():
            if not name in lightExceptList:
                l.setController(controllerFunc())




alsaseq.client('Click', 1, 1, True)
alsaseq.connectto(1,128,0)

class ClickTrackProgram(Program):
    songStructure = SongStructure([
        SongSection("All", [
            SongRhythm(4, 1, 120, 120, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
            SongRhythm(4, 20, 120, 120, [(i, 76) for i in range(4)])
            ])])

    # (measure, beat, <function to execute>)
    events = []

    def __init__(self, *args, **kwargs):
        super(ClickTrackProgram, self).__init__(*args, **kwargs)
        self.events = [(0, i, self.dark) if i %2 == 0 else (0, i, self.light) for i in range(20*4)]
        #def blah(x):
            #print "Hello! " + str(x)
        #self.events = [(0, i, lambda: blah(i)) for i in range(20*4)]


    clickThread = None
    stopClick = False
    clickStartTime = 0
    def clickThreadRun(self):
        def noteOff(time):
            time_split = math.modf(time)
            time_i = int(time_split[1])
            time_f = int(time_split[0]*1e9)
            #print (time_i, time_f)
            return (7, 1, 0, 0, (time_i, time_f), (130, 0), (131, 0), (9, 75, 0, 0, 0));
        def noteOn(time, v, instrument):
            time_split = math.modf(time)
            time_i = int(time_split[1])
            time_f = int(time_split[0]*1e9)
            #print (time_i, time_f)
            return (6, 1, 0, 0, (time_i, time_f), (130, 0), (131, 0), (9, instrument, v, 0, 0));

        clicks = self.songStructure.getAllClicksSecs()
        clicks.sort()
        lookAheadTime = 10 # seconds
        self.clickStartTime = time.time()
        alsaseq.start()

        """
        print "-=---------------------------"
        print self.songStructure.totalNumMeasures()
        print self.songStructure.totalSecsLength()
        print len(clicks)
        print "-=---------------------------"
        """
        totalSongLenSecs = self.songStructure.totalSecsLength()

        for c in clicks:
            alsaseq.output(noteOn(c[0], 127, c[1] ));
            if self.stopClick:
                break
            while c[0] > (time.time() - self.clickStartTime) + lookAheadTime:
                time.sleep(.5)

        while (time.time() - self.clickStartTime) < totalSongLenSecs:
            time.sleep(.5)
        print "done with song!"
        alsaseq.stop()
        self.clickStartTime = 0
        self.stopClick = True

    def eventThreadRun(self):
        # convert measure, beat to sec
        eventsSecs = []
        for e in self.events:
            eventsSecs.append((self.songStructure.measureBeatToSec(e[0], e[1]), e[2]))

        #sort events
        eventsSecs.sort()


        # wait for clicktrack:
        while self.clickStartTime == 0 and not self.stopClick:
            time.sleep(0.01)

        for e in eventsSecs:
            t = time.time() - self.clickStartTime
            d = e[0] - t
            if d > 0:
                time.sleep(d)
            e[1]()
            if self.stopClick:
                break
        while not self.stopClick:
            time.sleep(0.5)
        self.dark()

    def reset(self):
        print "stopping clicktrack"
        self.stopClick = True
        self.dark()


    def buttonPressed(self, n):
        if n == 0:
            print "starting clicktrack!!"
            self.stopClick = False
            self.clickThread = threading.Thread(target=self.clickThreadRun)
            self.clickThread.start()
            self.eventThread = threading.Thread(target=self.eventThreadRun)
            self.eventThread.start()

        if n == 1:
            self.reset()



