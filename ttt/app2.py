import cv2, sys
import numpy as np

def find_tic_tac_toe_board(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest rectangle (the Tic Tac Toe board)
    largest_area = 0
    tic_tac_toe_board = None

    for contour in contours:
        if cv2.contourArea(contour) > largest_area:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4:
                largest_area = cv2.contourArea(contour)
                tic_tac_toe_board = approx

    if tic_tac_toe_board is None:
        print("Tic Tac Toe board not found.")
        return None

    return tic_tac_toe_board

def extract_and_print_lines_coordinates(approx):
    # Sort the points in counter-clockwise order
    approx = np.array(sorted(approx, key=lambda x: x[0][0]))

    top_left, top_right, bottom_right, bottom_left = approx

    # Calculate the center points of each side
    top_center = (top_left + top_right) // 2
    bottom_center = (bottom_left + bottom_right) // 2
    left_center = (top_left + bottom_left) // 2
    right_center = (top_right + bottom_right) // 2

    # Print the coordinates of each line
    print("Top Line:    ", top_center[0])
    print("Bottom Line: ", bottom_center[0])
    print("Left Line:   ", left_center[0])
    print("Right Line:  ", right_center[0])

if __name__ == "__main__":
    image_path = sys.argv[1]
    
    tic_tac_toe_board = find_tic_tac_toe_board(image_path)
    
    if tic_tac_toe_board is not None:
        extract_and_print_lines_coordinates(tic_tac_toe_board)
    else:
        print("Tic Tac Toe board not found.")

