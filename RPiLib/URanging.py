#!/usr/bin/python
#coding:utf-8

import RPi.GPIO as gp
import time

gp.setmode(gp.BOARD)

gp.setup(11, gp.OUT)
gp.setup(12, gp.IN)


stime = 0

def cb(channel) :
    global stime
    if stime == 0 :
        stime = time.time()
    else :
        sp = time.time() - stime
        stime = 0
        print sp * 34300 / 2

gp.add_event_detect(12, gp.BOTH, callback=cb)

while True :
    gp.output(11, gp.HIGH)
    time.sleep(0.00001)
    gp.output(11, gp.LOW)

    time.sleep(1)

