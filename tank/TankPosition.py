#!/usr/bin/env python3
import serial, os, sys, json, time, threading
from datetime import datetime

if not 'ARDUINO_DEVICE' in os.environ.keys():
    __TANK_POSITION_SERIAL_PORT__ = '/dev/ttyACM0'
else:
    __TANK_POSITION_SERIAL_PORT__ = os.environ['ARDUINO_DEVICE'] 

__TANK_POSITION_SERIAL_PORT_BAUD_RATE__ = 9600

class TankPosition():
    serial = None
    HEADING = None
    X = None
    Y = None
    Z = None

    def poll(self):
        if self.serial.is_open:
            while True:
                size = self.serial.inWaiting()
                if size:
                    data = self.serial.read(size).decode().splitlines()
                    if len(data) == 2:
                        if data[0].startswith('X: '):
                            data[0] = ' '.join(x for x in data[0].split() if x)
                            self.X = data[0].split(' ')[1]
                            self.Y = data[0].split(' ')[3]
                            self.Z = data[0].split(' ')[5]
                            #print(f'mag: {self.X},{self.Y},{self.Z}')
                        if data[1].startswith('Heading '):
                            self.HEADING = data[1].split(' ')[2]
                            #print(f'heading: {self.HEADING}')
                time.sleep(0.5)
        else:
            print('serial not open')

    def __init__(self):
        self.serial = serial.Serial(port=__TANK_POSITION_SERIAL_PORT__, baudrate=__TANK_POSITION_SERIAL_PORT_BAUD_RATE__)
        t1 = threading.Thread(target=self.poll, daemon=True)
        t1.start()


    def info(self):
        if self.X == None or self.Y == None or self.Z == None or self.HEADING == None:
            return None
        info = {
            'x':self.X,
            'y':self.Y,
            'z':self.Z,
            'heading':self.HEADING,
        }
        return(info)

if __name__ == '__main__':
    p = TankPosition()
    while True:
        i = p.info()
        if i:
            print(json.dumps(i))
        time.sleep(1)
