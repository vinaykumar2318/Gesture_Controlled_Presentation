#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('pip', 'install cvzone')


# In[ ]:


get_ipython().run_line_magic('pip', 'install --user mediapipe')


# In[1]:


import cv2
import os

import mediapipe as mp

import numpy as np


# 
# # Setting up Camera

# In[2]:


width = 1280
height = 720
gesture_threshold = 300
path = "project_presentation"


# In[3]:


cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)


#here we will get the path of all images
imgpaths = sorted(os.listdir(path), key=len)

imgpaths = imgpaths[:15]


# # Handtracking Module

# In[4]:


from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)


# In[5]:


#helps in changing the img num
imgnum = 0
buttonPressed = False
buttonCounter = 0
buttonDelay = 20
annotations = [[]]
annotationNum = 0
annotationStart = False
colorChange = False
colorDraw = False
colorControl = False
colorCounter = 0
cursor_color= (0, 0, 255)
cursor_color_draw = (0, 0, 255)
cursorColor = [(0, 0, 255),(0, 255, 0)]
thumb_open = False


wsmall = int(220*1)
hsmall = int(120*1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    fullpathImg = os.path.join(path,imgpaths[imgnum])
    imgCurr = cv2.imread(fullpathImg)
    
    hands, img = detector.findHands(img)
    cv2.line(img,(0,gesture_threshold),(width,gesture_threshold),(0,255,0), 10)
    
    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        #constraining the area for easy movability of cursor
        xValue = int(np.interp(lmList[8][0], [width//2 - 150, width], [0, width]))
        yValue = int(np.interp(lmList[8][1], [100, height], [0, height]))
        indexFinger = xValue, yValue
        
        
        if cy<=gesture_threshold: #if hand is above threshold line
            annotationStart = False
            #first gesture- left
            if fingers == [1, 0, 0, 0, 0]:
                annotationStart = False
                print("Left")
                if imgnum>0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNum = 0
                    imgnum -= 1
                
            #second gesture- Right
            if fingers == [0, 0, 0, 0, 1]:
                annotationStart = False
                print("Right")
                if imgnum < len(imgpaths)-1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNum = 0
                    imgnum += 1
    
                    
        #third gesture- pointer
        if fingers == [0, 1, 1, 0, 0] or colorChange:
            if fingers == [0, 1, 1, 0, 0] or fingers == [1, 1, 1, 0, 0]:
                colorChange = True
            else:
                colorChange = False
                colorCounter = 0
                cursor_color = (0, 0, 255)
                
                
            cv2.circle(imgCurr, indexFinger, 20, cursor_color, cv2.FILLED)
            annotationStart = False
            
            #for changing cursor color
            if colorControl:
                colorCounter += 1
                if colorCounter > 20:
                    colorCounter = 0
                    colorControl = False
                    
            if fingers[0] == 1 and colorControl is False:
                colorControl = True
                if not thumb_open:
                    thumb_open = True
                    cursor_color = (0, 255, 0)
                else:
                    thumb_open = False
                    cursor_color = (0, 0, 255)
                    
                    
            
        #fourth gesture- drawing
        if fingers == [0, 1, 0, 0, 0] or colorDraw:
            if fingers == [0, 1, 0, 0, 0] or fingers == [1, 1, 0, 0, 0]:
                colorDraw = True
            else:
                colorDraw = False
                colorCounter = 0
                cursor_color_draw = (0, 0, 255)
            
            tim = 1
            if annotationStart is False:
                annotationStart = True
                annotationNum += 1
                annotations.append([])
                
            cv2.circle(imgCurr, indexFinger, 20, cursor_color_draw, cv2.FILLED)
            annotations[annotationNum].append(indexFinger)
            
            #for changing cursor color
            if colorControl:
                colorCounter += 1
                if colorCounter > 20:
                    colorCounter = 0
                    colorControl = False
                    
            #print(f"Color Control: {colorControl}")
            if fingers[0] == 1 and colorControl is False:
                colorControl = True
                if not thumb_open:
                    thumb_open = True
                    cursor_color_draw = cursorColor[1]
                else:
                    thumb_open = False
                    cursor_color_draw = cursorColor[0]
            
        else:
            annotationStart = False
            
        #fifth gesture- erasing
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationNum>=0:
                    annotations.pop(-1)
                    annotationNum -= 1
                    buttonPressed = True
                    
        #sixth gesture- closing
        if fingers == [0,1,0, 0, 1]:
            print("Close")
            cv2.destroyAllWindows()
            break
            
    else:
        annotationStart = False
    
    
    #button pressed iterations to make the transitions slow
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False
            colorControl = False
        
        
    
    #drawing is done here
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                tim = i%2
                cv2.line(imgCurr,annotations[i][j-1],annotations[i][j],cursorColor[tim], 12)
    
    
    #adding webcam on the slide
    imgSmall = cv2.resize(img, (wsmall,hsmall))
    imgCurr = cv2.resize(imgCurr, (width,height))
    h, w, _ = imgCurr.shape
    imgCurr[0:hsmall,w-wsmall:w] = imgSmall
    
#     cv2.imshow("Image",img)
    cv2.imshow("Slides",imgCurr)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


# In[ ]:





# In[ ]:




