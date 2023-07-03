#!/usr/bin/env python3
import os, sys, time, logging, spidev as SPI, cv2, threading, queue
sys.path.append('../lcd')
from lib import LCD_2inch
from PIL import Image,ImageDraw

RST = 27
DC = 25
BL = 18
bus = 0 
device = 0
DEBUG_MODE = False

disp = LCD_2inch.LCD_2inch()
disp.Init()
disp.clear()

raw_frames = queue.Queue()
processed_frames = queue.Queue()

image1 = Image.new("RGB", (disp.height, disp.width ), "WHITE")
draw = ImageDraw.Draw(image1)

'''
while True:



vid.release()
disp.module_exit()
sys.exit(0)
'''

def display_frames():
    qty = 0
    while True:
        frame = processed_frames.get()
        if DEBUG_MODE:
            print(f'Showing Frame #{qty}')
        disp.ShowImage(frame)
        print(f'Showed Frame #{qty}')
        qty = qty + 1

def process_frames():
    qty = 0
    while True:
        frame = raw_frames.get()
        if DEBUG_MODE:
            print(f'Processing Frame #{qty}')
        resized = cv2.resize(frame, (disp.height,disp.width))
        img_color = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(img_color)
        image = image.rotate(180)
        if DEBUG_MODE:
            print(f'Processed Frame #{qty}')
        while processed_frames.qsize() > 0:
            processed_frames.get()
        processed_frames.put(image)
        qty = qty + 1

def collect_frames():
    qty = 0
    print('Starting Capture')
    vid = cv2.VideoCapture(0)
    #vid.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
    #vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
    print('Started Capture')
    while True:
        ret, frame = vid.read()
        if DEBUG_MODE:
            print(f'Read frame #{qty}')
        while raw_frames.qsize() > 0:
            raw_frames.get()
        raw_frames.put(frame)
        qty = qty + 1


def main():
    collect_thread = threading.Thread(target=collect_frames, daemon=False)
    process_thread = threading.Thread(target=process_frames, daemon=False)
    display_thread = threading.Thread(target=display_frames, daemon=False)

    display_thread.start()
    process_thread.start()
    collect_thread.start()

    collect_thread.join()
    process_thread.join()
    display_thread.join()

if __name__ == '__main__':
    main()
    

  
