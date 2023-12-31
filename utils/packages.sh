#!/usr/bin/env bash
set -eou pipefail
set -x
sudo apt -y install espeak vim cmake  libturbojpeg0-dev  \
	zsh kitty python3-opencv python3-venv \
	imagemagick  libortp-dev libortp15      libatlas-base-dev lynx sysstat npm nodejs \
	libsixel-dev graphicsmagick libdeflate-dev \
	libgraphicsmagick1-dev \
	python3-usb python3-tk python3-dev \
	bazel-bootstrap graphicsmagick++    \
	portaudio19-dev python3-pyaudio



sudo apt -y autoremove
