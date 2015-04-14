#!/usr/bin/python

import ConfigParser
import os
import sys
import RPi.GPIO as GPIO

# array that holds sound file names, and what pins they are attached to (loaded from config)
sounds = []
# what sound is currently active
activeSound = 0
# what is going to play the sounds (loaded from config)
aplay=""

def flashPickNew(calcSound):
  play(calcSound,0)

def flashWrong(wrongSound):
  play(wrongSound,0)

def flashCorrect(correctSound):
  play(correctSound,0)

# wait is a bool 1 wait for sound to finish 0 don't wait
def play(sound,wait):
  system("%s wav/%s" % (aplay, sound)

def setPins(pinConfig):
  for pin in pinConfig:
    GPIO.setup( pin['in'], GPIO.in, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect( pin['in'], GPIO.RISING)


if __name__ == '__main__':
  config = ConfigParser.SafeConfigParser()
  if os.path.isfile("run.cfg"):
    config.read("run.cfg")

    # load in each sound
    for sound in config.options('sounds'):
      sounds.append( eval( config.get('sounds', sound)))

    # configure each pin
    setPins(sounds)

    aplay   = config.get('config', 'pathToAplay')
    correct = config.get('config', 'correctSound')
    wrong   = config.get('config', 'wrongSound')
    calc    = config.get('config', 'calculatingSound')

    # main game loop
    while true:
      play(sounds[activeSound])
      i = getInput(aplay)
      if i == activeSound:
        flashCorrect(correct)
        flashPickNew(calc)
        activeSound = activeSound + 1
        if activeSound > len(sounds):
          activeSound = 0
      else:
        flashWrong(wrong)
