#!/usr/bin/python

import ConfigParser
import os
import sys
import RPi.GPIO as GPIO
import time
import smbus

# array that holds sound file names, and what pins they are attached to (loaded from config)
sounds = []
# what sound is currently active
activeSound = 0
# what is going to play the sounds (loaded from config)
aplay=""

i2c=smbus.SMBus(1)
addr=0x20
ledshadow=0
ledbit=[7, 6, 5, 4, 3, 2, 1, 0, 8, 9, 10, 11, 12, 13, 14, 15]

def flashPickNew(calcSound):
  play(calcSound,0)
  for i in range(15):
    lamp_set(i, 1)
    time.sleep(.1)
    lamp_set(i,0)

def flashWrong(wrongSound):
  play(wrongSound,0)

def flashCorrect(correctSound):
  play(correctSound,0)

# wait is a bool 1 wait for sound to finish 0 don't wait
def play(sound,wait):
  if wait:
    os.system("%s './wav/%s'" % (aplay, sound))
  else:
    os.system("%s './wav/%s' &" % (aplay, sound))

def lamp_set(n, state):
  global ledshadow
  if (state) :
    ledshadow |= 1<<(ledbit[n])
    i2c.write_byte_data(addr, ledshadow & 0xff, ledshadow >> 8)
  else :
    ledshadow &= ~(1<<ledbit[n])
    i2c.write_byte_data(addr, ledshadow & 0xff, ledshadow >> 8)
  return

def pinSetup(pinConfig, replay):
  GPIO.cleanup()
  GPIO.setmode(GPIO.BCM)

  GPIO.setup( replay , GPIO.IN, pull_up_down=GPIO.PUD_UP)

  for pin in pinConfig:
    GPIO.setup( pin['in'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect( pin['in'], GPIO.FALLING) # , bouncetime=1000)

# poll until you get something
def getInput(pinConfig, replay):
  while True:
    for pin in pinConfig:
      if not GPIO.input(replay):
        return replay
      if not GPIO.input(int( pin['in'] ) ):
        return int(pin['id'])

if __name__ == '__main__':
  config = ConfigParser.SafeConfigParser()
  if os.path.isfile("run.cfg"):
    config.read("run.cfg")

    # load in each sound
    for sound in config.options('sounds'):
      sounds.append( eval( config.get('sounds', sound)))


    aplay    = config.get('config', 'pathToAplay')
    correct  = config.get('config', 'correctSound')
    wrong    = config.get('config', 'wrongSound')
    calc     = config.get('config', 'calculatingSound')
    replayid = config.getint('config', 'replayid')

    # configure each pin
    pinSetup(sounds, replayid)

    lamp_set(15,1)

    # main game loop
    while True:
      for sound in sounds:
        match=False
        print sound
        while not match:
          play(sound['sound'],1)
          i = getInput(sounds,replayid)
          if i == replayid:
            continue
          elif i == sound['id']:
            flashCorrect(correct)
            flashPickNew(calc)
            match=True
          else:
            match=False
            flashWrong(wrong)
            #GPIO.cleanup()
            #sys.exit()
