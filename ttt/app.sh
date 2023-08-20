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
timg -g30x -pk "$img"
#clear
#for x in $(seq 1 25); do echo; done
exec python3 $script $img
