#!/usr/bin/env bash
set -eou pipefail
set -x
sudo apt -y install espeak vim cmake  libturbojpeg0-dev libexif-dev libavutil-dev libswscale-dev libgraphicsmagick++1-dev \
	libavcodec-dev libavformat-dev libavdevice-dev \
	zsh kitty python3-opencv \
	imagemagick  libortp-dev libortp15      libatlas-base-dev lynx sysstat npm nodejs \
	libncurses-dev ninja-build gfortran docker.io libgif-dev libgif7 raspberrypi-kernel-headers \
	v4l-utils python3-usb libgtk-3-dev libwebkit2gtk-4.0-dev

sudo apt -y autoremove
