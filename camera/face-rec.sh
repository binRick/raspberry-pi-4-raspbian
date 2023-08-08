#!/usr/bin/env bash
source .v/bin/activate
exec ./face-rec.py ${@:-}
