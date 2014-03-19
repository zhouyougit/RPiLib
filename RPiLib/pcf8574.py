#!/usr/bin/python
#coding:utf-8

import smbus
import thread
import time

count = [0] * 8
class PCF8574(object) :
    def __init__(self, bus, addr) :
        self.bus = smbus.SMBus(bus)
        self.addr = addr
        self.value = 0
        self.bus.write_byte(self.addr, self.value)
        self.pwm = [None] * 8

    def output(self, pin, value) :
        if pin < 0 or pin > 7 :
            raise RuntimeError('pin(%s) is not exist' % (pin,))
        if value :
            self.value = self.value | (1 << pin)
        else :
            self.value = self.value & ~(1 << pin)
        self.bus.write_byte(self.addr, self.value)
    def input(self, pin) :
        if pin < 0 or pin > 7 :
            raise RuntimeError('pin(%s) is not exist' % (pin,))
        value = self.bus.read_byte(self.addr)
        if value & (1 << pin) :
            return 1
        else :
            return 0

    def outputByte(self, value) :
        self.bus.write_byte(self.addr, value)
        self.value = value

    def inputByte(self) :
        return self.bus.read_byte(self.addr)

    def clean(self) :
        self.bus.write_byte(self.addr, 0)
        self.value = 0

    def close(self) :
        self.bus.close()
        self.value = 0

    def startPWM(self, pin, freq = 1000, duty = 0) :
        if pin < 0 or pin > 7 :
            raise RuntimeError('pin(%s) is not exist' % (pin,))
        if self.pwm[pin] != None :
            return
        self.pwm[pin] = {'running' : True, 'pin' : pin, 'freq' : freq, 'duty' : duty, 'reqOn' : 0, 'reqOff' : 0}
        self.calculateTime(pin)
        print self.pwm[pin]
        thread.start_new_thread(self.pwmThread, (pin,))

    def stopPWM(self, pin) :
        if pin < 0 or pin > 7 :
            raise RuntimeError('pin(%s) is not exist' % (pin,))
        if self.pwm[pin] == None :
            return
        self.pwm[pin]['running'] = False
        self.pwm[pin] = None

    def calculateTime(self, pin) :
        pwm = self.pwm[pin]
        sliceTime = 10.0 / pwm['freq'] #sliceTIme = 1000 / pwm['freq'] * 100
        pwm['reqOn'] = (100 - pwm['duty']) * sliceTime / 1000.0
        pwm['reqOff'] = pwm['duty'] * sliceTime / 1000.0
        print pwm
        
    def changeFreq(self, pin, freq) :
        if pin < 0 or pin > 7 :
            raise RuntimeError('pin(%s) is not exist' % (pin,))
        if self.pwm[pin] == None :
            return
        if freq <= 0 : 
            return
        self.pwm[pin]['freq'] = freq
        calculateTime(pin)

    def changeDuty(self, pin, duty) :
        if pin < 0 or pin > 7 :
            raise RuntimeError('pin(%s) is not exist' % (pin,))
        if self.pwm[pin] == None :
            return
        if duty < 0 or duty > 100 :
            return
        self.pwm[pin]['duty'] = duty
        calculateTime(pin)

    def pwmThread(self, pin) :
        pwm = self.pwm[pin]
        while pwm['running'] :
            if pwm['duty'] < 100 :
                self.output(pin, 1)
                time.sleep(pwm['reqOn'])
            if pwm['duty'] > 0 :
                self.output(pin, 0)
                time.sleep(pwm['reqOff'])
            global count
            count[pin] += 1

        self.output(pin, 0)


if __name__ == '__main__' :
    b = PCF8574(1, 0x20)
    b.startPWM(0, 200, 1)
    b.startPWM(1, 200, 50)
    b.startPWM(2, 200, 99)
    
    while True :
        time.sleep(1)
        print count
        count = [0] * 8
