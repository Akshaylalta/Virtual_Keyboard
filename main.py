#Importing libraries
import cv2
import HandTrackingModule as htm
import mediapipe as mp
import math
from time import sleep
import pyautogui

#capture webcam
cap=cv2.VideoCapture(0)

#using handtrackingmodule import handdetector
detector = htm.handDetector(detectionCon=0.8)

#Create a class Key
class Key():

    def __init__(self,x,y,w,h,text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text=text

#define a function draw for put rectangle around keys
def draw(img,keys,alpha=0.5):

   #take a copy of image for drawing
    img_copy=img.copy()
        
    for Key in keys:
        x=Key.x
        y=Key.y
        w=Key.w
        h=Key.h
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),-1)
        cv2.putText(img,Key.text,(x+w//2-14,y+43),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

    #add copy_img and orginal_img - for decreasing the capacity of drawing box
    res=cv2.addWeighted(img,alpha,img_copy,1-alpha,1)
    
    #put it back to orginal image 
    img=res 
    return img

w,h = 80, 75  #width & height of keys
X, Y = 200, 100
keys=[]
letters =list("QWERTYUIOPASDFGHJKLZXCVBNM")
finaltext=''
#assigning x,y,w,h for each keys
for i,l in enumerate(letters):
    if i<10:
        keys.append(Key(X + i*w + i*5, Y, w, h, l))
    elif i<19:
        keys.append(Key(X + (i-10)*w + i*5, Y + h + 5,w,h,l))
    else:
        keys.append(Key(X + (i-19)*w + i*5, Y + 2*h + 10, w, h, l))

keys.append(Key(X+25, Y+3*h+15, 5*w, h, "Space"))
keys.append(Key(X+8*w + 50, Y+2*h+10, w+5, h, "clr"))
keys.append(Key(X+5*w+30, Y+3*h+15, 5*w, h, "<--"))



while True:
    #read image from video
    success,image=cap.read()
    if not success:
        break
    #resize image
    image = cv2.resize(image, (1280, 760))

    #detect hand landmarks
    image=detector.findHands(image)
    
    #detect position of hands
    lmlist=detector.findPosition(image)
    
    #draw keyboard on image
    image=draw(image,keys,alpha=0.6) #alpha is the capacity of rectangle

    if len(lmlist)!=0:
        #assign coordinates of index tip and thumb tip
        x1,y1=lmlist[8][1:]  
        x2,y2=lmlist[4][1:]

        #lentgh between index tip & thumb tip
        length = math.hypot(x2-x1,y2-y1)
        c1,c2=int((x1+x2)/2),int((y1+y2)/2)
        print(length)
        
        for Key in keys:
            x=Key.x
            y=Key.y
            w=Key.w
            h=Key.h

            #if finger over each keys
            if x<x1<x+w and y<y1<y+h:
                #bright the keys
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),-1)
                cv2.putText(image,Key.text,(x+w//2-14,y+43),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)

                #key selection
                if length<30:
                    cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.circle(image,(c1,c2),5,(0,255,0),-1)
                    if Key.text=="Space":
                       finaltext+=" "
                    elif Key.text=="<--":
                        finaltext=finaltext[:-1]
                    elif Key.text=="clr":
                        finaltext=""
                    else:
                        finaltext+=Key.text
                        # pyautogui.keyDown(Key.text)
                        # pyautogui.keyUp(Key.text)

    #print typing letters in screen     
    cv2.rectangle(image,(X, Y-h-10),(1050, 90),(0,0,0),-1)
    cv2.putText(image,finaltext,(X+150,Y-30),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,255,255),2)         
    
    sleep(0.2)
    print(finaltext)
    #show video
    cv2.imshow('video',image)
    
    #if press q close the video 
    if cv2.waitKey(1) ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()