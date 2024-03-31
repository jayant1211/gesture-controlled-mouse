'''
1. get camera feed - x
2. run inference
   - detect and draw - x
   - get coordinates - x
3. perform mouse functions
    - move mouse - index is open; all other is close; status = ["close","open","close","close","close"] - x 
    - left click - index and thmmb open; other close - x
    - right click - x
    - hold and drag
'''

import cv2
import handDetectionModule as hdm
import pyautogui
import numpy as np
import math

flag = False
screenW, screenH = pyautogui.size() 
locx, locy = pyautogui.position()
smoothening_factor=5

cap = cv2.VideoCapture(0)

def isTouching(p1,p2):
    dist = math.sqrt(pow(p2[0]-p1[0],2) + pow(p2[1]-p1[1],2))
    return dist < 30

def get_open_status(x,y):
    if len(x)!=21:
        return
    status = ["open","open","open","open","open"]
    #fingers
    for i in range(2,6):
        if(y[4*i - 1]>y[4*i]):
            status[i-1] = "open"
        else:
            status[i-1] = "close"

    #for thumb
    is_right = x[17]>x[2]
    if is_right:
        if(x[3]>x[4]):
            status[0]="open"
        else:
            status[0]="close"
    else:
        if(x[3]>x[4]):
            status[0]="close"
        else:
            status[0]="open"
    return status

def caseMovement(point,imgW,imgH):
    x = point[0]
    y = point[1]

    x = np.interp(x,(imgW//4+10,3*imgW//4 - 10),(0,screenW))
    y = np.interp(y,(imgH//4+10,3*imgH//4 - 10),(0,screenH))
    global locy
    global locx
    locx = locx + (x-locx)//smoothening_factor
    locy = locy + (y-locy)//smoothening_factor
    pyautogui.moveTo(locx,locy)


def perform_mouse_function(x,y,status,imgW,imgH,frame):
    if len(x)!=21:
        return
    thumb, index, middle, ring, pinky = (x[4],y[4]),(x[8],y[8]),(x[12],y[12]),(x[16],y[16]),(x[20],y[20])
    #case movement 
    global flag
    if(status == ["close","open","close","close","close"] ):
        if flag:
            pyautogui.mouseUp(button='left')
            flag = False
        cv2.circle(frame,(int(index[0]),int(index[1])),3,(255,255,255),-1)
        caseMovement(index,imgW,imgH)

    #case left clcik
    if(status==["open","open","close","close","close"] and isTouching(thumb,index)):
        if flag:
            pyautogui.mouseUp(button='left')
            flag = False
        cv2.circle(frame,(int(index[0]),int(index[1])),3,(255,255,255),-1)
        cv2.circle(frame,(int(thumb[0]),int(thumb[1])),3,(255,255,255),-1)
        pyautogui.click(button='left')

    #case right 
    if(status==["close","open","open","close","close"] and isTouching(middle,index)):
        if flag:
            pyautogui.mouseUp(button='left')
            flag = False
        cv2.circle(frame,(int(index[0]),int(index[1])),3,(255,255,255),-1)
        cv2.circle(frame,(int(middle[0]),int(middle[1])),3,(255,255,255),-1)
        pyautogui.click(button='right')

    #case hold and drag
    if(status==["close","open","open","open","close"]):
        if not flag:
            pyautogui.mouseDown(button='left')
            flag = True
        cv2.circle(frame,(int(index[0]),int(index[1])),3,(255,255,255),-1)
        cv2.circle(frame,(int(middle[0]),int(middle[1])),3,(255,255,255),-1)
        cv2.circle(frame,(int(ring[0]),int(ring[1])),3,(255,255,255),-1)
        caseMovement(index,imgW,imgH)
        

while cap.isOpened():
    _, frame = cap.read()

    frame = hdm.detectAndDraw(frame)
    imgH, imgW = frame.shape[:2]
    x_cords, y_cords = hdm.getCoordinates()
    status =get_open_status(x_cords,y_cords)
    #print(status)
    cv2.rectangle(frame,(imgW//4,imgH//4),(3*imgW//4,3*imgH//4),(0,255,0),1)
    perform_mouse_function(x_cords,y_cords,status,imgW,imgH,frame)
    
    cv2.imshow("Frame",frame)

    if cv2.waitKey(1)& 0xff==ord('q'):
        break

cv2.destroyAllWindows()
cap.release()