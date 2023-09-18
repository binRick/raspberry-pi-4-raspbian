#!/usr/bin/env python3
import gpsd, os, sys, json, time
from datetime import datetime

class TankGPS():
    RETRIES = 3
    def __init__(self):
        gpsd.connect()

    def valid_packet(self, packet):
        return(packet != None and packet.mode == 3)

    def info(self):
        p = None
        attempt = 0
        while attempt < self.RETRIES and not self.valid_packet(p):
            if attempt > 1:
                print(f'Attempt #{attempt+1}/{retries}')
            p = gpsd.get_current()
            if not self.valid_packet(p):
                time.sleep(1)
            attempt = attempt + 1


        if not self.valid_packet(p):
            print('Failed to get gps info')
            return None

        info = {
                'attempt': attempt,
                'mode': p.mode,
                'satellites': p.sats,
                'valid_satellites': p.sats_valid,
                'lattitude': p.lat,
                'longitude': p.lon,
                'altitude': p.altitude(),
                'url': p.map_url(),
                'movement': p.movement(),
                'localtime': datetime.timestamp(p.get_time(local_time=True)),
                'time': datetime.timestamp(p.get_time(local_time=False)),
        }
        return(info)

if __name__ == '__main__':
    g = TankGPS()
    while True:
        print(json.dumps(g.info()))
        time.sleep(1)
