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
import datetime


# NTP sunucusu adresi
ntp_server = "time.google.com"

# NTP sunucusuna bağlanma
client = ntplib.NTPClient()
response = client.request(ntp_server)

import pyodbc 

cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=193.35.200.106;DATABASE=Prevla;UID=SA;PWD=hP337^9nArG&;TrustServerCertificate=Yes')
print(cnxn,"Bağlandı")



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
#print(isHandOpen)



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
    dataBaseList = []
    p = 0
    stamp = getTime() # Time stamp
    currentTime = time.ctime(getTime()) # Current Time (Ex: Mon Mar 15 14:44:25 2021)
    dataBaseList.append(stamp)
    dataBaseList.append(datetime.datetime.now())

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
        
   

    if results.pose_landmarks:
        

        psLm = results.pose_landmarks.landmark
    
        mpDraw.draw_landmarks(image,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        
        
        
        
        

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
            
            #dataBaseList.append(x_points[item])
            #dataBaseList.append(y_points[item])
            #dataBaseList.append(z_points[item])
            #dataBaseList.append(x_NormalizePoints[item])
            #dataBaseList.append(y_NormalizePoints[item])
        
      
        
        
        
        

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
            
    if(handResult.multi_hand_landmarks or results.pose_landmarks):

        for index in range(33):
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

        out1 = csv.writer(open('/home/inosens/Desktop/data_collection/sensor_data/burak.csv', 'a')) #data base'e gidecek olan data
        out1.writerow(dataBaseList)
        cursor = cnxn.cursor()
        sql = """INSERT INTO [dbo].[MediapipeDatas]
           ([mp_1_p1_mp_h_p_timestamp]
           ,[mp_2_p2_date]
           ,[mp_3_p3_x_points_of_PoseLandmark_NOSE]
           ,[mp_4_p4_y_points_of_PoseLandmark_NOSE]
           ,[mp_5_p5_z_points_of_PoseLandmark_NOSE]
           ,[mp_6_p6_x_pixel_points_of_PoseLandmark_NOSE]
           ,[mp_7_p7_y_pixel_points_of_PoseLandmark_NOSE]
           ,[mp_8_p8_x_points_of_PoseLandmark_LEFT_EYE_INNER]
           ,[mp_9_p9_y_points_of_PoseLandmark_LEFT_EYE_INNER]
           ,[mp_10_p10_z_points_of_PoseLandmark_LEFT_EYE_INNER]
           ,[mp_11_p11_x_pixel_points_of_PoseLandmark_LEFT_EYE_INNER]
           ,[mp_12_p12_y_pixel_points_of_PoseLandmark_LEFT_EYE_INNER]
           ,[mp_13_p13_x_points_of_PoseLandmark_LEFT_EYE]
           ,[mp_14_p14_y_points_of_PoseLandmark_LEFT_EYE]
           ,[mp_15_p15_z_points_of_PoseLandmark_LEFT_EYE]
           ,[mp_16_p16_x_pixel_points_of_PoseLandmark_LEFT_EYE]
           ,[mp_17_p17_y_pixel_points_of_PoseLandmark_LEFT_EYE]
           ,[mp_18_p18_x_points_of_PoseLandmark_LEFT_EYE_OUTER]
           ,[mp_19_p19_y_points_of_PoseLandmark_LEFT_EYE_OUTER]
           ,[mp_20_p20_z_points_of_PoseLandmark_LEFT_EYE_OUTER]
           ,[mp_21_p21_x_pixel_points_of_PoseLandmark_LEFT_EYE_OUTER]
           ,[mp_22_p22_y_pixel_points_of_PoseLandmark_LEFT_EYE_OUTER]
           ,[mp_23_p23_x_points_of_PoseLandmark_RIGHT_EYE_INNER]
           ,[mp_24_p24_y_points_of_PoseLandmark_RIGHT_EYE_INNER]
           ,[mp_25_p25_z_points_of_PoseLandmark_RIGHT_EYE_INNER]
           ,[mp_26_p26_x_pixel_points_of_PoseLandmark_RIGHT_EYE_INNER]
           ,[mp_27_p27_y_pixel_points_of_PoseLandmark_RIGHT_EYE_INNER]
           ,[mp_28_p28_x_points_of_PoseLandmark_RIGHT_EYE]
           ,[mp_29_p29_y_points_of_PoseLandmark_RIGHT_EYE]
           ,[mp_30_p30_z_points_of_PoseLandmark_RIGHT_EYE]
           ,[mp_31_p31_x_pixel_points_of_PoseLandmark_RIGHT_EYE]
           ,[mp_32_p32_y_pixel_points_of_PoseLandmark_RIGHT_EYE]
           ,[mp_33_p33_x_points_of_PoseLandmark_RIGHT_EYE_OUTER]
           ,[mp_34_p34_y_points_of_PoseLandmark_RIGHT_EYE_OUTER]
           ,[mp_35_p35_z_points_of_PoseLandmark_RIGHT_EYE_OUTER]
           ,[mp_36_p36_x_pixel_points_of_PoseLandmark_RIGHT_EYE_OUTER]
           ,[mp_37_p37_y_pixel_points_of_PoseLandmark_RIGHT_EYE_OUTER]
           ,[mp_38_p38_x_points_of_PoseLandmark_LEFT_EAR]
           ,[mp_39_p39_y_points_of_PoseLandmark_LEFT_EAR]
           ,[mp_40_p40_z_points_of_PoseLandmark_LEFT_EAR]
           ,[mp_41_p41_x_pixel_points_of_PoseLandmark_LEFT_EAR]
           ,[mp_42_p42_y_pixel_points_of_PoseLandmark_LEFT_EAR]
           ,[mp_43_p43_x_points_of_PoseLandmark_RIGHT_EAR]
           ,[mp_44_p44_y_points_of_PoseLandmark_RIGHT_EAR]
           ,[mp_45_p45_z_points_of_PoseLandmark_RIGHT_EAR]
           ,[mp_46_p46_x_pixel_points_of_PoseLandmark_RIGHT_EAR]
           ,[mp_47_p47_y_pixel_points_of_PoseLandmark_RIGHT_EAR]
           ,[mp_48_p48_x_points_of_PoseLandmark_MOUTH_LEFT]
           ,[mp_49_p49_y_points_of_PoseLandmark_MOUTH_LEFT]
           ,[mp_50_p50_z_points_of_PoseLandmark_MOUTH_LEFT]
           ,[mp_51_p51_x_pixel_points_of_PoseLandmark_MOUTH_LEFT]
           ,[mp_52_p52_y_pixel_points_of_PoseLandmark_MOUTH_LEFT]
           ,[mp_53_p53_x_points_of_PoseLandmark_MOUTH_RIGHT]
           ,[mp_54_p54_y_points_of_PoseLandmark_MOUTH_RIGHT]
           ,[mp_55_p55_z_points_of_PoseLandmark_MOUTH_RIGHT]
           ,[mp_56_p56_x_pixel_points_of_PoseLandmark_MOUTH_RIGHT]
           ,[mp_57_p57_y_pixel_points_of_PoseLandmark_MOUTH_RIGHT]
           ,[mp_58_p58_x_points_of_PoseLandmark_LEFT_SHOULDER]
           ,[mp_59_p59_y_points_of_PoseLandmark_LEFT_SHOULDER]
           ,[mp_60_p60_z_points_of_PoseLandmark_LEFT_SHOULDER]
           ,[mp_61_p61_x_pixel_points_of_PoseLandmark_LEFT_SHOULDER]
           ,[mp_62_p62_y_pixel_points_of_PoseLandmark_LEFT_SHOULDER]
           ,[mp_63_p63_x_points_of_PoseLandmark_RIGHT_SHOULDER]
           ,[mp_64_p64_y_points_of_PoseLandmark_RIGHT_SHOULDER]
           ,[mp_65_p65_z_points_of_PoseLandmark_RIGHT_SHOULDER]
           ,[mp_66_p66_x_pixel_points_of_PoseLandmark_RIGHT_SHOULDER]
           ,[mp_67_p67_y_pixel_points_of_PoseLandmark_RIGHT_SHOULDER]
           ,[mp_68_p68_x_points_of_PoseLandmark_LEFT_ELBOW]
           ,[mp_69_p69_y_points_of_PoseLandmark_LEFT_ELBOW]
           ,[mp_70_p70_z_points_of_PoseLandmark_LEFT_ELBOW]
           ,[mp_71_p71_x_pixel_points_of_PoseLandmark_LEFT_ELBOW]
           ,[mp_72_p72_y_pixel_points_of_PoseLandmark_LEFT_ELBOW]
           ,[mp_73_p73_x_points_of_PoseLandmark_RIGHT_ELBOW]
           ,[mp_74_p74_y_points_of_PoseLandmark_RIGHT_ELBOW]
           ,[mp_75_p75_z_points_of_PoseLandmark_RIGHT_ELBOW]
           ,[mp_76_p76_x_pixel_points_of_PoseLandmark_RIGHT_ELBOW]
           ,[mp_77_p77_y_pixel_points_of_PoseLandmark_RIGHT_ELBOW]
           ,[mp_78_p78_x_points_of_PoseLandmark_LEFT_WRIST]
           ,[mp_79_p79_y_points_of_PoseLandmark_LEFT_WRIST]
           ,[mp_80_p80_z_points_of_PoseLandmark_LEFT_WRIST]
           ,[mp_81_p81_x_pixel_points_of_PoseLandmark_LEFT_WRIST]
           ,[mp_82_p82_y_pixel_points_of_PoseLandmark_LEFT_WRIST]
           ,[mp_83_p83_x_points_of_PoseLandmark_RIGHT_WRIST]
           ,[mp_84_p84_y_points_of_PoseLandmark_RIGHT_WRIST]
           ,[mp_85_p85_z_points_of_PoseLandmark_RIGHT_WRIST]
           ,[mp_86_p86_x_pixel_points_of_PoseLandmark_RIGHT_WRIST]
           ,[mp_87_p87_y_pixel_points_of_PoseLandmark_RIGHT_WRIST]
           ,[mp_88_p88_x_points_of_PoseLandmark_LEFT_PINKY]
           ,[mp_89_p89_y_points_of_PoseLandmark_LEFT_PINKY]
           ,[mp_90_p90_z_points_of_PoseLandmark_LEFT_PINKY]
           ,[mp_91_p91_x_pixel_points_of_PoseLandmark_LEFT_PINKY]
           ,[mp_92_p92_y_pixel_points_of_PoseLandmark_LEFT_PINKY]
           ,[mp_93_p93_x_points_of_PoseLandmark_RIGHT_PINKY]
           ,[mp_94_p94_y_points_of_PoseLandmark_RIGHT_PINKY]
           ,[mp_95_p95_z_points_of_PoseLandmark_RIGHT_PINKY]
           ,[mp_96_p96_x_pixel_points_of_PoseLandmark_RIGHT_PINKY]
           ,[mp_97_p97_y_pixel_points_of_PoseLandmark_RIGHT_PINKY]
           ,[mp_98_p98_x_points_of_PoseLandmark_LEFT_INDEX]
           ,[mp_99_p99_y_points_of_PoseLandmark_LEFT_INDEX]
           ,[mp_100_p100_z_points_of_PoseLandmark_LEFT_INDEX]
           ,[mp_101_p101_x_pixel_points_of_PoseLandmark_LEFT_INDEX]
           ,[mp_102_p102_y_pixel_points_of_PoseLandmark_LEFT_INDEX]
           ,[mp_103_p103_x_points_of_PoseLandmark_RIGHT_INDEX]
           ,[mp_104_p104_y_points_of_PoseLandmark_RIGHT_INDEX]
           ,[mp_105_p105_z_points_of_PoseLandmark_RIGHT_INDEX]
           ,[mp_106_p106_x_pixel_points_of_PoseLandmark_RIGHT_INDEX]
           ,[mp_107_p107_y_pixel_points_of_PoseLandmark_RIGHT_INDEX]
           ,[mp_108_p108_x_points_of_PoseLandmark_LEFT_THUMB]
           ,[mp_109_p109_y_points_of_PoseLandmark_LEFT_THUMB]
           ,[mp_110_p110_z_points_of_PoseLandmark_LEFT_THUMB]
           ,[mp_111_p111_x_pixel_points_of_PoseLandmark_LEFT_THUMB]
           ,[mp_112_p112_y_pixel_points_of_PoseLandmark_LEFT_THUMB]
           ,[mp_113_p113_x_points_of_PoseLandmark_RIGHT_THUMB]
           ,[mp_114_p114_y_points_of_PoseLandmark_RIGHT_THUMB]
           ,[mp_115_p115_z_points_of_PoseLandmark_RIGHT_THUMB]
           ,[mp_116_p116_x_pixel_points_of_PoseLandmark_RIGHT_THUMB]
           ,[mp_117_p117_y_pixel_points_of_PoseLandmark_RIGHT_THUMB]
           ,[mp_118_p118_x_points_of_PoseLandmark_LEFT_HIP]
           ,[mp_119_p119_y_points_of_PoseLandmark_LEFT_HIP]
           ,[mp_120_p120_z_points_of_PoseLandmark_LEFT_HIP]
           ,[mp_121_p121_x_pixel_points_of_PoseLandmark_LEFT_HIP]
           ,[mp_122_p122_y_pixel_points_of_PoseLandmark_LEFT_HIP]
           ,[mp_123_p123_x_points_of_PoseLandmark_RIGHT_HIP]
           ,[mp_124_p124_y_points_of_PoseLandmark_RIGHT_HIP]
           ,[mp_125_p125_z_points_of_PoseLandmark_RIGHT_HIP]
           ,[mp_126_p126_x_pixel_points_of_PoseLandmark_RIGHT_HIP]
           ,[mp_127_p127_y_pixel_points_of_PoseLandmark_RIGHT_HIP]
           ,[mp_128_p128_x_points_of_PoseLandmark_LEFT_KNEE]
           ,[mp_129_p129_y_points_of_PoseLandmark_LEFT_KNEE]
           ,[mp_130_p130_z_points_of_PoseLandmark_LEFT_KNEE]
           ,[mp_131_p131_x_pixel_points_of_PoseLandmark_LEFT_KNEE]
           ,[mp_132_p132_y_pixel_points_of_PoseLandmark_LEFT_KNEE]
           ,[mp_133_p133_x_points_of_PoseLandmark_RIGHT_KNEE]
           ,[mp_134_p134_y_points_of_PoseLandmark_RIGHT_KNEE]
           ,[mp_135_p135_z_points_of_PoseLandmark_RIGHT_KNEE]
           ,[mp_136_p136_x_pixel_points_of_PoseLandmark_RIGHT_KNEE]
           ,[mp_137_p137_y_pixel_points_of_PoseLandmark_RIGHT_KNEE]
           ,[mp_138_p138_x_points_of_PoseLandmark_LEFT_ANKLE]
           ,[mp_139_p139_y_points_of_PoseLandmark_LEFT_ANKLE]
           ,[mp_140_p140_z_points_of_PoseLandmark_LEFT_ANKLE]
           ,[mp_141_p141_x_pixel_points_of_PoseLandmark_LEFT_ANKLE]
           ,[mp_142_p142_y_pixel_points_of_PoseLandmark_LEFT_ANKLE]
           ,[mp_143_p143_x_points_of_PoseLandmark_RIGHT_ANKLE]
           ,[mp_144_p144_y_points_of_PoseLandmark_RIGHT_ANKLE]
           ,[mp_145_p145_z_points_of_PoseLandmark_RIGHT_ANKLE]
           ,[mp_146_p146_x_pixel_points_of_PoseLandmark_RIGHT_ANKLE]
           ,[mp_147_p147_y_pixel_points_of_PoseLandmark_RIGHT_ANKLE]
           ,[mp_148_p148_x_points_of_PoseLandmark_LEFT_HEEL]
           ,[mp_149_p149_y_points_of_PoseLandmark_LEFT_HEEL]
           ,[mp_150_p150_z_points_of_PoseLandmark_LEFT_HEEL]
           ,[mp_151_p151_x_pixel_points_of_PoseLandmark_LEFT_HEEL]
           ,[mp_152_p152_y_pixel_points_of_PoseLandmark_LEFT_HEEL]
           ,[mp_153_p153_x_points_of_PoseLandmark_RIGHT_HEEL]
           ,[mp_154_p154_y_points_of_PoseLandmark_RIGHT_HEEL]
           ,[mp_155_p155_z_points_of_PoseLandmark_RIGHT_HEEL]
           ,[mp_156_p156_x_pixel_points_of_PoseLandmark_RIGHT_HEEL]
           ,[mp_157_p157_y_pixel_points_of_PoseLandmark_RIGHT_HEEL]
           ,[mp_158_p158_x_points_of_PoseLandmark_LEFT_FOOT_INDEX]
           ,[mp_159_p159_y_points_of_PoseLandmark_LEFT_FOOT_INDEX]
           ,[mp_160_p160_z_points_of_PoseLandmark_LEFT_FOOT_INDEX]
           ,[mp_161_p161_x_pixel_points_of_PoseLandmark_LEFT_FOOT_INDEX]
           ,[mp_162_p162_y_pixel_points_of_PoseLandmark_LEFT_FOOT_INDEX]
           ,[mp_163_p163_x_points_of_PoseLandmark_RIGHT_FOOT_INDEX]
           ,[mp_164_p164_y_points_of_PoseLandmark_RIGHT_FOOT_INDEX]
           ,[mp_165_p165_z_points_of_PoseLandmark_RIGHT_FOOT_INDEX]
           ,[mp_166_p166_x_pixel_points_of_PoseLandmark_RIGHT_FOOT_INDEX]
           ,[mp_167_p167_y_pixel_points_of_PoseLandmark_RIGHT_FOOT_INDEX]
           ,[mp_168_h1_x_norm_HandLandmark_WRIST_right]
           ,[mp_169_h1_y_norm_HandLandmark_WRIST_right]
           ,[mp_170_h1_z_norm_HandLandmark_WRIST_right]
           ,[mp_171_h1_x_pxl_HandLandmark_WRIST_right]
           ,[mp_172_h1_y_pxl_HandLandmark_WRIST_right]
           ,[mp_173_h2_x_norm_HandLandmark_THUMB_CMC_right]
           ,[mp_174_h2_y_norm_HandLandmark_THUMB_CMC_right]
           ,[mp_175_h2_z_norm_HandLandmark_THUMB_CMC_right]
           ,[mp_176_h2_x_pxl_HandLandmark_THUMB_CMC_right]
           ,[mp_177_h2_y_pxl_HandLandmark_THUMB_CMC_right]
           ,[mp_178_h3_x_norm_HandLandmark_THUMB_MCP_right]
           ,[mp_179_h3_y_norm_HandLandmark_THUMB_MCP_right]
           ,[mp_180_h3_z_norm_HandLandmark_THUMB_MCP_right]
           ,[mp_181_h3_x_pxl_HandLandmark_THUMB_MCP_right]
           ,[mp_182_h3_y_pxl_HandLandmark_THUMB_MCP_right]
           ,[mp_183_h4_x_norm_HandLandmark_THUMB_IP_right]
           ,[mp_184_h4_y_norm_HandLandmark_THUMB_IP_right]
           ,[mp_185_h4_z_norm_HandLandmark_THUMB_IP_right]
           ,[mp_186_h4_x_pxl_HandLandmark_THUMB_IP_right]
           ,[mp_187_h4_y_pxl_HandLandmark_THUMB_IP_right]
           ,[mp_188_h5_x_norm_HandLandmark_THUMB_TIP_right]
           ,[mp_189_h5_y_norm_HandLandmark_THUMB_TIP_right]
           ,[mp_190_h5_z_norm_HandLandmark_THUMB_TIP_right]
           ,[mp_191_h5_x_pxl_HandLandmark_THUMB_TIP_right]
           ,[mp_192_h5_y_pxl_HandLandmark_THUMB_TIP_right]
           ,[mp_193_h6_x_norm_HandLandmark_INDEX_FINGER_MCP_right]
           ,[mp_194_h6_y_norm_HandLandmark_INDEX_FINGER_MCP_right]
           ,[mp_195_h6_z_norm_HandLandmark_INDEX_FINGER_MCP_right]
           ,[mp_196_h6_x_pxl_HandLandmark_INDEX_FINGER_MCP_right]
           ,[mp_197_h6_y_pxl_HandLandmark_INDEX_FINGER_MCP_right]
           ,[mp_198_h7_x_norm_HandLandmark_INDEX_FINGER_PIP_right]
           ,[mp_199_h7_y_norm_HandLandmark_INDEX_FINGER_PIP_right]
           ,[mp_200_h7_z_norm_HandLandmark_INDEX_FINGER_PIP_right]
           ,[mp_201_h7_x_pxl_HandLandmark_INDEX_FINGER_PIP_right]
           ,[mp_202_h7_y_pxl_HandLandmark_INDEX_FINGER_PIP_right]
           ,[mp_203_h8_x_norm_HandLandmark_INDEX_FINGER_DIP_right]
           ,[mp_204_h8_y_norm_HandLandmark_INDEX_FINGER_DIP_right]
           ,[mp_205_h8_z_norm_HandLandmark_INDEX_FINGER_DIP_right]
           ,[mp_206_h8_x_pxl_HandLandmark_INDEX_FINGER_DIP_right]
           ,[mp_207_h8_y_pxl_HandLandmark_INDEX_FINGER_DIP_right]
           ,[mp_208_h9_x_norm_HandLandmark_INDEX_FINGER_TIP_right]
           ,[mp_209_h9_y_norm_HandLandmark_INDEX_FINGER_TIP_right]
           ,[mp_210_h9_z_norm_HandLandmark_INDEX_FINGER_TIP_right]
           ,[mp_211_h9_x_pxl_HandLandmark_INDEX_FINGER_TIP_right]
           ,[mp_212_h9_y_pxl_HandLandmark_INDEX_FINGER_TIP_right]
           ,[mp_213_h10_x_norm_HandLandmark_MIDDLE_FINGER_MCP_right]
           ,[mp_214_h10_y_norm_HandLandmark_MIDDLE_FINGER_MCP_right]
           ,[mp_215_h10_z_norm_HandLandmark_MIDDLE_FINGER_MCP_right]
           ,[mp_216_h10_x_pxl_HandLandmark_MIDDLE_FINGER_MCP_right]
           ,[mp_217_h10_y_pxl_HandLandmark_MIDDLE_FINGER_MCP_right]
           ,[mp_218_h11_x_norm_HandLandmark_MIDDLE_FINGER_PIP_right]
           ,[mp_219_h11_y_norm_HandLandmark_MIDDLE_FINGER_PIP_right]
           ,[mp_220_h11_z_norm_HandLandmark_MIDDLE_FINGER_PIP_right]
           ,[mp_221_h11_x_pxl_HandLandmark_MIDDLE_FINGER_PIP_right]
           ,[mp_222_h11_y_pxl_HandLandmark_MIDDLE_FINGER_PIP_right]
           ,[mp_223_h12_x_norm_HandLandmark_MIDDLE_FINGER_DIP_right]
           ,[mp_224_h12_y_norm_HandLandmark_MIDDLE_FINGER_DIP_right]
           ,[mp_225_h12_z_norm_HandLandmark_MIDDLE_FINGER_DIP_right]
           ,[mp_226_h12_x_pxl_HandLandmark_MIDDLE_FINGER_DIP_right]
           ,[mp_227_h12_y_pxl_HandLandmark_MIDDLE_FINGER_DIP_right]
           ,[mp_228_h13_x_norm_HandLandmark_MIDDLE_FINGER_TIP_right]
           ,[mp_229_h13_y_norm_HandLandmark_MIDDLE_FINGER_TIP_right]
           ,[mp_230_h13_z_norm_HandLandmark_MIDDLE_FINGER_TIP_right]
           ,[mp_231_h13_x_pxl_HandLandmark_MIDDLE_FINGER_TIP_right]
           ,[mp_232_h13_y_pxl_HandLandmark_MIDDLE_FINGER_TIP_right]
           ,[mp_233_h14_x_norm_HandLandmark_RING_FINGER_MCP_right]
           ,[mp_234_h14_y_norm_HandLandmark_RING_FINGER_MCP_right]
           ,[mp_235_h14_z_norm_HandLandmark_RING_FINGER_MCP_right]
           ,[mp_236_h14_x_pxl_HandLandmark_RING_FINGER_MCP_right]
           ,[mp_237_h14_y_pxl_HandLandmark_RING_FINGER_MCP_right]
           ,[mp_238_h15_x_norm_HandLandmark_RING_FINGER_PIP_right]
           ,[mp_239_h15_y_norm_HandLandmark_RING_FINGER_PIP_right]
           ,[mp_240_h15_z_norm_HandLandmark_RING_FINGER_PIP_right]
           ,[mp_241_h15_x_pxl_HandLandmark_RING_FINGER_PIP_right]
           ,[mp_242_h15_y_pxl_HandLandmark_RING_FINGER_PIP_right]
           ,[mp_243_h16_x_norm_HandLandmark_RING_FINGER_DIP_right]
           ,[mp_244_h16_y_norm_HandLandmark_RING_FINGER_DIP_right]
           ,[mp_245_h16_z_norm_HandLandmark_RING_FINGER_DIP_right]
           ,[mp_246_h16_x_pxl_HandLandmark_RING_FINGER_DIP_right]
           ,[mp_247_h16_y_pxl_HandLandmark_RING_FINGER_DIP_right]
           ,[mp_248_h17_x_norm_HandLandmark_RING_FINGER_TIP_right]
           ,[mp_249_h17_y_norm_HandLandmark_RING_FINGER_TIP_right]
           ,[mp_250_h17_z_norm_HandLandmark_RING_FINGER_TIP_right]
           ,[mp_251_h17_x_pxl_HandLandmark_RING_FINGER_TIP_right]
           ,[mp_252_h17_y_pxl_HandLandmark_RING_FINGER_TIP_right]
           ,[mp_253_h18_x_norm_HandLandmark_PINKY_MCP_right]
           ,[mp_254_h18_y_norm_HandLandmark_PINKY_MCP_right]
           ,[mp_255_h18_z_norm_HandLandmark_PINKY_MCP_right]
           ,[mp_256_h18_x_pxl_HandLandmark_PINKY_MCP_right]
           ,[mp_257_h18_y_pxl_HandLandmark_PINKY_MCP_right]
           ,[mp_258_h19_x_norm_HandLandmark_PINKY_PIP_right]
           ,[mp_259_h19_y_norm_HandLandmark_PINKY_PIP_right]
           ,[mp_260_h19_z_norm_HandLandmark_PINKY_PIP_right]
           ,[mp_261_h19_x_pxl_HandLandmark_PINKY_PIP_right]
           ,[mp_262_h19_y_pxl_HandLandmark_PINKY_PIP_right]
           ,[mp_263_h20_x_norm_HandLandmark_PINKY_DIP_right]
           ,[mp_264_h20_y_norm_HandLandmark_PINKY_DIP_right]
           ,[mp_265_h20_z_norm_HandLandmark_PINKY_DIP_right]
           ,[mp_266_h20_x_pxl_HandLandmark_PINKY_DIP_right]
           ,[mp_267_h20_y_pxl_HandLandmark_PINKY_DIP_right]
           ,[mp_268_h21_x_norm_HandLandmark_PINKY_TIP_right]
           ,[mp_269_h21_y_norm_HandLandmark_PINKY_TIP_right]
           ,[mp_270_h21_z_norm_HandLandmark_PINKY_TIP_right]
           ,[mp_271_h21_x_pxl_HandLandmark_PINKY_TIP_right]
           ,[mp_272_h21_y_pxl_HandLandmark_PINKY_TIP_right]
           ,[mp_168_h1_x_norm_HandLandmark_WRIST_left]
           ,[mp_169_h1_y_norm_HandLandmark_WRIST_left]
           ,[mp_170_h1_z_norm_HandLandmark_WRIST_left]
           ,[mp_171_h1_x_pxl_HandLandmark_WRIST_left]
           ,[mp_172_h1_y_pxl_HandLandmark_WRIST_left]
           ,[mp_173_h2_x_norm_HandLandmark_THUMB_CMC_left]
           ,[mp_174_h2_y_norm_HandLandmark_THUMB_CMC_left]
           ,[mp_175_h2_z_norm_HandLandmark_THUMB_CMC_left]
           ,[mp_176_h2_x_pxl_HandLandmark_THUMB_CMC_left]
           ,[mp_177_h2_y_pxl_HandLandmark_THUMB_CMC_left]
           ,[mp_178_h3_x_norm_HandLandmark_THUMB_MCP_left]
           ,[mp_179_h3_y_norm_HandLandmark_THUMB_MCP_left]
           ,[mp_180_h3_z_norm_HandLandmark_THUMB_MCP_left]
           ,[mp_181_h3_x_pxl_HandLandmark_THUMB_MCP_left]
           ,[mp_182_h3_y_pxl_HandLandmark_THUMB_MCP_left]
           ,[mp_183_h4_x_norm_HandLandmark_THUMB_IP_left]
           ,[mp_184_h4_y_norm_HandLandmark_THUMB_IP_left]
           ,[mp_185_h4_z_norm_HandLandmark_THUMB_IP_left]
           ,[mp_186_h4_x_pxl_HandLandmark_THUMB_IP_left]
           ,[mp_187_h4_y_pxl_HandLandmark_THUMB_IP_left]
           ,[mp_188_h5_x_norm_HandLandmark_THUMB_TIP_left]
           ,[mp_189_h5_y_norm_HandLandmark_THUMB_TIP_left]
           ,[mp_190_h5_z_norm_HandLandmark_THUMB_TIP_left]
           ,[mp_191_h5_x_pxl_HandLandmark_THUMB_TIP_left]
           ,[mp_192_h5_y_pxl_HandLandmark_THUMB_TIP_left]
           ,[mp_193_h6_x_norm_HandLandmark_INDEX_FINGER_MCP_left]
           ,[mp_194_h6_y_norm_HandLandmark_INDEX_FINGER_MCP_left]
           ,[mp_195_h6_z_norm_HandLandmark_INDEX_FINGER_MCP_left]
           ,[mp_196_h6_x_pxl_HandLandmark_INDEX_FINGER_MCP_left]
           ,[mp_197_h6_y_pxl_HandLandmark_INDEX_FINGER_MCP_left]
           ,[mp_198_h7_x_norm_HandLandmark_INDEX_FINGER_PIP_left]
           ,[mp_199_h7_y_norm_HandLandmark_INDEX_FINGER_PIP_left]
           ,[mp_200_h7_z_norm_HandLandmark_INDEX_FINGER_PIP_left]
           ,[mp_201_h7_x_pxl_HandLandmark_INDEX_FINGER_PIP_left]
           ,[mp_202_h7_y_pxl_HandLandmark_INDEX_FINGER_PIP_left]
           ,[mp_203_h8_x_norm_HandLandmark_INDEX_FINGER_DIP_left]
           ,[mp_204_h8_y_norm_HandLandmark_INDEX_FINGER_DIP_left]
           ,[mp_205_h8_z_norm_HandLandmark_INDEX_FINGER_DIP_left]
           ,[mp_206_h8_x_pxl_HandLandmark_INDEX_FINGER_DIP_left]
           ,[mp_207_h8_y_pxl_HandLandmark_INDEX_FINGER_DIP_left]
           ,[mp_208_h9_x_norm_HandLandmark_INDEX_FINGER_TIP_left]
           ,[mp_209_h9_y_norm_HandLandmark_INDEX_FINGER_TIP_left]
           ,[mp_210_h9_z_norm_HandLandmark_INDEX_FINGER_TIP_left]
           ,[mp_211_h9_x_pxl_HandLandmark_INDEX_FINGER_TIP_left]
           ,[mp_212_h9_y_pxl_HandLandmark_INDEX_FINGER_TIP_left]
           ,[mp_213_h10_x_norm_HandLandmark_MIDDLE_FINGER_MCP_left]
           ,[mp_214_h10_y_norm_HandLandmark_MIDDLE_FINGER_MCP_left]
           ,[mp_215_h10_z_norm_HandLandmark_MIDDLE_FINGER_MCP_left]
           ,[mp_216_h10_x_pxl_HandLandmark_MIDDLE_FINGER_MCP_left]
           ,[mp_217_h10_y_pxl_HandLandmark_MIDDLE_FINGER_MCP_left]
           ,[mp_218_h11_x_norm_HandLandmark_MIDDLE_FINGER_PIP_left]
           ,[mp_219_h11_y_norm_HandLandmark_MIDDLE_FINGER_PIP_left]
           ,[mp_220_h11_z_norm_HandLandmark_MIDDLE_FINGER_PIP_left]
           ,[mp_221_h11_x_pxl_HandLandmark_MIDDLE_FINGER_PIP_left]
           ,[mp_222_h11_y_pxl_HandLandmark_MIDDLE_FINGER_PIP_left]
           ,[mp_223_h12_x_norm_HandLandmark_MIDDLE_FINGER_DIP_left]
           ,[mp_224_h12_y_norm_HandLandmark_MIDDLE_FINGER_DIP_left]
           ,[mp_225_h12_z_norm_HandLandmark_MIDDLE_FINGER_DIP_left]
           ,[mp_226_h12_x_pxl_HandLandmark_MIDDLE_FINGER_DIP_left]
           ,[mp_227_h12_y_pxl_HandLandmark_MIDDLE_FINGER_DIP_left]
           ,[mp_228_h13_x_norm_HandLandmark_MIDDLE_FINGER_TIP_left]
           ,[mp_229_h13_y_norm_HandLandmark_MIDDLE_FINGER_TIP_left]
           ,[mp_230_h13_z_norm_HandLandmark_MIDDLE_FINGER_TIP_left]
           ,[mp_231_h13_x_pxl_HandLandmark_MIDDLE_FINGER_TIP_left]
           ,[mp_232_h13_y_pxl_HandLandmark_MIDDLE_FINGER_TIP_left]
           ,[mp_233_h14_x_norm_HandLandmark_RING_FINGER_MCP_left]
           ,[mp_234_h14_y_norm_HandLandmark_RING_FINGER_MCP_left]
           ,[mp_235_h14_z_norm_HandLandmark_RING_FINGER_MCP_left]
           ,[mp_236_h14_x_pxl_HandLandmark_RING_FINGER_MCP_left]
           ,[mp_237_h14_y_pxl_HandLandmark_RING_FINGER_MCP_left]
           ,[mp_238_h15_x_norm_HandLandmark_RING_FINGER_PIP_left]
           ,[mp_239_h15_y_norm_HandLandmark_RING_FINGER_PIP_left]
           ,[mp_240_h15_z_norm_HandLandmark_RING_FINGER_PIP_left]
           ,[mp_241_h15_x_pxl_HandLandmark_RING_FINGER_PIP_left]
           ,[mp_242_h15_y_pxl_HandLandmark_RING_FINGER_PIP_left]
           ,[mp_243_h16_x_norm_HandLandmark_RING_FINGER_DIP_left]
           ,[mp_244_h16_y_norm_HandLandmark_RING_FINGER_DIP_left]
           ,[mp_245_h16_z_norm_HandLandmark_RING_FINGER_DIP_left]
           ,[mp_246_h16_x_pxl_HandLandmark_RING_FINGER_DIP_left]
           ,[mp_247_h16_y_pxl_HandLandmark_RING_FINGER_DIP_left]
           ,[mp_248_h17_x_norm_HandLandmark_RING_FINGER_TIP_left]
           ,[mp_249_h17_y_norm_HandLandmark_RING_FINGER_TIP_left]
           ,[mp_250_h17_z_norm_HandLandmark_RING_FINGER_TIP_left]
           ,[mp_251_h17_x_pxl_HandLandmark_RING_FINGER_TIP_left]
           ,[mp_252_h17_y_pxl_HandLandmark_RING_FINGER_TIP_left]
           ,[mp_253_h18_x_norm_HandLandmark_PINKY_MCP_left]
           ,[mp_254_h18_y_norm_HandLandmark_PINKY_MCP_left]
           ,[mp_255_h18_z_norm_HandLandmark_PINKY_MCP_left]
           ,[mp_256_h18_x_pxl_HandLandmark_PINKY_MCP_left]
           ,[mp_257_h18_y_pxl_HandLandmark_PINKY_MCP_left]
           ,[mp_258_h19_x_norm_HandLandmark_PINKY_PIP_left]
           ,[mp_259_h19_y_norm_HandLandmark_PINKY_PIP_left]
           ,[mp_260_h19_z_norm_HandLandmark_PINKY_PIP_left]
           ,[mp_261_h19_x_pxl_HandLandmark_PINKY_PIP_left]
           ,[mp_262_h19_y_pxl_HandLandmark_PINKY_PIP_left]
           ,[mp_263_h20_x_norm_HandLandmark_PINKY_DIP_left]
           ,[mp_264_h20_y_norm_HandLandmark_PINKY_DIP_left]
           ,[mp_265_h20_z_norm_HandLandmark_PINKY_DIP_left]
           ,[mp_266_h20_x_pxl_HandLandmark_PINKY_DIP_left]
           ,[mp_267_h20_y_pxl_HandLandmark_PINKY_DIP_left]
           ,[mp_268_h21_x_norm_HandLandmark_PINKY_TIP_left]
           ,[mp_269_h21_y_norm_HandLandmark_PINKY_TIP_left]
           ,[mp_270_h21_z_norm_HandLandmark_PINKY_TIP_left]
           ,[mp_271_h21_x_pxl_HandLandmark_PINKY_TIP_left]
           ,[mp_272_h21_y_pxl_HandLandmark_PINKY_TIP_left])
     VALUES
           (?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?)"""
        
        #print(sql)

        with open("sql.txt" ,'r') as my_file:
            sql = my_file.read()
        
        #print(sql)
        cursor.execute(sql,tuple(dataBaseList))
        cnxn.commit()
    #print(len(dataBaseList))
           

    cv2.imshow("Image",image)
    cv2.moveWindow('Image', 1400, 0)
    

    #cv2.imshow("Image",image)

    cv2.waitKey(1)