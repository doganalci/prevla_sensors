import os

#Disable tf warning and info
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import mediapipe as mp
import numpy as np
import sys
import subprocess
import datetime
import time
import csv
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import ntplib
import cv2

# NTP sunucusu adresi
ntp_server = "time.google.com"

# NTP sunucusuna bağlanma
client = ntplib.NTPClient()
response = client.request(ntp_server)


#time.sleep(5)


################################
#CV2 text settings
font = cv2.FONT_HERSHEY_SIMPLEX
org = (5, 20)
fontScale = 0.5
color = (255, 0, 0)
thickness = 1
################################

#######################################
#Parameters

ploting = int(sys.argv[1])
deney_no = int(sys.argv[2]) # 0 dı
isHandOpen = bool(int(sys.argv[3]))
print(isHandOpen)



########################################
import ntplib

# NTP sunucusu adresi
ntp_server = "time.google.com"

# NTP sunucusuna bağlanma
client = ntplib.NTPClient()
def differ():
    
    while True:
        try:
            print("Connection Establish")
            return client.request(ntp_server).tx_time-time.time()   
        except:
            print("Time Stamp Connection Error\nRestablish connection")
        

dif = differ()

def getTime():
    return time.time() + dif

###############
#Inital Veriables
start = 0
end = 0
image_no = 0
ff=0
###############

#fc = open('/home/inosens/Desktop/mmwave_ti_ros/ros_driver/log//home/inosens/Desktop/data_collection/sensor_data/mediapipe.csv', file_module)
#fk = open('/home/inosens/Desktop/mmwave_ti_ros/ros_driver/log/deney_loglari.cvs', file_module)

fc = open('/home/inosens/Desktop/data_collection/sensor_data/mediapipe.csv', 'a')

#fk = open('deney_loglari.cvs', file_module)


start=datetime.datetime.now()
fps=0


cap = cv2.VideoCapture(0) ## Opens file or camera (0)

## Mediapipe pose solution
mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils ## Drawing Util
pose = mpPose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.8)
mpHand = mp.solutions.hands
hand = mpHand.Hands()

def draw(image,x,y,z,stamp,image_no,deney_no):
    cv2.imshow("Image",image)
    cv2.moveWindow('Image', 1400, 0)
    
