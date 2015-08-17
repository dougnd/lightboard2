import pyttsx

"""
e = pyttsx.init()
for v in e.getProperty('voices'):
    print v.id, v.languages, v.name

e.setProperty('voice', 'english-us')
e.say("If your system is already configured to load OSS drivers for your sound card then look at your current module loader configuration files. There will be entries for the OSS modules which will give you clues about which chipsets your sound cards have. Don't forget to disable these entries before reconfiguring things to load ALSA modules. This is a test.  How are you doing?")
e.runAndWait()
exit()
"""

import alsaseq
import time
import math

alsaseq.client('Click', 1, 1, True)
alsaseq.connectto(1,128,0)

class SongRhythm:
    beatsPerMeasure = 4
    numberMeasures = 10
    initialTempo = 180
    finalTempo = 180
    metronomeHits = [] # (<beat>, <soundfont num>)
    def totalBeatLength(self):
        return self.numberMeasures*self.beatsPerMeasure
    def measureBeatToBeat(self, measure, beat):
        return measure*self.beatsPerMeasure+beat
    def beatToSec(self, beat):
        beat = float(beat)
        return 60.0*(beat/self.initialTempo + 
                (1.0/self.finalTempo - 1.0/self.initialTempo)
                *beat*beat/2.0/self.totalBeatLength())
    def measureBeatToSec(self, measure, beat):
        return self.beatToSec(self.measureBeatToBeat(measure, beat))

    def getAllMetronomeHits(self):
        hits = []
        for i in range(self.numberMeasures):
            for h in self.metronomeHits:
                hits.append((h[0]+i*self.beatsPerMeasure, h[1]))
        return hits
        
    def __init__(self,beatsPerMeasure, numberMeasures, initialTempo, finalTempo, metronomeHits):
        self.beatsPerMeasure = beatsPerMeasure
        self.numberMeasures = numberMeasures
        self.initialTempo = initialTempo
        self.finalTempo = finalTempo
        self.metronomeHits = metronomeHits


r = SongRhythm(4, 40, 100, 200, [(0,76), (1,75), (2,75), (3,75)])
print r.totalBeatLength()
print r.beatToSec(10)
print r.beatToSec(10.0)
print r.beatToSec(0.0)
print r.measureBeatToSec(0,0)
print r.measureBeatToSec(1,0)
print r.measureBeatToSec(2,0)
print r.measureBeatToSec(0,3)
print r.measureBeatToSec(0,4)
print r.getAllMetronomeHits()

class SongSection:
    name = ""
    rhythms =  []
    def __init__(self, name, rhythms):
        self.name = name
        self.rhythms = rhythms
    def getAllHitsSecs(self):
        currentTime = 0
        allHits = []
        for r in self.rhythms:
            hits = r.getAllMetronomeHits()
            for h in hits:
                allHits.append((currentTime + r.beatToSec(h[0]), h[1]))
            currentTime+=r.beatToSec(r.totalBeatLength())
        return allHits
    def totalSecsLength(self):
        totalLength = 0
        for r in self.rhythms:
            totalLength+=r.beatToSec(r.totalBeatLength())
        return totalLength


class SongStructure:
    sections = []
    def __init__(self, sections):
        self.sections =sections
    def getAllHitsSecs(self):
        currentTime = 0
        allHits = []
        for s in self.sections:
            hits = s.getAllHitsSecs()
            for h in hits:
                allHits.append((currentTime + h[0], h[1]))
            currentTime+=s.totalSecsLength()
        return allHits
    def totalSecsLength(self):
        totalLength = 0
        for s in self.sections:
            totalLength+=s.totalSecsLength()
        return totalLength

def noteOff(time):
    time_split = math.modf(time)
    time_i = int(time_split[1])
    time_f = int(time_split[0]*1e9)
    print (time_i, time_f)
    return (7, 1, 0, 0, (time_i, time_f), (130, 0), (131, 0), (9, 75, 0, 0, 0));
def noteOn(time, v, instrument):
    time_split = math.modf(time)
    time_i = int(time_split[1])
    time_f = int(time_split[0]*1e9)
    print (time_i, time_f)
    return (6, 1, 0, 0, (time_i, time_f), (130, 0), (131, 0), (9, instrument, v, 0, 0));

alsaseq.start()



introTempo = 95
verseBeginTempo = 100
verseEndTempo = 105
chorusTempo = 115
solo2Tempo = 225

#introTempo = 120
#verseBeginTempo = 120
#verseEndTempo = 120
#chorusTempo = 120
#solo2Tempo = 120

s = SongStructure([
        SongSection("Intro", [
            SongRhythm(4, 1, introTempo, introTempo, [(i, 76) for i in range(4)] + [(0,50),(2,51)] ),
            SongRhythm(4, 1, introTempo, introTempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
            SongRhythm(4, 4, introTempo, verseBeginTempo, [(i, 76) for i in range(4)]),
        ]),
        SongSection("Verse1", [
            SongRhythm(4, 11, verseBeginTempo, verseEndTempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, verseEndTempo, chorusTempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Chorus1", [
            SongRhythm(4, 18, chorusTempo, chorusTempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, chorusTempo, verseBeginTempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Verse2", [
            SongRhythm(4, 11, verseBeginTempo, verseEndTempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, verseEndTempo, chorusTempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Chorus2", [
            SongRhythm(4, 12, chorusTempo, chorusTempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, chorusTempo, chorusTempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Bridge1", [
            SongRhythm(4, 24, chorusTempo, chorusTempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, chorusTempo, verseEndTempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Solo1", [
            SongRhythm(4, 7, verseEndTempo, verseEndTempo, [(i, 76) for i in range(4)]),
        ]),
        SongSection("Solo2", [
            SongRhythm(4, 7, verseEndTempo, solo2Tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, solo2Tempo, solo2Tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Bridge2", [
            SongRhythm(4, 23, solo2Tempo, solo2Tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, solo2Tempo, solo2Tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Chorus3", [
            SongRhythm(4, 18, solo2Tempo, solo2Tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, solo2Tempo, chorusTempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
    ])

"""
s = SongSection("test", [
    SongRhythm(4, 1, 120, 120, [(0,76), (0,50), (1,76), (2,76), (2,51), (3,76)]),
    SongRhythm(4, 1, 120, 120, [(0,76), (0,50), (1,76), (1,51), (2,76), (2,52), (3,76), (3,53)]),
    SongRhythm(4, 50, 120, 120, [(0,76), (1,76), (2,76), (3,76)]),
    SongRhythm(4, 50, 120, 120, [(0,76), (1,76), (2,76), (3,76)]),
    SongRhythm(4, 50, 120, 120, [(0,76), (1,76), (2,76), (3,76)]),
    ])
"""


for h in s.getAllHitsSecs():
    alsaseq.output(noteOn(h[0], 127, h[1] ));


totalTime = s.totalSecsLength()
print totalTime
time.sleep(totalTime)
exit()
bpm = 240
spb = 60.0/bpm
blen = .01
for i in range(0,10):
    print i;

    alsaseq.output(noteOn(i*spb));
    alsaseq.output(noteOff((i+blen) * spb));

time.sleep(5)


exit()
while 1:
    if alsaseq.inputpending():
        ev = alsaseq.input()
        print ev
        alsaseq.output( ev )
