#!/usr/bin/env python3
import cv2, sys
if len(sys.argv) > 1:
    out = sys.argv[1]
else:
    out = 'capture.png'

if len(sys.argv) > 2:
    qty = int(sys.argv[2])
else:
    qty = 1
  

vid = cv2.VideoCapture(0)
ret, frame = vid.read()
vid.release()


IMG_COL = 320
IMG_ROW = 240
border_v = 0
border_h = 0
if (IMG_COL/IMG_ROW) >= (frame.shape[0]/frame.shape[1]):
    border_v = int((((IMG_COL/IMG_ROW)*frame.shape[1])-frame.shape[0])/2)
else:
    border_h = int((((IMG_ROW/IMG_COL)*frame.shape[0])-frame.shape[1])/2)
print(f'h:{border_h} v:{border_h}')

#img = cv2.copyMakeBorder(img, border_v, border_v, border_h, border_h, cv2.BORDER_CONSTANT, 0)
#img = cv2.resize(img, (IMG_ROW, IMG_COL))

width = 320
height = frame.shape[0]
dim = (width, 240)

# resize image
resized = cv2.resize(frame, dim)
#, interpolation = cv2.INTER_AREA)

print('Resized Dimensions : ',resized.shape)

cv2.imwrite(out,resized)
print(out)
  
