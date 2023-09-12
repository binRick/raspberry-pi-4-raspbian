#!/usr/bin/env bash
[[ -d .d ]] || python3 -m venv .v
source .v/bin/activate
python tank.py
#reset
