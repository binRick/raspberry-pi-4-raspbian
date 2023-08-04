#!/usr/bin/env python3
import numpy as np
import cv2
import ffmpeg
import queue

q = queue.Queue()

in_file='rtsp://127.0.0.1:11795/live.sdp?tcp'#?overrun_nonfatal=1?buffer_size=10000000?fifo_size=100000'

width = 320
height = 240
cv2.namedWindow("Realtime Video")

process1 = (
    ffmpeg
    .input(in_file,rtsp_flags= 'listen')
    .output('pipe:', format='rawvideo', pix_fmt='bgr24')
    .run_async(pipe_stdout=True)
)
while True:
    in_bytes = process1.stdout.read(width * height * 3)
    if not in_bytes:
        break
    in_frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height, width, 3])
    )
    cv2.imshow("test", in_frame)
    cv2.waitKey(10)

process1.wait()
