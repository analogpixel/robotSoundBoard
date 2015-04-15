#!/usr/bin/python

import ConfigParser
import os
import sys
import RPi.GPIO as GPIO
import time


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
  os.system("%s './wav/%s'" % (aplay, sound))

def pinSetup(pinConfig):
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)

  for pin in pinConfig:
    GPIO.setup( pin['in'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect( pin['in'], GPIO.FALLING) # , bouncetime=1000)

# poll until you get something
def getInput(pinConfig):
  while True:
    for pin in pinConfig:
      #if GPIO.event_detected( int( pin['in'] ) ):
      if not GPIO.input(int( pin['in'] ) ):
        return int(pin['id'])

if __name__ == '__main__':
  config = ConfigParser.SafeConfigParser()
  if os.path.isfile("run.cfg"):
    config.read("run.cfg")

    # load in each sound
    for sound in config.options('sounds'):
      sounds.append( eval( config.get('sounds', sound)))

    # configure each pin
    pinSetup(sounds)

    aplay   = config.get('config', 'pathToAplay')
    correct = config.get('config', 'correctSound')
    wrong   = config.get('config', 'wrongSound')
    calc    = config.get('config', 'calculatingSound')

    # main game loop
    while True:
      for sound in sounds:
        match=False
        print sound
        while not match:
          play(sound['sound'],1)
          i = getInput(sounds)
          if i == sound['id']:
            flashCorrect(correct)
            flashPickNew(calc)
            match=True
          else:
            match=False
            flashWrong(wrong)
            #GPIO.cleanup()
            #sys.exit()
