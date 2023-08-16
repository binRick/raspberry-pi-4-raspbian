#!/usr/bin/env bash
set -eou pipefail
if [[ ! -e ".v/bin/activate" ]]; then
	python3 -m venv .v
	source .v/bin/activate
	pip install opencv-python numpy
else
	source .v/bin/activate
fi
script="$1"
img="$2"
timg -pk "$img"
exec python3 $script $img