while True:
    
    success , image = cap.read()
    
    if(not success):
        continue
    
    ###########################################################
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    if(isHandOpen):
        handResult = hand.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    imageHeight, imageWidth, _ = image.shape
    ###########################################################

    N = 33

    ############################
    x_points = np.zeros(N)
    y_points = np.zeros(N)
    z_points = np.zeros(N)

    

    x_NormalizePoints = np.zeros(N)
    y_NormalizePoints = np.zeros(N)


    hand_x_points = np.zeros(42)
    hand_y_points = np.zeros(42)
    hand_z_points = np.zeros(42)
    hand_x_NormalizePoints = np.zeros(42)
    hand_y_NormalizePoints = np.zeros(42)
    
    ############################

    p = 0

    

    if(isHandOpen and handResult.multi_hand_landmarks and results.pose_landmarks):
        handsType = []
        myHands = []
        for h in handResult.multi_handedness:
            handType = h.classification[0].label
            handsType.append(handType)
        for handLandMarks in handResult.multi_hand_landmarks:
            myHand = []
            for landMark in handLandMarks.landmark:
                myHand.append(landMark)
            myHands.append(myHand)  

        for (handLocation, ht) in zip(myHands, handsType):

            if ht == 'Right':
                results.pose_landmarks.landmark[15].x = handLocation[0].x
                results.pose_landmarks.landmark[21].x = handLocation[4].x
                results.pose_landmarks.landmark[19].x = handLocation[5].x
                results.pose_landmarks.landmark[17].x = handLocation[17].x

                results.pose_landmarks.landmark[15].y = handLocation[0].y
                results.pose_landmarks.landmark[21].y = handLocation[4].y
                results.pose_landmarks.landmark[19].y = handLocation[5].y
                results.pose_landmarks.landmark[17].y = handLocation[17].y

                results.pose_landmarks.landmark[15].z = handLocation[0].z
                results.pose_landmarks.landmark[21].z = handLocation[4].z
                results.pose_landmarks.landmark[19].z = handLocation[5].z
                results.pose_landmarks.landmark[17].z = handLocation[17].z

            if ht == 'Left':
                results.pose_landmarks.landmark[16].x = handLocation[0].x
                results.pose_landmarks.landmark[22].x = handLocation[4].x
                results.pose_landmarks.landmark[20].x = handLocation[5].x
                results.pose_landmarks.landmark[18].x = handLocation[17].x

                results.pose_landmarks.landmark[16].y = handLocation[0].y
                results.pose_landmarks.landmark[22].y = handLocation[4].y
                results.pose_landmarks.landmark[20].y = handLocation[5].y
                results.pose_landmarks.landmark[18].y = handLocation[17].y

                results.pose_landmarks.landmark[16].z = handLocation[0].z
                results.pose_landmarks.landmark[22].z = handLocation[4].z
                results.pose_landmarks.landmark[20].z = handLocation[5].z
                results.pose_landmarks.landmark[18].z = handLocation[17].z
        
    dataBaseList = []

    if results.pose_landmarks:
        stamp = getTime() # Time stamp
        currentTime = time.ctime(getTime()) # Current Time (Ex: Mon Mar 15 14:44:25 2021)

        psLm = results.pose_landmarks.landmark
    
        mpDraw.draw_landmarks(image,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        
        
        
        dataBaseList.append(stamp)
        dataBaseList.append(currentTime)
        

        for item,point in enumerate(mpPose.PoseLandmark):
            
            normalizedLandmark = psLm[item]
            pixelCoordinatesLandmark = mpDraw._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
            if(pixelCoordinatesLandmark):
                x_points[item] = normalizedLandmark.x        
                y_points[item] = normalizedLandmark.y
                z_points[item] = normalizedLandmark.z
                x_NormalizePoints[item] = pixelCoordinatesLandmark[0]
                y_NormalizePoints[item] = pixelCoordinatesLandmark[1]
        
                

            p+=1
            
            dataBaseList.append(x_points[item])
            dataBaseList.append(y_points[item])
            dataBaseList.append(z_points[item])
            dataBaseList.append(x_NormalizePoints[item])
            dataBaseList.append(y_NormalizePoints[item])
        
      
        
        
        
        

        image_no +=1 

        p = 0
        
        #fun(image_no,x_points,y_points,x_points,delay,stamp,image)
        #draw(image,x_points,y_points,x_points,stamp,image_no,deney_no=1)

    if(isHandOpen and handResult.multi_hand_landmarks):
        handsType = []
        for h in handResult.multi_handedness:
            handType = h.classification[0].label
            handsType.append(handType)
        for hLm,h in zip(handResult.multi_hand_landmarks,handsType):
            i = 0
            print("hand",handsType)
            if(h == "Right"):
                i = 21
            

            for item,point in enumerate(mpHand.HandLandmark):
                hand_normalizedLandmark = hLm.landmark[item]

                hand_pixel = mpDraw._normalized_to_pixel_coordinates(hand_normalizedLandmark.x, hand_normalizedLandmark.y, imageWidth, imageHeight)
                    
                if(hand_pixel):
                    hand_x_points[item+i] = hand_normalizedLandmark.x        
                    hand_y_points[item+i] = hand_normalizedLandmark.y
                    hand_z_points[item+i] = hand_normalizedLandmark.z
                    hand_x_NormalizePoints[item+i] = hand_pixel[0]
                    hand_y_NormalizePoints[item+i] = hand_pixel[1]
            
                


            mpDraw.draw_landmarks(
                image,
                hLm,
                mpHand.HAND_CONNECTIONS)

    for index in range(21):
        dataBaseList.append(x_points[index])
        dataBaseList.append(y_points[index])
        dataBaseList.append(z_points[index])
        dataBaseList.append(x_NormalizePoints[index])
        dataBaseList.append(y_NormalizePoints[index]) 

    for index in range(42):
        dataBaseList.append(hand_x_points[index])
        dataBaseList.append(hand_y_points[index])
        dataBaseList.append(hand_z_points[index])
        dataBaseList.append(hand_x_NormalizePoints[index])
        dataBaseList.append(hand_y_NormalizePoints[index])

    print(len(dataBaseList))
    out1 = csv.writer(open('/home/inosens/Desktop/data_collection/sensor_data/burak.csv', 'a')) #data base'e gidecek olan data
    out1.writerow(dataBaseList)       

    cv2.imshow("Image",image)
    cv2.moveWindow('Image', 1400, 0)
    

    #cv2.imshow("Image",image)

    cv2.waitKey(1)