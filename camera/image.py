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
cv2.imwrite(out,frame)
print(out)
  
