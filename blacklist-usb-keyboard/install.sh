#!/usr/bin/env bash
set -eoxu pipefail
sudo cp \
		100-blacklist-usb-keyboard.rules \
		101-blacklist-usb-knob-controller.rules \
			/etc/udev/rules.d/.
