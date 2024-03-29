import cv2
import numpy as np
import pyautogui
import handDetectionModule as hdm
import math

flag = False
cap = cv2.VideoCapture(0)

x_max = 0
screenW, screenH = pyautogui.size()
locx,locy=0,0
smoothening_factor = 5

def isTouching(p1,p2,log):
    return (math.sqrt(pow(p2[0]-p1[0],2) + pow(p2[1]-p1[1],2))<35) 

def get_open_status(x,y):
    status = ["open","open","open","open","open"]
    if(len(x)==21):
        #handling fingers
        #7-8, 11-12, 15-16, 19-20
        for i in range(2,6):
            if(y[4*i-1] - y[4*i]>0):
                status[i-1] = "open"
            else:
                status[i-1] = "close"

        #handling thumb case:
        is_right = (x_cords[17]>x_cords[2]) #for checking handedness
        if is_right:
            if(x_cords[4]>x_cords[3]):
                status[0] = "close"
            else:
                status[0] = "open"
        else:
            if(x_cords[4]>x_cords[3]):
                status[0] = "open"
            else:
                status[0] = "close"
        return status

#mouse function
def case_movement(point):
    global locx
    global locy
    x = point[0]
    y = point[1]
    # Convert Coordinates
    # np.interplot maps one range to another desired range, (point, original range, desired range)
    x = np.interp(x, (imgW//4 + 30,3*imgW//4 - 30), (0, screenW))  
    y = np.interp(y, (imgH//4 + 30,3*imgH//4 - 30), (0, screenH))

    #check if these are out of bounds
    x = min(x,screenW-1)
    y = min(y,screenH-1)

    #smoothening
    x = locx + (x - locx)/smoothening_factor
    y = locy + (y - locy)/smoothening_factor
    pyautogui.moveTo(x,y,duration=0)
    locy = y
    locx = x
    

def perform_mouse_funtion(status, x_cords,y_cords,imgH,imgW,frame):
    global flag
    if(len(x_cords)!=21):
        return frame
    thumb, index, middle, ring, pinky = (x_cords[4],y_cords[4]),(x_cords[8],y_cords[8]),(x_cords[12],y_cords[12]),(x_cords[16],y_cords[16]),(x_cords[20],y_cords[20])
    
    #case movement
    if(status[1]=="open" and status.count("open")==1): 
        if flag:
            flag = False
            pyautogui.mouseUp(button='left')
        cv2.circle(frame,(int(index[0]),int(index[1])),5,(0,255,0),-1)
        case_movement(index)
        
    #case left click
    elif(isTouching(index,thumb,"index and thumb") and status == ["open","open","close","close","close"]):
        if flag:
            flag = False
            pyautogui.mouseUp(button='left')
        cv2.circle(frame,(int(index[0]),int(index[1])),5,(0,0,255),-1)
        pyautogui.leftClick()
    
    #case right click
    elif(isTouching(index,middle,"index and middle") and status == ["close","open","open","close","close"]):
        if flag:
            flag = False
            pyautogui.mouseUp(button='left')
        cv2.circle(frame,(int(index[0]),int(index[1])),5,(0,0,255),-1)
        pyautogui.rightClick()
        
    #drag case
    elif(status==["close","open","open","open","close"]):
        if not flag:
            flag = True
            pyautogui.mouseDown(button='left')
            pass
        cv2.circle(frame,(int(index[0]),int(index[1])),5,(0,0,255),-1)
        cv2.circle(frame,(int(middle[0]),int(middle[1])),5,(0,0,255),-1)
        cv2.circle(frame,(int(ring[0]),int(ring[1])),5,(0,0,255),-1)
        case_movement(index)

    return frame

while cap.isOpened():
    ret, frame = cap.read()
    if ret is False:
        continue
    result_frame = hdm.detectAndDraw(frame)
    x_cords, y_cords = hdm.getCoordinates()
    imgH,imgW = result_frame.shape[:2]  
    status  = (get_open_status(x_cords,y_cords)) #gets status of all fingers and thumb - open or close
    #Perform mouse function
    result_frame = perform_mouse_funtion(status, x_cords,y_cords,imgH,imgW,result_frame)
    
    #display it
    cv2.rectangle(result_frame,(imgW//4,imgH//4),(3*(imgW//4),3*(imgH//4)),(0,255,0),1)
    cv2.imshow("Frame",cv2.resize(result_frame,(900,600)))
    if cv2.waitKey(1) & 0xFF == 27:
        break

