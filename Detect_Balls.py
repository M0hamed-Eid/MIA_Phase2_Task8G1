import cv2 as cv
import numpy as np

# Reading the image
image = cv.imread("/home/micro/Downloads/drive-download-20230914T045833Z-001/rb_000.jpg")
img = cv.medianBlur(image,17)
# Converting the image to HSV color space
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Defining the range of red and blue colors in HSV
lower_red  = np.array([170, 100, 170])
upper_red  = np.array([180, 255, 255])
lower_blue = np.array([110,120,50])
upper_blue = np.array([150,255,255])

# Creating a mask for red and blue colors using inRange function
mask_red  = cv.inRange(hsv, lower_red, upper_red)
mask_blue = cv.inRange(hsv, lower_blue, upper_blue)

# Applying morphological transformations (dilation and erosion) to remove noise from the mask
kernel   = np.ones((5,5),np.uint8)
mask_red = cv.dilate(mask_red,kernel,iterations = 3)
mask_red = cv.erode(mask_red,kernel,iterations = 2)

mask_blue = cv.dilate(mask_blue,kernel,iterations = 3)
mask_blue = cv.erode(mask_blue,kernel,iterations = 2)

# Detecting contours on the mask
contours_red, hierarchy = cv.findContours(mask_red, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
contours_blue, hierarchy = cv.findContours(mask_blue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Looping through the contours and drawing a bounding box around the red and blue balls
if contours_red:
    for contour in contours_red:
        (x,y,w,h) = cv.boundingRect(contour)
        cv.rectangle(image, (x,y), (x+w,y+h), (0,0,0), 2)
    cv.putText(image,"RED",(x,y),cv.FONT_HERSHEY_DUPLEX,1,100,2)
if contours_blue:    
    for contour in contours_blue:
        (X,Y,w,h) = cv.boundingRect(contour)
        cv.rectangle(image, (X,Y), (X+w,Y+h), (0,0,0), 2)
    cv.putText(image,"BLUE",(X,Y),cv.FONT_HERSHEY_DUPLEX,1,100,2)



cv.imshow('result', image)
cv.waitKey(0)
cv.destroyAllWindows()
