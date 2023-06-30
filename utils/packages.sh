#!/usr/bin/env bash
set -eou pipefail
set -x
sudo apt -y install  vim cmake  libturbojpeg0-dev libexif-dev libavutil-dev libswscale-dev libgraphicsmagick++1-dev \
	libavcodec-dev libavformat-dev libavdevice-dev
