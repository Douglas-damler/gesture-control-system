
import cv2
import numpy as np
from collections import deque
from processd import current_process
import pyautogui as gui
import time
import pickle



buff=128
oldx=0
oldy=0
currx=0
curry=0
counter=0
counter1=0
call_counter=0;
flag=0
last_motion=""
flag_do_gesture=0
current_gesture = []

yellow_lower = np.array([7, 96, 85])                          # HSV yellow lower
yellow_upper = np.array([255, 255, 255])    

# blue_lower = np.array([110,50,50])
# blue_upper = np.array([130,255,255])

with open("range.pickle", "rb") as f:
        t = pickle.load(f)
        print(t)

# blue_lower = np.array([94, 80, 50])
# blue_upper = np.array([126, 255, 255])


blue_lower = np.array([t[0], t[1], t[2]])
blue_upper = np.array([t[3], t[4], t[5]])

cap = cv2.VideoCapture(0)



def perform(gesture):
    current=current_process()
    # print("Perform "+ current +" Gesture:" + gesture)
    if(current=="chrome"):
        print("Chrome")
        if(gesture=="N"):
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
            gui.hotkey('DOWN')
                
        if(gesture=="S"):
            gui.hotkey('UP')
            gui.hotkey('UP')
            gui.hotkey('UP')
            gui.hotkey('UP')
            gui.hotkey('UP')

        if(gesture=="E"):
            gui.hotkey('right')
            gui.hotkey('right')
            gui.hotkey('right')

        if(gesture=="W"):
            gui.hotkey('left')
            gui.hotkey('left')
            gui.hotkey('left')


        if(gesture=="SW"):
            gui.hotkey('ctrl','-')

        if(gesture=="NE"):
            gui.hotkey('ctrl','+')

        if(gesture=="SE"):
            gui.hotkey('alt','f4')
        
            
    if(current=="vlc"):
        print("VLC")
        if(gesture=="S"):
            gui.press('down')
            # gui.hotkey('DOWN')

        if(gesture=="N"):
            gui.press('up')
            # gui.hotkey('UP')

        if(gesture=="E"):
            gui.press('right')

        if(gesture=="W"):
            gui.press('left')

        if(gesture=="SW"):
            print("SW")
            # gui.press('space')
            gui.hotkey('space')

        if(gesture=="SE"):
            print("SE")
            gui.hotkey('alt','f4')


    if(current=="music"):
        if(gesture=="S"):
            gui.hotkey('volumedown')

        if(gesture=="N"):
            gui.hotkey('volumeup')

        if(gesture=="SW"):
            gui.hotkey('space')

        if(gesture=="SE"):
            gui.hotkey('alt','f4')

    if(current == "PPT"):
        print("PPT")
        if(gesture=='E'):
            gui.press('right')
        if(gesture=='W'):
            gui.press('left')


    if(current=="game"):
       
         print("game")
         if(gesture=="S"):
             gui.keyUp('d')
             gui.keyUp('w') 
             gui.keyUp('a')
             
             gui.keyDown('s')
            #  gui.press('s')
            #  gui.press('s')
            # gui.keyUp('DOWN')
             
             """
             counter1=20
             while(counter1>0):
                 gui.hotkey('DOWN')
                 counter1=counter1-1 
                 """
        
         if(gesture=="N"):
            
            gui.keyUp('a')
            gui.keyUp('d')
            gui.keyUp('s')
            
            gui.keyDown('w')
            # gui.press('w')
            # gui.press('w')
            """
            counter1=20
            while(counter1>0):
                gui.hotkey('UP')
                counter1=counter1-1 
                """
                
         if(gesture=="E"):
             
            gui.keyUp('a')
            gui.keyUp('w')
            gui.keyUp('s')
            
            gui.keyDown('d')

            # gui.press('d')
            # gui.press('d')
            """
            counter1=30
            gui.keyDown('RIGHT')
            while(counter1>0):
                counter1=counter1-1
            gui.keyUp('RIGHT')
            """
                
         if(gesture=="W"):
            
            gui.keyUp('w')
            gui.keyUp('s')
            gui.keyUp('d')
                
            gui.keyDown('a')
            # gui.press('d')
            # gui.press('d')
            
            """
            counter1=30
            gui.keyDown('LEFT')
            while(counter1>0):
                counter1=counter1-1
            gui.keyUp('LEFT')
            """
                
            
            
        
    
    


while(1):

    
    # Take each frame
    _, frame = cap.read()
    
    #for not touching frame
    img=frame
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (480, 360))
    #this part is over

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    
    blur = cv2.medianBlur(mask, 15)
    blur = cv2.GaussianBlur(blur , (5,5), 0)
    temp,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    _,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow("Thresh", thresh)

    # _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours = contours[0] if len(contours) == 2 else contours[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # print(len(contours))
    
    
    
    if(len(contours)==0):
        line_pts = deque(maxlen = buff)
        # print("Empty Image")
       
        """processed_gesture_hand1 = tuple(process_gesture(current_gesture))
        
        if flag_do_gesture == 0:                                            # flag_do_gesture to make sure that gesture runs only once and not repeatedly
            if processed_gesture_hand1 != ():
                do_gesture_action(processed_gesture_hand1)
            flag_do_gesture = 1
        print(processed_gesture_hand1)     """                                 # for debugging purposes
        created_gesture = []
        flag = True

    else:
        flag_do_gesture = 0
        #max_contour = max(contours, key = cv2.contourArea)
        
        area_t=0;
        thresh_area=2000;
        for i in contours:
            temp=cv2.contourArea(i)
            # print("inside: ",temp)
            if(temp>area_t and temp<thresh_area):
                area_t=temp
                max_contour=i
            
        
        rect1 = cv2.minAreaRect(max_contour)
        (w, h) = rect1[1]
        area_c = w*h
        # print("area:",area_c)

        box = cv2.boxPoints(rect1)
        box = np.int0(box)
        
        
        
        if(area_t>350):
            # print("suff area:",area_c)
            
            center=list(rect1[0])
            currx=int(center[0])
            curry=int(center[1])
            print("last_motion:",last_motion)
            # print("curr pos: ",currx,curry)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            cv2.circle(img, (currx, curry), 2, (0, 255, 0), 2)
            
            
            
            
            if(counter==0):
                oldx=currx
                oldy=curry


                
            call_counter=call_counter+1
            counter=counter+1
            
            diffx, diffy=0, 0
            if counter>5:
                diffx=currx-oldx
                diffy=curry-oldy
                counter=0

                
            # print("Differences: ",diffx,diffy)   
            
            if(diffx<40 and diffy<40):
                
            
                if(diffx>15 and abs(diffy)<15):
                    last_motion="E"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif(diffx<-15 and abs(diffy)<15):
                    last_motion="W"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif(abs(diffx)<15 and diffy<-15 ):
                    last_motion="N"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                   
                elif(abs(diffx)<15 and diffy>15):
                    last_motion="S"
                    perform(last_motion);
                    current_gesture.append(last_motion)
     
                    
                elif diffx > 20 and diffy > 20:
                    last_motion="SE"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                        
                elif diffx < -20 and diffy > 20:
                    last_motion="SW"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif diffx > 20 and diffy < -20:
                    last_motion="NE"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                elif diffx < -20 and diffy < -20:
                    last_motion="NW"
                    perform(last_motion);
                    current_gesture.append(last_motion)
                    
                
                    
                
                
            flag=False
            
        
    cv2.imshow("Detected: ", img)    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
