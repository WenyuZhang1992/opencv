import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, img = cap.read()
    cv2.rectangle(img,(400,400),(100,100),(0,255,0),0)
    crop_img = img[100:400, 100:400]
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
            cv2.CHAIN_APPROX_NONE)
    max_area = -1
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=contours[ci]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 180 / math.pi
        if angle <= 90:
            count_defects += 1
            cv2.circle(drawing,far,1,[0,0,255],2)
        cv2.line(drawing,start,end,[0,0,255],0)
    if count_defects == 0:
        cv2.putText(crop_img,"1", (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    elif count_defects == 1:
        str = "2"
        cv2.putText(crop_img, str, (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    elif count_defects == 2:
        cv2.putText(crop_img,"3", (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    elif count_defects == 3:
        cv2.putText(crop_img,"4", (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    else:
        cv2.putText(crop_img,"5", (25,25),\
                    cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
    cv2.rectangle(crop_img,(20,1), (51,30), (0,0,255), 3)
    #all_img = np.hstack((drawing, drawing2))
    #cv2.imshow('Convex Hull and Convexity Defects--WENYU ZHANG', all_img)
    cv2.imshow('Original--WENYU ZHANG',crop_img)
    cv2.imshow('Recognition--WENYU ZHANG',drawing)
    k = cv2.waitKey(10)
    if k == 27:
        break