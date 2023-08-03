ffmpeg -stream_loop 5 -re -i /dev/video0 -vf scale=320:240 -vcodec libx264 -f rtsp -rtsp_transport tcp rtsp://127.0.0.1:11795/live.sdp
