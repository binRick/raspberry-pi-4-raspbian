#!/usr/bin/env python3
import os, sys, time, logging, spidev as SPI, cv2
sys.path.append('../lcd')
from lib import LCD_2inch
from PIL import Image,ImageDraw
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
disp = LCD_2inch.LCD_2inch()
disp.Init()
disp.clear()

print(f'{disp.width}x{disp.height}')

image1 = Image.new("RGB", (disp.height, disp.width ), "WHITE")
draw = ImageDraw.Draw(image1)

vid = cv2.VideoCapture(0)

#vid.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
#vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

qty = 0
while True:
    ret, frame = vid.read()
    resized = cv2.resize(frame, (320,240))
    img_color = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(img_color)
    image = image.rotate(180)
    disp.ShowImage(image)
    print(f'processed frame #{qty}')
    qty = qty + 1



vid.release()
disp.module_exit()
sys.exit(0)


  
