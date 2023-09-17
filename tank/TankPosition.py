#!/usr/bin/env python3
import serial, os, sys, json, time
from datetime import datetime

__TANK_POSITION_SERIAL_PORT__ = '/dev/ttyACM1'
__TANK_POSITION_SERIAL_PORT_BAUD_RATE__ = 9600

class TankPosition():
    serial = None
    HEADING = None
    X = None
    Y = None
    Z = None
    def __init__(self):
        self.serial = serial.Serial(port=__TANK_POSITION_SERIAL_PORT__, baudrate=__TANK_POSITION_SERIAL_PORT_BAUD_RATE__)

        print(self.serial.is_open)
        if self.serial.is_open:
            while True:
                size = self.serial.inWaiting()
                if size:
                    data = self.serial.read(size).decode().splitlines()
                    if data[0].startswith('X: '):
                        data[0] = ' '.join(x for x in data[0].split() if x)
                        self.X = data[0].split(' ')[1]
                        self.Y = data[0].split(' ')[3]
                        self.Z = data[0].split(' ')[5]
                        print(f'mag: {self.X},{self.Y},{self.Z}')
                    if data[1].startswith('Heading '):
                        self.HEADING = data[1].split(' ')[2]
                        print(f'heading: {self.HEADING}')
                else:
                    print('no data')
                time.sleep(1)
        else:
            print('serial not open')

    def info(self):
        info = {
        }
        return(info)

if __name__ == '__main__':
    p = TankPosition()
    while True:
        print(json.dumps(p.info()))
        time.sleep(1)
