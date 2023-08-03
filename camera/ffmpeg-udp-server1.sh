ffmpeg -re -i /dev/video0 -strict -2 -c:v copy -an -preset slower -tune stillimage -b 11200k -f rawvideo udp://127.0.0.1:11795
