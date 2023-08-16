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

def normalize_image(image, corners):
    # Define the desired width and height of the normalized image
    width = 300
    height = 300

    # Define the coordinates of the corners of the normalized image
    normalized_corners = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    # Calculate the perspective transform matrix
    transform_matrix = cv2.getPerspectiveTransform(corners, normalized_corners)

    # Apply the perspective transform to the original image
    normalized_image = cv2.warpPerspective(image, transform_matrix, (width, height))

    return normalized_image

if __name__ == "__main__":
    image_path = sys.argv[1]
    
    tic_tac_toe_board = find_tic_tac_toe_board(image_path)
    
    if tic_tac_toe_board is not None:
        # Reshape the corners to be in the order: top-left, top-right, bottom-right, bottom-left
        corners = np.array([tic_tac_toe_board[0], tic_tac_toe_board[1], tic_tac_toe_board[3], tic_tac_toe_board[2]], dtype=np.float32)
        
        # Load the original image
        image = cv2.imread(image_path)
        
        # Normalize the image
        normalized_image = normalize_image(image, corners)
        
        # Display the original and normalized images
        cv2.imshow('Original Image', image)
        cv2.imshow('Normalized Image', normalized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Tic Tac Toe board not found.")
