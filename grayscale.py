import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, img = cap.read()
    # Draw a rectangle and obtain the img
    cv2.rectangle(img,(400,400),(100,100),(0,255,0),0)
    crop_img = img[100:400, 100:400]
    # Convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grey--WENYU ZHANG',grey)
    cv2.imshow('Cropimg--WENYU ZHANG',crop_img)
    k = cv2.waitKey(10)
    if k == 27:
        break