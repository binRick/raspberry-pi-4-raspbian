#!/usr/bin/env python3
import cv2, sys, os, numpy as np, pyautogui
font = cv2.FONT_HERSHEY_COMPLEX
image_path = sys.argv[1]
image = cv2.imread(image_path)
win_w, win_h = pyautogui.size()

print(f'Monitor Size: {win_w}x{win_h}')

def process_image_contours(image, c):
  for index, cnt in enumerate(c):
    print(f'\tContour #{index}')
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

    # draws boundary of contours.
    #cv2.drawContours(image, [approx], 0, (0, 0, 255), 5)

    # Used to flatted the array containing
    # the co-ordinates of the vertices.
    n = approx.ravel()
    i = 0

    for j in n:
        if(i % 2 == 0):
            x = n[i]
            y = n[i + 1]
            #print(f'\t\tx:{x}|y:{y}')

            # String containing the co-ordinates.
            string = str(x) + " " + str(y)

            if(i == 0):
                # text on topmost co-ordinate.
                cv2.putText(i, "Arrow tip", (x, y),
                                font, 0.5, (255, 0, 0))
            else:
                # text on remaining co-ordinates.
                cv2.putText(i, string, (x, y),
                        font, 0.5, (0, 255, 0))
        i = i + 1


print('Original Dimensions : ',image.shape)


scale_percent = 60 # percent of original size
scale_percent = int(500 / image.shape[0] * 100)
print(f'scale percent: {scale_percent}')

width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
print('Resized Dimensions : ',image.shape)

blanks = []
blanks.append(np.zeros(image.shape, dtype = np.uint8))
blanks.append(np.zeros(image.shape, dtype = np.uint8))
blanks.append(np.zeros(image.shape, dtype = np.uint8))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# Apply edge detection using Canny
canny_min = 25
canny_max = 275
edges = cv2.Canny(blurred, canny_min, canny_max)
lines = cv2.HoughLinesP(edges,1,np.pi/180,40,minLineLength=25,maxLineGap=30)
print(f'# Lines:{len(lines)}')
for line in lines:
  for x1,y1,x2,y2 in line:
    cv2.line(blanks[1],(x1,y1),(x2,y2),(255,0,0),5)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 50  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments


# Find contours in the edged image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f'# Contours: {len(contours)}')

#area = cv2.contourArea(contours[0])
#print(area)

cv2.imshow('Original', image)
(o_x,o_y,o_w,o_h) = cv2.getWindowImageRect('Original')
print(f'Original: {o_x}x{o_y}@{o_w}x{o_h}')
cv2.drawContours(blanks[0], contours, -1, (0, 255, 0), 3)
#cv2.drawContours(blanks[0], [contours[1]], -1, (0, 255, 0), 3)


cs = []
titles = []
#cv2.namedWindow("Video", cv2.WINDOW_AUTOSIZE)
#(x,y,w,h) = cv2.getWindowImageRect('Video')
draw_contours = False
board_contour = None
board = {
  'area':0,'contour':None,'permiter':0,
  'center':{'x':0,'y':0}, 
  'position':{'x':0,'y':0},
  'size':{'w':0,'h':0},
  'index':None
}
for i, c in enumerate(contours):
  titles.append(f'#{i}')
  area = cv2.contourArea(c)
  perim = cv2.arcLength(c, True)
  M = cv2.moments(c)
  cX = int(M["m10"] / M["m00"])
  cY = int(M["m01"] / M["m00"])
  approx = cv2.approxPolyDP(c, 0.009 * cv2.arcLength(c, True), True)
  is_circle = cv2.isContourConvex(approx)
  c_x,c_y,c_w,c_h = cv2.boundingRect(c)
  if not is_circle and area > board['area']:
    board['index'] = i
    board['contour'] = c
    board['permiter'] = perim
    board['area'] = area
    board['center']['x'] = cX
    board['center']['y'] = cY
    board['position']['x'] = c_x
    board['position']['y'] = c_y
    board['size']['w'] = c_w
    board['size']['h'] = c_h


  cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
  cv2.circle(blanks[0], (cX, cY), 7, (255, 255, 255), -1)
  cv2.putText(blanks[0], titles[i], (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)

  print(f'\t{titles[i]}|area:{area}|permiter:{perim}|cX:{cX}|cY:{cY}|circle? {is_circle}|')
  print(f'\t\tc_x:{c_x}|c_y:{c_y}|c_w:{c_w}|c_h:{c_h}')
  x = 0
  y = 0
  if draw_contours:
    cv2.namedWindow(titles[i], cv2.WINDOW_AUTOSIZE)
  if i > 0:
    if draw_contours:
      (prev_x,prev_y,prev_w,prev_h) = cv2.getWindowImageRect(titles[i-1])
      print(f'Previous: {prev_x}x{prev_y}@{prev_w}x{prev_h}')
      x = x + prev_w
      y = y + prev_h
      cv2.moveWindow(titles[i], x, y)
  if draw_contours:
    (x,y,w,h) = cv2.getWindowImageRect(titles[i])
    print(f'#{i}: {x}x{y}@{w}x{h}')

  if draw_contours:
    cs.append(np.zeros(image.shape, dtype = np.uint8))
    cv2.drawContours(cs[i], [c[i]], -1, (0, 255, 0), 3)
    cv2.imshow(titles[i], cs[i])


if board['area'] > 0:
  print(f'Found board!')
  print(f'\t|area={board["area"]}|permiter:{board["permiter"]}|')
  print(f'\t|center:{board["center"]["x"]}x{board["center"]["y"]}|index:{board["index"]}|')
  print(f'\t|position:{board["position"]["x"]}x{board["position"]["y"]}|')
  print(f'\t|size:{board["size"]["w"]}x{board["size"]["h"]}|')

#process_image_contours(blanks[0], contours)
cv2.namedWindow('Contours', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Contours', blanks[0])
cv2.imshow('Lines', blanks[1])
cv2.imshow('Lines 2', blanks[2])
cv2.moveWindow('Contours', o_w, 0)
(c_x,c_y,c_w,c_h) = cv2.getWindowImageRect('Contours')
print(f'Contours: {c_x}x{c_y}@{c_w}x{c_h}')
cv2.moveWindow('Lines', c_x, 0)
(l_x,l_y,l_w,l_h) = cv2.getWindowImageRect('Lines')
cv2.moveWindow('Lines 2', l_x, 0)


cv2.waitKey(0)
cv2.destroyAllWindows()
