#!/usr/bin/env bash
[[ -d .d ]] || python3 -m venv .v
source .v/bin/activate
source get-device.sh
ARDUINO_DEVICE="/dev/$(getdevice "$(./get-arduino-device-id.sh)")"
GPS_DEVICE="/dev/$(getdevice "$(./get-gps-device-id.sh)")"

echo -e "GPS:$GPS_DEVICE\nARDUINO:$ARDUINO_DEVICE"
export GPS_DEVICE ARDUINO_DEVICE

python tank.py
#reset
