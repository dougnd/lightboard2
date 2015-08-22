import lights
import programs
import sys
import subprocess
import time
import array
import threading
#import pkgutil
#import ipdb as pdb
#import time


allLights = {
    'frontLeftMagic': lights.DMXMagic(53),
    'frontLeft': lights.DMXPar(4),
    'frontSpencer': lights.DMXPar(1),
    'frontTanner': lights.DMXPar(7),
    'frontRight': lights.DMXPar(10),
    'backSpencer': lights.DMXPar(37),
    'backTanner': lights.DMXPar(40),
    'backDoug': lights.DMXPar(43),
    'backTravis': lights.DMXPar7Ch(46),
    'rear1': lights.DMXPar6Ch(13),
    'rear2': lights.DMXPar6Ch(19),
    'rear3': lights.DMXPar6Ch(25),
    'rear4': lights.DMXPar6Ch(31)
}


class Master:
    def __init__(self):
        self.allPrograms = programs.programList
        self.currentProgram = None
        self.currentProgramIndex = 0
        self.loadProgram(0)
        self.lastFrontPress = 0


    def loadProgram(self, index):
        #print 'loading ' + str(self.allPrograms[index])

        #reset old program:
        if self.currentProgram:
            self.currentProgram.reset()

        self.currentProgramIndex = index
        currentProgramModule = __import__('programs.' +
                                          self.allPrograms[index][1],
                                          fromlist=[
                                              self.allPrograms[index][1]])
        programClass = getattr(currentProgramModule,
                               self.allPrograms[index][2])
        self.currentProgram = programClass(allLights)
        self.currentProgram.reset()
        print "------------------"
        print self.allPrograms[index][0]
        #self.currentProgramModule.setAllLights(allLights)

    def btn(self,number):
        #print "Button " + str(number) + " pressed"
        #testProgram.buttonPressed(number)
        self.currentProgram.buttonPressed(number)

    def nextProgram(self):
        self.loadProgram((self.currentProgramIndex+1)%len(self.allPrograms))

    def prevProgram(self):
        self.loadProgram((self.currentProgramIndex-1)%len(self.allPrograms))

    def darkBtn(self):
        print "Dark"

        self.currentProgram.reset()
        for name, l in allLights.items():
            l.setController(lights.FadeInController(
                lights.ConstantRGBController(0,0,0), 0.1
            ))

    def frontBtn(self):
        if time.time() - self.lastFrontPress > 1.0:
            print "Front Spencer"
            frontLights = ['frontSpencer']
        else:
            print "All Front"
            frontLights = ['frontSpencer', 'frontTanner', 'frontLeft', 'frontRight']

        self.lastFrontPress = time.time()
        for name, l in allLights.items():
            l.setController(lights.FadeInController(
                lights.ConstantRGBController(0,0,0), 0.1
            ))
        for l in frontLights:
            allLights[l].setController(lights.FadeInController(
                lights.ConstantRGBController(255,255,255), 0.3
            ))



    def getProgramName(self):
        return self.allPrograms[self.currentProgramIndex][0]


    def runReal(self):
        self.dmxArray = array.array('B', [0]*100)
        self.dmxArray[0] = 255 # needed for spencer's second 4channel front light

        for name, l in allLights.items():
            l.dmxArray = self.dmxArray

        from ola.ClientWrapper import ClientWrapper
        targetFps = 24.0
        TICK_INTERVAL = 1000.0/targetFps
        wrapper = None

        def DmxSent(state):
            if not state.Succeeded():
                print "Error!"

        def SendDMXFrame():
            wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)

            for name, l in allLights.items():
                l.update()

            wrapper.Client().SendDmx(0, self.dmxArray, DmxSent)

        wrapper = ClientWrapper()
        wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
        wrapper.Run()
        print "What??"




