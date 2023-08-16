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

    return tic_tac_toe_board

def calculate_board_size_in_pixels(corners):
    # Calculate the distance between two corners to estimate the size in pixels
    diagonal_length = np.linalg.norm(corners[0] - corners[2])
    
    return diagonal_length

if __name__ == "__main__":
    image_path = sys.argv[1]
    
    tic_tac_toe_board = find_tic_tac_toe_board(image_path)
    
    if tic_tac_toe_board is not None:
        # Reshape the corners to be in the order: top-left, top-right, bottom-right, bottom-left
        corners = np.array([tic_tac_toe_board[0], tic_tac_toe_board[1], tic_tac_toe_board[3], tic_tac_toe_board[2]], dtype=np.float32)
        
        # Calculate the board size in pixels
        board_size_pixels = calculate_board_size_in_pixels(corners)
        
        print("Detected Board Size (in pixels):", board_size_pixels)
    else:
        print("Tic Tac Toe board not found.")

