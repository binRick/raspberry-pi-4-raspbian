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

def get_center_square_state(image, corners):
    # Define the coordinates of the center square's corners
    center_square_corners = np.array([
        [corners[0][0] + (corners[1][0] - corners[0][0]) // 3, corners[0][1] + (corners[3][1] - corners[0][1]) // 3],
        [corners[0][0] + 2 * (corners[1][0] - corners[0][0]) // 3, corners[0][1] + (corners[3][1] - corners[0][1]) // 3],
        [corners[0][0] + (corners[1][0] - corners[0][0]) // 3, corners[0][1] + 2 * (corners[3][1] - corners[0][1]) // 3],
        [corners[0][0] + 2 * (corners[1][0] - corners[0][0]) // 3, corners[0][1] + 2 * (corners[3][1] - corners[0][1]) // 3]
    ], dtype=np.float32)

    # Warp the center square to a smaller image
    warped_center_square = cv2.getPerspectiveTransform(center_square_corners, np.array([[0, 0], [2, 0], [0, 2], [2, 2]], dtype=np.float32))
    warped_image = cv2.warpPerspective(image, warped_center_square, (3, 3))

    # Convert the center square to grayscale
    gray_center_square = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to separate X and O squares
    _, thresholded = cv2.threshold(gray_center_square, 128, 255, cv2.THRESH_BINARY)

    # Count the number of white pixels in the thresholded image
    white_pixel_count = np.sum(thresholded == 255)

    # Determine the state of the center square
    if white_pixel_count > 0.5 * thresholded.size:
        return 'O'
    elif white_pixel_count > 0:
        return 'X'
    else:
        return 'Empty'

if __name__ == "__main__":
    image_path = sys.argv[1]
    
    tic_tac_toe_board = find_tic_tac_toe_board(image_path)
    
    if tic_tac_toe_board is not None:
        # Reshape the corners to be in the order: top-left, top-right, bottom-right, bottom-left
        corners = np.array([tic_tac_toe_board[0], tic_tac_toe_board[1], tic_tac_toe_board[3], tic_tac_toe_board[2]], dtype=np.float32)
        
        # Load the original image
        image = cv2.imread(image_path)
        
        # Get the state of the center square
        center_square_state = get_center_square_state(image, corners)
        
        print("Center Square State:", center_square_state)
    else:
        print("Tic Tac Toe board not found.")

