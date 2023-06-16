#!/usr/bin/env python3
import cv2, sys
out = 'camera.png'
if len(sys.argv) > 1:
    out = sys.argv[1]

  
vid = cv2.VideoCapture(0)
ret, frame = vid.read()
vid.release()
cv2.imwrite('i.png',frame)
print(out)
  
