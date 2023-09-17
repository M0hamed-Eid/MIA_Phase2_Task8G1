import cv2 as cv
import numpy as np
import os

# Full absolute path to the directory containing the images
image_dir = r"D:\My_GitHub\balls_dataset"

# Create a directory to save the images with detections
output_dir = r"D:\My_GitHub\output_images"
os.makedirs(output_dir, exist_ok=True)

# Function to detect balls in an image
def detect_balls(image_path):
    # Reading the image
    image = cv.imread(image_path)
    img = cv.medianBlur(image, 17)
    # Converting the image to HSV color space
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Defining the range of red and blue colors in HSV
    lower_red = np.array([170, 100, 170])
    upper_red = np.array([180, 255, 255])
    lower_blue = np.array([110, 120, 50])
    upper_blue = np.array([150, 255, 255])
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([250, 255, 30])

    # Creating a mask for red and blue colors using inRange function
    mask_red = cv.inRange(hsv, lower_red, upper_red)
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)

    # Applying morphological transformations (dilation and erosion) to remove noise from the mask
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv.dilate(mask_red, kernel, iterations=3)
    mask_red = cv.erode(mask_red, kernel, iterations=2)

    mask_blue = cv.dilate(mask_blue, kernel, iterations=3)
    mask_blue = cv.erode(mask_blue, kernel, iterations=2)

    # Detecting contours on the mask
    contours_red, hierarchy = cv.findContours(mask_red, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours_blue, hierarchy = cv.findContours(mask_blue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Looping through the contours and drawing circles around the red and blue balls
    if contours_red:
        for contour in contours_red:
            # Get the area of the contour
            area = cv.contourArea(contour)
            # Set a minimum threshold for the detected object's area
            if area > 400:
                (x, y), radius = cv.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv.circle(image, center, radius, (0, 0, 0), 2)
                cv.putText(image, "RED", (int(x) - 30, int(y)), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
    if contours_blue:
        for contour in contours_blue:
            # Get the area of the contour
            area = cv.contourArea(contour)
            # Set a minimum threshold for the detected object's area
            if area > 500:
                (x, y), radius = cv.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv.circle(image, center, radius, (0, 0, 0), 2)
                cv.putText(image, "BLUE", (int(x) - 30, int(y)), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)

    # Save the image with detections
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv.imwrite(output_path, image)

# Process all images in the directory
for image_file in os.listdir(image_dir):
    if image_file.endswith(".jpg"):
        image_path = os.path.join(image_dir, image_file)
        detect_balls(image_path)

cv.destroyAllWindows()
