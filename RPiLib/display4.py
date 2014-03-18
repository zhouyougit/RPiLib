#!/usr/bin/python

import RPi.GPIO as gp
import time
import thread

bgThread = None
isRunning = False
data = [0xff, 0xff, 0xff, 0xff]


NUM = [0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90]
MINUS = 0xbf
DOT = 0x7f

PINS = None
DAT = None
CLK = None
ST = None

GPIO = 0
I2C = 1
IO = None

OUTPUT = None

def setup(io, mode = None, pins = []) :
    global IO, OUTPUT, PINS, DAT, CLK, ST
    if io != GPIO and io != I2C :
        raise RuntimeError('io is only GPIO or I2C')
    IO = io
    if len(pins) != 7 :
        raise RuntimeError('need 7 pins')
    PINS = pins

    if IO == GPIO :
        if mode != gp.BOARD and mode != gp.BCM :
            raise RuntimeError('gpio mode is only board or bcm')
        gp.setmode(mode)
        for pin in PINS :
            gp.setup(pin, gp.OUT)
        OUTPUT = gp.output
        OUTPUT(PINS[0], 1)
        OUTPUT(PINS[1], 1)
        OUTPUT(PINS[2], 1)
        OUTPUT(PINS[3], 1)
    DAT = pins[4]
    CLK = pins[5]
    ST = pins[6]

def sleepMS() :
    time.sleep(0.05)

def dispOne(value) :
    for i in range(8) :
        OUTPUT(CLK, 0)
        OUTPUT(DAT, (value & 0x80 >> i) > 0)
        OUTPUT(CLK, 1)
    OUTPUT(ST, 0)
    OUTPUT(ST, 1)

def bgTask() :
    oldPin = PINS[0]
    while isRunning :
        for i in range(4) :
            OUTPUT(oldPin, 1)
            oldPin = PINS[i]
            dispOne(data[i])
            OUTPUT(PINS[i], 0)
            time.sleep(0.002)

def close() :
    data = [0xff, 0xff, 0xff, 0xff]
    sleepMS()
    isRunning = False
    bgThread = None
    if IO == GPIO :
        gp.cleanup()

def display(value) :
    if IO == None :
        raise RuntimeError('need setup first')
    if value > 9999 or value < -999 :
        raise RuntimeError('value(%s) is too long' % (value,))
    nums = [0xff, 0xff, 0xff, 0xff]
    vs = str(value)
    lvs = len(vs)
    if '.' in vs :
        lvs -= 1
    if lvs < 4 :
        idx = 4 - lvs
    else :
        idx = 0
    hasDot = False
    for c in vs :
        if c == '.' :
            nums[idx - 1] &= DOT
            hasDot = True
        elif c == '-' :
            nums[idx] = MINUS
            idx += 1
        else :
            nums[idx] = NUM[int(c)]
            idx += 1
        if idx == 4 :
            break
    if not hasDot :
        nums[3] &= DOT
    
    global data, bgThread, isRunning
    data = nums
    if bgThread == None :
        isRunning = True
        bgThread = thread.start_new_thread(bgTask, ())

if __name__ == '__main__' :
    setup(GPIO, mode = gp.BOARD, pins = [11, 12, 13, 15, 16, 18, 22])
    display(12.32)
    time.sleep(1000)
