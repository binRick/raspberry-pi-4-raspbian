#!/usr/bin/env python3
import numpy as np
import cv2
import ffmpeg, threading
import queue

q = queue.Queue()

in_file='rtsp://127.0.0.1:11795/live.sdp?tcp'#?overrun_nonfatal=1?buffer_size=10000000?fifo_size=100000'

width = 320
height = 240
cv2.namedWindow("Realtime Video")



def receive():
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
        while not q.empty():
            q.get()
        q.put(in_frame)
        #cv2.imshow("test", in_frame)
        #cv2.waitKey(10)

    process1.wait()
    '''
    cap = cv2.VideoCapture('udp://@127.0.0.1:11795?buffer_size=65535&pkt_size=65535&fifo_size=65535')
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        q.put(frame)
    '''

def display():
    while True:
        if q.empty() != True:
            frame = q.get()
            cv2.imshow('Video', frame)

        k = cv2.waitKey(1) & 0xff
        if k == 27:  # press 'ESC' to quit
            break


tr = threading.Thread(target=receive, daemon=True)
td = threading.Thread(target=display)

tr.start()
td.start()

td.join()
