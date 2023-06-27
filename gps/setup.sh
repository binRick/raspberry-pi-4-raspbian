#!/usr/bin/env bash
set -eou pipefail
if ! command -v gpsd >/dev/null 2>&1; then
	sudo apt install gpsd
fi

sudo systemctl enable --now gpsd
sudo systemctl status gpsd

gpscsv -n 2
