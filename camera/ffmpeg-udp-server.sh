ffmpeg -f v4l2 -input_format mjpeg -i /dev/video0 -r 10 -b:v 2000k -s 256x144 -c:v libx264 -f mpegts -flush_packets 0 udp://localhost:11795?pkt_size=1024
