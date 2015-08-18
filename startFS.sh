#!/bin/bash

#fluidsynth -C0 -R0 -d -g$1 -a alsa -o audio.alsa.device=hw:Series clickTrackSounds.sf2
fluidsynth -C1 -R0 -d -g$1 -a pulseaudio  clickTrackSounds.sf2
#/usr/share/sounds/sf2/FluidR3_GM.sf2
