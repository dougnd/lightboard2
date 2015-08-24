import common, math, lights, random, time
from clicktrack import *



class IAmOneProgram(common.ClickTrackProgram):
    tempo = 80
    songStructure = SongStructure([
        SongSection("Intro", [
            SongRhythm(4, 1, tempo, tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
            SongRhythm(4, 6, tempo, tempo, [(i, 76) for i in range(4)])
        ]),
        SongSection("Verse1", [
            SongRhythm(4, 21, tempo, tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, tempo, tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Chorus1", [
            SongRhythm(4, 7, tempo, tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, tempo, tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Verse2", [
            SongRhythm(4, 21, tempo, tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, tempo, tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Chorus2", [
            SongRhythm(4, 7, tempo, tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, tempo, tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Bridge", [
            SongRhythm(4, 7, tempo, tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, tempo, tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Chorus3", [
            SongRhythm(4, 15, tempo, tempo, [(i, 76) for i in range(4)]),
            SongRhythm(4, 1, tempo, tempo, [(i, 76) for i in range(4)] + [(i, 50+i) for i in range(4)] ),
        ]),
        SongSection("Verse3", [
            SongRhythm(4, 22, tempo, tempo, [(i, 76) for i in range(4)]),
        ])])

    def __init__(self, *args, **kwargs):
        def fadeLights(lightList, r,g,b, t):
            def fun():
                self.setLights(lightList, lambda: lights.FadeInController(
                    lights.ConstantRGBController(r,g,b), t))
            return fun
        def fadeLightsExcept(lightList, r,g,b, t):
            def fun():
                self.setLightsExcept(lightList, lambda:  lights.FadeInController(
                    lights.ConstantRGBController(r,g,b), t))
            return fun
        super(IAmOneProgram, self).__init__(*args, **kwargs)
        self.events = [
            # Intro
            (1, 0, fadeLights(['backSpencer'], 0,0,255,4)),
            (1, 0, fadeLights(['frontSpencer'], 100,0,100,4)),
            # verse
            (7, 0, fadeLights(['backDoug'], 0,0,255,1)),
            (7, 0, fadeLights(['backTanner', 'backTravis'], 0,0,200,8)),
            (13, 0, fadeLights(['frontSpencer'], 200,200,200,1)),
            (13, 0, fadeLights(['rear1', 'rear2', 'rear3', 'rear4'], 0,0,255,1)),
            (13, 0, fadeLights(['rear1', 'rear2', 'rear3', 'rear4'], 0,0,255,1)),
            # chorus
            (29, 0, fadeLightsExcept(['frontSpencer'], 255,100,0,0)),
            (29, 0, fadeLights(['frontSpencer'], 255,255,255,1)),
            # verse
            (37, 0, fadeLightsExcept(['frontSpencer'], 0,0,150,0)),
            (37, 0, fadeLights(['frontSpencer'], 150,150,255,1)),
            # chorus
            (59, 0, fadeLightsExcept(['frontSpencer'], 255,100,0,0)),
            (59, 0, fadeLights(['frontSpencer'], 255,255,255,1)),
            # bridge
            (67, 0, fadeLightsExcept(['frontTanner'], 50,255,50,0)),
            (67, 0, fadeLights(['frontTanner'], 255,255,255,1)),
            # bridge2
            (75, 0, fadeLightsExcept(['frontTanner'], 255,100,0,0)),
            (75, 0, fadeLights(['frontTanner'], 255,255,255,1)),
            # chorus
            (83, 0, fadeLightsExcept(['frontSpencer'], 255,100,0,0)),
            (83, 0, fadeLights(['frontSpencer'], 255,255,255,1)),
            # verse
            (91, 0, fadeLightsExcept(['frontSpencer'], 0,0,150,0)),
            (91, 0, fadeLights(['frontSpencer'], 150,150,255,1))

        ]






   
"""
    def intro(self, n):
        if n == 1:
            self.dark()
            self.allLights['backSpencer'].setController(
                lights.FadeInController(
                    lights.ConstantRGBController(
                        40, 0, 255
                    ), 1.0
                )
            )
        if n == 2:
            self.allLights['backDoug'].setController(
                lights.FadeInController(
                    lights.ConstantRGBController(
                        40, 0, 255
                    ), 1.0
                )
            )


    def verse(self, n):
        lightsToEnable = ['backDoug', 'backSpencer', 'backTravis', 'backTanner',
                          'rear1', 'rear2', 'rear3', 'rear4']
        def blueLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(.1,1), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,1), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,1), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255))
                ), 1.4
            )

        if n == 1:
            for name, l in self.allLights.items():
                if name in lightsToEnable:
                    l.setController(HitController(
                        blueLight()))
                else:
                    l.setController(HitController(lights.FadeInController(
                        lights.ConstantRGBController(0,0,0), 1.0)))
        if n == 2:
            self.allLights['frontSpencer'].setController(
                HitController(lights.FadeInController(
                    lights.ConstantRGBController(
                        180, 50, 255
                    ), 1.0
                ))
            )
        if n > 2:
            for name, l in self.allLights.items():
                if n%2 == 1:
                    l.controller.preHit()
                else:
                    l.controller.hit()

    def chorus(self, n):
        def redLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70))
                ), .2
            )
        for name, l in self.allLights.items():
            l.setController(redLight())
            #l.controller.lastRGB = (255,255,255)

        self.allLights['frontSpencer'].setController(
            lights.FadeInController(
                lights.ConstantRGBController(
                    255, 255, 255
                ), .2
            )
        )

    def bridge(self, n):
        def greenLight():
            return lights.FadeInController(
                lights.SineRGBController(
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(5,70), random.uniform(180,255)),
                    (random.uniform(.1,3), random.uniform(0,2*math.pi),
                        random.uniform(50,100), random.uniform(0,70))
                ), .2
            )
        for name, l in self.allLights.items():
            l.setController(greenLight())
            #l.controller.lastRGB = (255,255,255)

    def outro(self, n):
        for name, l in self.allLights.items():
            l.setController(lights.FadeInController(
                lights.ConstantRGBController(0,0,0), 2.0
            ))
            l.controller.lastRGB = (255,255,255)


    def buttonPressed(self, n):
        if hasattr(self, 'lastn') and self.lastn == n:
            self.btnCount += 1
        else:
            self.btnCount = 1

        btnmap = {
            0: self.intro,
            1: self.verse,
            2: self.chorus,
            3: self.bridge,
            4: self.outro
        }
        try:
            btnmap[n](self.btnCount)
        except KeyError:
            pass
        self.lastn = n
        """

