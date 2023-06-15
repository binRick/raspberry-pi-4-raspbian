#!/usr/bin/env bash
set -eoxu pipefail
sudo apt install libhidapi-hidraw0 python3-dev libusb-1.0-0-dev libudev-dev

[[ -d .v ]] || python3 -m venv .v
source .v/bin/activate
pip install hidapi

[[ -d cython-hidapi ]] || git clone https://github.com/trezor/cython-hidapi.git
cd cython-hidapi
git submodule update --init
python setup.py build
python setup.py install
