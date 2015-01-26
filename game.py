#!/usr/bin/python


import ConfigParser
import os


# array that holds sound file names, and what pins they are attached to
sounds = []
# what sound is currently active
activeSound = 0

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

    # if testing on a non pi, then set option
    # to false
    if config.getboolean('config', "useGPIO"):
      import RPi.GPIO as GPIO

      setPins(sounds)
