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

def determine_board_size(corners):
    # Calculate the length of each side of the board
    side_lengths = []
    for i in range(3):
        side_lengths.append(np.linalg.norm(corners[i] - corners[i + 1]))
    side_lengths.append(np.linalg.norm(corners[3] - corners[0]))

    # Find the average side length
    average_side_length = np.mean(side_lengths)

    # Determine the size based on the average side length
    if 0.8 * average_side_length <= side_lengths[0] <= 1.2 * average_side_length:
        return 3  # 3x3 board
    elif 1.8 * average_side_length <= side_lengths[0] <= 2.2 * average_side_length:
        return 4  # 4x4 board
    else:
        return -1  # Unable to determine size

if __name__ == "__main__":
    image_path = sys.argv[1]
    
    tic_tac_toe_board = find_tic_tac_toe_board(image_path)
    
    if tic_tac_toe_board is not None:
        # Reshape the corners to be in the order: top-left, top-right, bottom-right, bottom-left
        corners = np.array([tic_tac_toe_board[0], tic_tac_toe_board[1], tic_tac_toe_board[3], tic_tac_toe_board[2]], dtype=np.float32)
        
        # Determine the board size
        board_size = determine_board_size(corners)
        
        if board_size > 0:
            print("Detected Board Size:", board_size, "x", board_size)
        else:
            print("Unable to determine board size.")
    else:
        print("Tic Tac Toe board not found.")

