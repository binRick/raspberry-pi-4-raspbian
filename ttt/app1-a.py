#!/usr/bin/env python3                                                                                                                               [51/1824]
import cv2, sys, os, numpy as np
font = cv2.FONT_HERSHEY_COMPLEX

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

    for j in n :
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
# Load the image                                                                                                                                     [15/1824]
image_path = sys.argv[1]
image = cv2.imread(image_path)

print('Original Dimensions : ',image.shape)


scale_percent = 60 # percent of original size
scale_percent = 500 / image.shape[0] * 100
print(f'scale percent: {scale_percent}')

width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

blank = np.zeros(image.shape, dtype = np.uint8)

print('Resized Dimensions : ',image.shape)

#sys.exit(0)

#image = cv2.resize(image, (500, 500))

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection using Canny
canny_min = 25
canny_max = 275
edges = cv2.Canny(blurred, canny_min, canny_max)

# Find contours in the edged image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f'# Contours: {len(contours)}')

#area = cv2.contourArea(contours[0])
#print(area)

cv2.drawContours(blank, contours, -1, (0, 255, 0), 3)
process_image_contours(blank, contours)



cv2.imshow('Original', image)
cv2.imshow('Board', blank)
cv2.waitKey(0)
cv2.destroyAllWindows()
