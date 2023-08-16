#!/usr/bin/env python3
import cv2, sys, os, numpy as np

# Load the image
image_path = sys.argv[1]
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply edge detection using Canny
edges = cv2.Canny(blurred, 50, 150)

# Find contours in the edged image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize empty board
board = [[' ' for _ in range(3)] for _ in range(3)]

for contour in contours:
    if cv2.contourArea(contour) > 1000:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            cell = gray[y:y+h, x:x+w]
            
            # Threshold the cell to detect X or O
            _, cell_thresholded = cv2.threshold(cell, 128, 255, cv2.THRESH_BINARY)
            
            # Count the number of white pixels
            white_pixel_count = np.sum(cell_thresholded == 255)
            
            row = int(y / h)
            col = int(x / w)
            
            if white_pixel_count > 0.5 * cell.size:
                board[row][col] = 'O'
            else:
                board[row][col] = 'X'

# Print the board state
for row in board:
    print(' | '.join(row))
    print('-' * 9)

# Display the image with detected contours
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
cv2.imshow('Detected Board', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
