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

s = SongSection("test", [
    SongRhythm(4, 50, 220, 220, [(0,75), (1,76), (2,76), (3,76)]),
    SongRhythm(4, 50, 220, 240, [(0,75), (1,76), (2,76), (3,76)]),
    SongRhythm(4, 50, 240, 240, [(0,75), (1,76), (2,76), (3,76)]),
    ])


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
