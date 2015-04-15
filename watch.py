#!/usr/bin/env python

#GPIO input state monitor on the Raspberry Pi
#GPIO state - show the state of all the GPIO inputs on P1
#non GPIO pins shown as x
import RPi.GPIO as GPIO
print "Display the GPIO input pin states"
print "Ctrl C to stop"

pinout = [3,5,7,11,13,15,19,21,23,8,10,12,16,18,22,24,26]

GPIO.setmode(GPIO.BCM) # use real GPIO numbering

for pin in pinout: # set all pins to inputs
  GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True: # do forever
 needUpdate = False
 for check in pinout: # look at each input in turn
    if GPIO.input(check) :
      #print("Button %d is high" % check)
      pass
    else:
      latestState = 0
      print("Button %d is high" % check)
