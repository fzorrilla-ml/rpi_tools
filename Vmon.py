#!/usr/bin/python

# The Raspberry Pi 1 B+ has an under voltage detect trigger which results in the power led 
# going off when voltage drops below about 4.65V.
# The signal is also available on a gpio line (GPIO35).

"""
The red power LEDs indicate that the Pi has an active power supply. In the Model A and Model B (rev 1) the LED is 
connected directly to the 3.3V supply. If it fails to light or flashes it indicates that there is a problem with 
the power supply.

In the later models (A+, B+, Pi 2 & Pi 3) the power LED is slightly more intelligent. it is connected to the 5V 
and will flash if the voltage drops below 4.63V.

"""

import RPi.GPIO as GPIO , time
from subprocess import call
import shlex
import sys

import signal

def handler(signum, frame):
#   call(shlex.split("echo -ne '\e[u''\e[0m'"))
   sys.exit()

signal.signal(signal.SIGINT, handler)

redLED=35
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLED, GPIO.IN)

powerlow=0
#call(shlex.split("echo -ne '\e[s'"))
while True:
   if(GPIO.input(redLED)==0):
      call(shlex.split("echo -ne '\e[s''\e[1;56H''\e[1;31m'POWER dipped below 4.63v'\e[u''\e[0m'"))
      powerlow += 1
   else:
      powerlow = 0
      call(shlex.split("echo -ne '\e[s''\e[1;78H''\e[1;31m'ON'\e[u''\e[0m'"))

   if (powerlow  > 3):
      break
    
   time.sleep(1)

#call(shlex.split("echo -ne '\e[u''\e[0m'"))
print "Low power for " + str(powerlow) + " seconds"
