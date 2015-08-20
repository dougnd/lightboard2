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


        import usb.core
        import usb.util

# udmx stuff:

        while True:
            try:
                dev = usb.core.find(idVendor=0x16C0, idProduct=0x05DC)

                if dev is None:
                    raise ValueError('Device not found')

                udmxSetChannelRange = 2
                bmRequestType = 0x40
                targetFps = 24.0
                #targetFps = 1.0
                t = time.time()

                print "Ready."
                while True:
                    for name, l in allLights.items():
                        l.update()

                    dev.ctrl_transfer(bmRequestType, udmxSetChannelRange,
                            len(self.dmxArray), 0, self.dmxArray)

                    wait = 1.0/targetFps - time.time()+t
                    if wait > 0:
                        time.sleep(wait)
                    t = time.time()
            except (ValueError, usb.core.USBError):
                print "USB Error cannot find DMX controller!"
                time.sleep(1)
                print "Checking again..."


