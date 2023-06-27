#!/usr/bin/env python3
import gpsd, os, sys, json, time
from datetime import datetime


gpsd.connect()

retries = 3

def valid_packet(packet):
    return(packet != None and packet.mode == 3)

def get_gps_info():
    p = None
    attempt = 0
    while attempt < retries and not valid_packet(p):
        if attempt > 1:
            print(f'Attempt #{attempt+1}/{retries}')
        p = gpsd.get_current()
        if not valid_packet(p):
            time.sleep(1)
        attempt = attempt + 1


    if not valid_packet(p):
        print('Failed to get gps info')
        sys.exit(1)

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

while True:
    print(json.dumps(get_gps_info()))
    time.sleep(1)
