#!/usr/bin/env bash
set -eou pipefail
IMG="capture-$(date +%s).png"

./image.py "$IMG" 1

timg -pk "$IMG"
