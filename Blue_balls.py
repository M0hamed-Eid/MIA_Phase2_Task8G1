import cv2 as cv
import numpy as np
  
# To read image
img = cv.imread("D:\\My_GitHub\\balls_dataset")
#cv.imshow("image",img)
if ((img.shape[1]>1000 and img.shape[1]<1500) or (img.shape[0]>1000 and img.shape[0]<1500)):
    new_image = cv.resize(img,None,fx=0.75, fy=0.75, interpolation = cv.INTER_AREA)
elif((img.shape[1]>1500) or (img.shape[0]>1500 )):
    new_image = cv.resize(img,None,fx=0.25, fy=0.25, interpolation = cv.INTER_AREA)
else:
    new_image = img 
hsv = cv.cvtColor(new_image,cv.COLOR_BGR2HSV)
lower = np.array ([110,120,50])
upper = np.array ([150,255,255])
mask_blue = cv.inRange(hsv,lower,upper)
cv.imshow("Maskbbbb",mask_blue)
#lower_red = np.array([100,20, 20])
#upper_red = np.array([200, 255, 255])  
#red_mask = cv.inRange(hsv, lower_red, upper_red)
#cv.imshow("Maskrrrr",red_mask)
res1 = cv.bitwise_and(hsv,hsv,mask=mask_blue)
#res2 = cv.bitwise_and(img,img,mask=red_mask)
#res = cv.bitwise_or(res1,res2)
#cv.imshow("Mask",res)
cont,_ = cv.findContours(mask_blue,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
cont_img = cv.drawContours(new_image,cont,1, 255,3)
c= max(cont,key=cv.contourArea)
x,y,w,h = cv.boundingRect(c)
cv.rectangle(cont_img,(x,y),(x+w,y+h),(255,0,0),5)
cv.putText(cont_img,"BLUE",(x,y),cv.FONT_HERSHEY_DUPLEX,1,(0,0,0))
cv.imshow("dddd",cont_img)



cv.waitKey(0)