#!/usr/bin/env bash
if [[ ! -d .v ]]; then
	python3 -m venv .v
	source .v/bin/activate
	pip install numpy Pillow numpy
	python3 -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
	#python3 -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
fi
source .v/bin/activate
pip install opencv-python numpy
cmd="time python3 ./Banana.py \
	--model models/mobilenet_v1_0.75_192_quant_edgetpu.tflite \
	--labels labels/mobilenet_v1_0.75_192_quant_edgetpu.txt \
	--input $BANANAS"
	echo -e "$cmd" >&2
	eval "$cmd"
