ffmpeg -f video4linux2 -s 640x480 -r 15 -vcodec h264 -i /dev/video0 -an http://localhost:8099/feed1.ffm
