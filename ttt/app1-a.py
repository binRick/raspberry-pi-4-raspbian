#!/usr/bin/env python3
import cv2, sys, os, numpy as np, pyautogui, json
''''''''''''
font = cv2.FONT_HERSHEY_COMPLEX
canny_min = 25
canny_max = 275
LINES_MIN_LENGTH = 25
LINES_MAX_GAP = 30
''''''''''''

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
edges = cv2.Canny(blurred, canny_min, canny_max)


lines = cv2.HoughLinesP(edges,1,np.pi/180,40,minLineLength=LINES_MIN_LENGTH,maxLineGap=LINES_MAX_GAP)
#print(f'# Lines:{len(lines)}')
#for line in lines:
#  for x1,y1,x2,y2 in line:
#    cv2.line(blanks[1],(x1,y1),(x2,y2),(255,0,0),5)

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

def find_contour_index_closest_to_border(contours,left,right,top_bottom):
  return None

def find_left_of_contours(contours):
  x = None
  for i, c in enumerate(contours):
    c_x,c_y,c_w,c_h = cv2.boundingRect(c)
    if x is None or (c_x) < x:
      x = c_x
  return x

def find_right_of_contours(contours):
  x = 0
  for i, c in enumerate(contours):
    c_x,c_y,c_w,c_h = cv2.boundingRect(c)
    if (c_x + c_w) > x:
      x = c_x + c_w
  return x

def find_top_of_contours(contours):
  y = None
  for i, c in enumerate(contours):
    c_x,c_y,c_w,c_h = cv2.boundingRect(c)
    if y is None or (c_y ) < y:
      y = c_y 
  return y

def find_bottom_of_contours(contours):
  y = 0
  for i, c in enumerate(contours):
    c_x,c_y,c_w,c_h = cv2.boundingRect(c)
    if (c_y + c_h) > y:
      y = c_y + c_h
  return y
      

def find_board_contour_index(contours):
  id = None
  board_area = 0
  for i, c in enumerate(contours):
    area = cv2.contourArea(c)
    perim = cv2.arcLength(c, True)
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    approx = cv2.approxPolyDP(c, 0.009 * cv2.arcLength(c, True), True)
    is_circle = cv2.isContourConvex(approx)
    c_x,c_y,c_w,c_h = cv2.boundingRect(c)
    if area > board_area:
      id = i
      board_area = area

  if id is None:
    raise Exception('Unable to find board contour!')
  return id

board_index = find_board_contour_index(contours)
bottom_y = find_bottom_of_contours(contours)
top_y = find_top_of_contours(contours)
right_x = find_right_of_contours(contours)
left_x = find_left_of_contours(contours)
cv2.drawContours(blanks[1], [contours[board_index]], -1, (0, 255, 0), 3)
print(f'[Board] #{board_index}|Bottom:{bottom_y}|Right:{right_x}|Left:{left_x}|Top:{top_y}|')
#sys.exit(0)

cs = []
titles = []
#cv2.namedWindow("Video", cv2.WINDOW_AUTOSIZE)
#(x,y,w,h) = cv2.getWindowImageRect('Video')
board_contour = None
board = {
  'contour':None,
  'properties': {
    'area':0,
    'permiter':0,
    'center':{'x':0,'y':0}, 
    'position':{'x':0,'y':0},
    'size':{'w':0,'h':0},
    'index':None
  }
}
for i, c in enumerate(contours):
  titles.append(f'#{i}')
  text_size = .8
  text_color = (0,255,255)
  area = cv2.contourArea(c)
  perim = int(cv2.arcLength(c, True))
  M = cv2.moments(c)
  cX = int(M["m10"] / M["m00"])
  cY = int(M["m01"] / M["m00"])
  approx = cv2.approxPolyDP(c, 0.009 * cv2.arcLength(c, True), True)
  is_circle = cv2.isContourConvex(approx)
  c_x,c_y,c_w,c_h = cv2.boundingRect(c)
  if i == board_index:
    board['properties']['index'] = i
    board['contour'] = c
    board['properties']['permiter'] = int(perim)
    board['properties']['area'] = int(area)
    board['properties']['center']['x'] = cX
    board['properties']['center']['y'] = cY
    board['properties']['position']['x'] = c_x
    board['properties']['position']['y'] = c_y
    board['properties']['size']['w'] = c_w
    board['properties']['size']['h'] = c_h
    titles[i] = f'#{i}'
    text_size = .7
    text_color = (255,0,0)
  elif is_circle:
    text_color = (0,0,255)

  cv2.circle(blanks[0], (cX, cY), 7, (255, 255, 255), -1)
  cv2.putText(blanks[0], titles[i], (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, text_size, text_color, 2)

  print(f'\t{titles[i]}|area:{area}|permiter:{perim}|cX:{cX}|cY:{cY}|circle? {is_circle}|')
  print(f'\t\tc_x:{c_x}|c_y:{c_y}|c_w:{c_w}|c_h:{c_h}')


if board['properties']['area'] > 0:
  board['properties']['left_line'] = {
    'position': {
      'x': board['properties']['position']['x'] + (board['properties']['size']['w']/3)
    }
  }
  blanks[0] = cv2.rectangle(blanks[0], 
	(left_x,top_y),
	(right_x,bottom_y),
	(255,0,0),
	2
  )

#  '''
  cv2.line(blanks[0],
	(int(board['properties']['left_line']['position']['x']),top_y),
	(int(board['properties']['left_line']['position']['x']),bottom_y),
	(255,0,0),
	5
  )
#  '''
  print(f'Found board!')
  print(json.dumps(board['properties'], indent=1))
#  print(f'\t|area={board["area"]}|permiter:{board["permiter"]}|')
#  print(f'\t|center:{board["center"]["x"]}x{board["center"]["y"]}|index:{board["index"]}|')
#  print(f'\t|position:{board["position"]["x"]}x{board["position"]["y"]}|')
#  print(f'\t|size:{board["size"]["w"]}x{board["size"]["h"]}|')

#process_image_contours(blanks[0], contours)
cv2.namedWindow('Contours', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('Board', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Contours', blanks[0])
cv2.imshow('Board', blanks[1])
#cv2.imshow('Lines', blanks[1])
#cv2.imshow('Lines 2', blanks[2])
cv2.moveWindow('Contours', o_w, 0)
cv2.moveWindow('Board', 0, o_h)
(c_x,c_y,c_w,c_h) = cv2.getWindowImageRect('Contours')
cv2.moveWindow('Original', 0, 0)
print(f'Contours: {c_x}x{c_y}@{c_w}x{c_h}')
#cv2.moveWindow('Lines', c_x, 0)
#(l_x,l_y,l_w,l_h) = cv2.getWindowImageRect('Lines')
#cv2.moveWindow('Lines 2', l_x, 0)


cv2.waitKey(0)
cv2.destroyAllWindows()
