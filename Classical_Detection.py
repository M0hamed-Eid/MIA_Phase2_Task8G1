import cv2 as cv
import numpy as np
import os

# Full absolute path to the directory containing the images
image_dir = r"/home/micro/Downloads/drive-download-20230914T045833Z-001"

# Create a directory to save the images with detections
output_dir = r"/home/micro/Downloads/out"
os.makedirs(output_dir, exist_ok=True)

# Function to detect balls in an image
def detect_balls(image_path):
    # Reading The Image
    img = cv.imread(image_path)
    
    
    # Resize The Image If Neede
    if ((img.shape[1]>1000 and img.shape[1]<1500) or (img.shape[0]>1000 and img.shape[0]<1500)):
        new_image = cv.resize(img,None,fx=0.75, fy=0.75, interpolation = cv.INTER_AREA)
    elif((img.shape[1]>1500) or (img.shape[0]>1500 )):
        new_image = cv.resize(img,None,fx=0.25, fy=0.25, interpolation = cv.INTER_AREA)
    else:
        new_image = img 
    # Convert Image into HSV And Set Lower_Upper values for H-S-V
    image      = cv.medianBlur(new_image,17)      
    hsv        = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    lower_red  = np.array([0, 160, 150])
    upper_red  = np.array([10, 255, 255])
    lower_blue = np.array([110,120,50])
    upper_blue = np.array([150,255,255])
    
    # Creating a mask for red and blue colors using inRange function
    mask_red  = cv.inRange(hsv, lower_red, upper_red)
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    
    # Applying morphological transformations (dilation and erosion) to remove noise from the mask
    kernel    = np.ones((5,5),np.uint8)
    
    mask_red  = cv.dilate(mask_red,kernel,iterations =2)
    mask_red  = cv.erode(mask_red,kernel,iterations = 1)
    
    mask_blue = cv.dilate(mask_blue,kernel,iterations = 4)
    mask_blue = cv.erode(mask_blue,kernel,iterations = 3)
    
    # Apply Contour Detection
    red_contours  = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    blue_contours = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    # Trying to Delete Noise 
    red_contours  = [contour for contour in red_contours if cv.contourArea(contour) > 600]
    blue_contours = [contour for contour in blue_contours if cv.contourArea(contour) > 600]
    
    red_bboxes = []
    for contour in red_contours:
        (x, y, w, h) = cv.boundingRect(contour)
        red_bboxes.append((x, y, w, h))
    
    # Draw the bounding boxes around the red balls
    for bbox in red_bboxes:
        (x, y, w, h) = bbox
        cv.rectangle(new_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.putText(new_image,"RED",(x,y),cv.FONT_HERSHEY_DUPLEX,1,100,2)
    blue_bboxes = []
    for contour in blue_contours:
        (x, y, w, h) = cv.boundingRect(contour)
        blue_bboxes.append((x, y, w, h))
    
    # Draw the bounding boxes around the red balls
    for bbox in blue_bboxes:
        (x, y, w, h) = bbox
        cv.rectangle(new_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv.putText(new_image,"BLUE",(x,y),cv.FONT_HERSHEY_DUPLEX,1,100,2)
    

    # Save the image with detections
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv.imwrite(output_path, new_image)

# Process all images in the directory
for image_file in os.listdir(image_dir):
    if image_file.endswith(".jpg"):
        image_path = os.path.join(image_dir, image_file)
        detect_balls(image_path)

cv.destroyAllWindows()