ffmpeg -i /dev/video0 \
	-filter:v fps=30 \
	-c:v rawvideo -pix_fmt yuv420p -f sdl "Realtime Video Stream"
