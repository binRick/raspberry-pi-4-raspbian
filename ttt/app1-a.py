#!/usr/bin/env python3
import cv2, sys, os, numpy as np, pyautogui, json, pygetwindow as gw, subprocess
''''''''''''
font = cv2.FONT_HERSHEY_COMPLEX
canny_min = 25
canny_max = 200
LINES_MIN_LENGTH = 25
LINES_MAX_GAP = 30
''''''''''''

image_path = sys.argv[1]
image = cv2.imread(image_path)
win_w, win_h = pyautogui.size()

active_window = gw.getActiveWindow().strip()
activate_cmd = f'osascript -e \'tell application "{active_window}" to activate\''

print(f'Monitor Size: {win_w}x{win_h}px')

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


print(f'Original Image Dimensions : {image.shape[0]}x{image.shape[1]}px')


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

def get_contour_center(c):
  M = cv2.moments(c)
  cX = int(M["m10"] / M["m00"])
  cY = int(M["m01"] / M["m00"])
  return cX, cY

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
chars_x = []
chars_o = []
for i, c in enumerate(contours):
  titles.append(f'#{i}')
  text_size = .8
  text_color = (0,255,255)
  area = cv2.contourArea(c)
  perim = int(cv2.arcLength(c, True))
  M = cv2.moments(c)
  cX = int(M["m10"] / M["m00"])
  cY = int(M["m01"] / M["m00"])
  poly_dp_val = 0.009
  poly_dp_val = 0.059
  approx = cv2.approxPolyDP(c, poly_dp_val * cv2.arcLength(c, True), True)
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

  if i != board_index:
   if is_circle:
    chars_o.append(i)
   else:
    chars_x.append(i)

  if i != board_index:
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
  board['properties']['right_line'] = {
    'position': {
      'x': board['properties']['position']['x'] + (board['properties']['size']['w']/3*2)
    }
  }
  board['properties']['top_line'] = {
    'position': {
      'y': board['properties']['position']['y'] + (board['properties']['size']['h']/3)
    }
  }
  board['properties']['bottom_line'] = {
    'position': {
      'y': board['properties']['position']['y'] + (board['properties']['size']['h']/3*2)
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
	(left_x,int(board['properties']['top_line']['position']['y'])),
	(right_x,int(board['properties']['top_line']['position']['y'])),
	(255,0,0),
	5
  )
  cv2.line(blanks[0],
	(left_x,int(board['properties']['bottom_line']['position']['y'])),
	(right_x,int(board['properties']['bottom_line']['position']['y'])),
	(255,0,0),
	5
  )
  cv2.line(blanks[0],
	(int(board['properties']['left_line']['position']['x']),top_y),
	(int(board['properties']['left_line']['position']['x']),bottom_y),
	(255,0,0),
	5
  )
  cv2.line(blanks[0],
	(int(board['properties']['right_line']['position']['x']),top_y),
	(int(board['properties']['right_line']['position']['x']),bottom_y),
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

def get_position(x, y):
  top_line_y = int(board['properties']['top_line']['position']['y'])
  bottom_line_y = int(board['properties']['bottom_line']['position']['y'])
  left_line_x = int(board['properties']['left_line']['position']['x'])
  right_line_x = int(board['properties']['right_line']['position']['x'])
  print(f'\tComparing {x}x{y} to {left_line_x}/{right_line_x}@{top_line_y}/{bottom_line_y}')
  if x < left_line_x and y < top_line_y:
    return 0
  if x > left_line_x and y < top_line_y and x < right_line_x:
    return 1
  if x > right_line_x and y < top_line_y:
    return 2
  if x < left_line_x and y > top_line_y and y < bottom_line_y:
    return 3
  if x > left_line_x and y > top_line_y and y < bottom_line_y and x < right_line_x:
    return 4
  if x > right_line_x and y > top_line_y and y < bottom_line_y:
    return 5
  if x < left_line_x and y > bottom_line_y:
    return 6
  if x > left_line_x and x < right_line_x and y > bottom_line_y:
    return 7
  if x > right_line_x and y > bottom_line_y:
    return 8

#  raise Exception(f'Unable to find {x}x{y}!')
  return -1

positions = [
  [' ',' ',' '],
  [' ',' ',' '],
  [' ',' ',' '],
]

for i in chars_x:
  x, y = get_contour_center(contours[i])
  p = get_position(x,y)
  print(f'X: #{i} @ {x}x{y}|p={p}')

for i in chars_o:
  x, y = get_contour_center(contours[i])
  p = get_position(x,y)
  print(f'O: #{i} @ {x}x{y}|p={p}')

print(positions)


#process_image_contours(blanks[0], contours)
cv2.namedWindow('Contours', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('Board', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Contours', blanks[0])
cv2.imshow('Board', blanks[1])
cv2.imshow('Cells', blanks[2])
cv2.moveWindow('Contours', o_w, 0)
cv2.moveWindow('Board', 0, o_h)
(c_x,c_y,c_w,c_h) = cv2.getWindowImageRect('Contours')
print(f'Contours: {c_x}x{c_y}@{c_w}x{c_h}')
(b_x,b_y,b_w,b_h) = cv2.getWindowImageRect('Board')
cv2.moveWindow('Cells', b_w, o_h)
cv2.moveWindow('Original', 0, 0)
subprocess.call(activate_cmd, shell=True)

print("___|_X_|___", "___|___|___", "   |   |   ", sep='\n')


cv2.waitKey(0)
cv2.destroyAllWindows()


