#!/usr/bin/python
#coding:utf-8

import smbus


class PCF8574(object) :
    def __init__(self, bus, addr) :
        self.bus = smbus.SMBus(bus)
        self.addr = addr
        self.value = 0
        self.bus.write_byte(self.addr, self.value)

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

