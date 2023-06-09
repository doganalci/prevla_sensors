import mediapipe as mp
import numpy as np
import sys
import datetime
import time
import csv
import ntplib
import cv2
import pyodbc 
import matplotlib



#matplotlib.use("QTAgg")

#######################################
#Parameters


isHandOpen = bool(int(sys.argv[1]))

########################################


########################################

#ODBC Serverine databaseden alınan "connection string" ile bağlanıldı.
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=193.35.200.106;DATABASE=Prevla;UID=SA;PWD=hP337^9nArG&;TrustServerCertificate=Yes')
#print(cnxn,"Bağlandı")

########################################


########################################
# Timestamp Calculation
# 

# NTP server adress
ntp_server = "time.google.com"

# Connection NTP Server
client = ntplib.NTPClient()


#Calculating difference between Google Timestamp and System Timestamp
def differ():
    
    while True:
        try:
            print("Connection Establish")
            return client.request(ntp_server).tx_time-time.time()   
        except:
            print("Time Stamp Connection Error\nRestablish connection")
        
#Saving diffrence
dif = differ()

#Get timestamp
def getTime():
    return time.time() + dif


########################################
# MediaPipe and cv

cap = cv2.VideoCapture(0) ## Opens file or camera (0)

## Mediapipe pose solution
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.8)

## Mediapipe hand solution
mpHand = mp.solutions.hands
hand = mpHand.Hands()

## Drawing Util
mpDraw = mp.solutions.drawing_utils 

########################################
  
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


    ############################
    N = 33
    pose_x_points = np.zeros(N)
    pose_y_points = np.zeros(N)
    pose_z_points = np.zeros(N)

    pose_x_NormalizePoints = np.zeros(N)
    pose_y_NormalizePoints = np.zeros(N)

    hand_x_points = np.zeros(42)
    hand_y_points = np.zeros(42)
    hand_z_points = np.zeros(42)

    hand_x_NormalizePoints = np.zeros(42)
    hand_y_NormalizePoints = np.zeros(42)
    
    ############################
    ## Data
    dataBaseList = []

    ##Taking timestamp and 
    stamp = getTime() # Time stamp
    currentTime = time.ctime(getTime()) # Current Time (Ex: Mon Mar 15 14:44:25 2021)


    dataBaseList.append(stamp)
    dataBaseList.append(datetime.datetime.now())

    ## Synchronization of hand data and pose data
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
        
   
    ## Saving Pose data
    if results.pose_landmarks:
        
        psLm = results.pose_landmarks.landmark
    
        mpDraw.draw_landmarks(image,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        
        for item,point in enumerate(mpPose.PoseLandmark):
            
            normalizedLandmark = psLm[item]
            pixelCoordinatesLandmark = mpDraw._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
            if(pixelCoordinatesLandmark):
                pose_x_points[item] = normalizedLandmark.x        
                pose_y_points[item] = normalizedLandmark.y
                pose_z_points[item] = normalizedLandmark.z
                pose_x_NormalizePoints[item] = pixelCoordinatesLandmark[0]
                pose_y_NormalizePoints[item] = pixelCoordinatesLandmark[1]
        

    ## Saving hand Data
    if(isHandOpen and handResult.multi_hand_landmarks):
        handsType = []
        for h in handResult.multi_handedness:
            handType = h.classification[0].label
            handsType.append(handType)
        for hLm,h in zip(handResult.multi_hand_landmarks,handsType):
            i = 0
            #print("hand",handsType)
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
    
    # Saving data to database 
    if(handResult.multi_hand_landmarks or results.pose_landmarks):

        for index in range(33):
            dataBaseList.append(pose_x_points[index])
            dataBaseList.append(pose_y_points[index])
            dataBaseList.append(pose_z_points[index])
            dataBaseList.append(pose_x_NormalizePoints[index])
            dataBaseList.append(pose_y_NormalizePoints[index]) 

        for index in range(42):
            dataBaseList.append(hand_x_points[index])
            dataBaseList.append(hand_y_points[index])
            dataBaseList.append(hand_z_points[index])
            dataBaseList.append(hand_x_NormalizePoints[index])
            dataBaseList.append(hand_y_NormalizePoints[index])

        #cursor = cnxn.cursor()
        with open("sql.txt" ,'r') as my_file:
            sql = my_file.read()    

        #cursor.execute(sql,tuple(dataBaseList))
        #cnxn.commit()
        
        out1 = csv.writer(open('/home/inosens/Desktop/data_collection/sensor_data/burak.csv', 'a')) #data base'e gidecek olan data
        out1.writerow(dataBaseList)

    #print(len(dataBaseList))
           

    cv2.imshow("Image",image)
    cv2.moveWindow('Image', 1400, 0)

    
    

    #cv2.imshow("Image",image)

    cv2.waitKey(1)