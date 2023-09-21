#!/usr/bin/env bash
set -eou pipefail
BANANAS="$(find images/bananas/ -type f|tr '\n' ',')"
if [[ ! -d .v ]]; then
	python3 -m venv .v
	source .v/bin/activate
	pip -q install numpy Pillow numpy opencv-python
	python3 -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
	#python3 -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
fi
source .v/bin/activate
cmd="time python3 ./Banana.py \
	--model models/mobilenet_v1_0.75_192_quant_edgetpu.tflite \
	--labels labels/mobilenet_v1_0.75_192_quant_edgetpu.txt \
	--input $BANANAS"
	echo -e "$cmd" >&2
	eval "$cmd"
