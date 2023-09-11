H=192.168.1.225
ffmpeg -i /dev/video0 -f rtsp -rtsp_transport tcp "rtsp://$H:8888/live.sdp"
