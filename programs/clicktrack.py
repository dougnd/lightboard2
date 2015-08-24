class SongRhythm:
    beatsPerMeasure = 4
    numberMeasures = 10
    initialTempo = 180
    finalTempo = 180
    metronomeClicks = [] # (<beat>, <soundfont num>)
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

    def getAllMetronomeClicks(self):
        clicks = []
        for i in range(self.numberMeasures):
            for c in self.metronomeClicks:
                clicks.append((c[0]+i*self.beatsPerMeasure, c[1]))
        return clicks
    def totalSecsLength(self):
        return self.beatToSec(self.totalBeatLength())
        
    def __init__(self,beatsPerMeasure, numberMeasures, initialTempo, finalTempo, metronomeClicks):
        self.beatsPerMeasure = beatsPerMeasure
        self.numberMeasures = numberMeasures
        self.initialTempo = initialTempo
        self.finalTempo = finalTempo
        self.metronomeClicks = metronomeClicks


class SongSection:
    name = ""
    rhythms =  []
    def __init__(self, name, rhythms):
        self.name = name
        self.rhythms = rhythms
    def getAllClicksSecs(self):
        currentTime = 0
        allClicks = []
        for r in self.rhythms:
            clicks = r.getAllMetronomeClicks()
            for c in clicks:
                allClicks.append((currentTime + r.beatToSec(c[0]), c[1]))
            currentTime+=r.beatToSec(r.totalBeatLength())
        return allClicks
    def measureBeatToSec(self, measure, beat):
        currentTime = 0
        currentMeasure = 0
        i = 0
        while measure > currentMeasure + self.rhythms[i].numberMeasures:
            currentMeasure += self.rhythms[i].numberMeasures
            currentTime += self.rhythms[i].totalSecsLength()
            i+=1
        return currentTime + self.rhythms[i].measureBeatToSec(measure-currentMeasure, beat)

    def totalNumMeasures(self):
        totalMeasures = 0
        for r in self.rhythms:
            totalMeasures+=r.numberMeasures
        return totalMeasures

    def totalSecsLength(self):
        totalLength = 0
        for r in self.rhythms:
            totalLength+=r.beatToSec(r.totalBeatLength())
        return totalLength


class SongStructure:
    sections = []
    def __init__(self, sections):
        self.sections =sections
    def getAllClicksSecs(self):
        currentTime = 0
        allClicks = []
        for s in self.sections:
            clicks = s.getAllClicksSecs()
            for c in clicks:
                allClicks.append((currentTime + c[0], c[1]))
            currentTime+=s.totalSecsLength()
        return allClicks
    def measureBeatToSec(self, measure, beat):
        currentTime = 0
        currentMeasure = 0
        i = 0
        while measure > currentMeasure + self.sections[i].totalNumMeasures():
            currentMeasure += self.sections[i].totalNumMeasures()
            currentTime += self.sections[i].totalSecsLength()
            i+=1
        return currentTime + self.sections[i].measureBeatToSec(measure-currentMeasure, beat)

    def totalNumMeasures(self):
        totalMeasures = 0
        for s in self.sections:
            totalMeasures+=s.totalNumMeasures()
        return totalMeasures

    def totalSecsLength(self):
        totalLength = 0
        for s in self.sections:
            totalLength+=s.totalSecsLength()
        return totalLength

 
