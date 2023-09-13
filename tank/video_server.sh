#!/usr/bin/env bash
set -eou pipefail
set -x
H="192.168.1.225"
cmd="ffmpeg -i /dev/video0 -f rtsp -rtsp_transport tcp \"rtsp://$H:8888/live.sdp\""
while :; do 
	eval "$cmd" || sleep 1
done
