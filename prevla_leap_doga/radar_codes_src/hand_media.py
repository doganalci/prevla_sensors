#parametreler camera_portu - bekleme_suresi - camera_bas _cloud_bas file_mod figSave denek Imsave scale_percent  deney_no  im_operatçon buffer_cfg
#doga18@doga18:~/Desktop/hand$ python3 hand_media.py 2 0.0000000001 1 1 w 1 1 doga 50 1  1 str(cfg)

import cv2
import mediapipe
import math
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import get_test_data
import matplotlib.patches as patches
import sys
import subprocess
import datetime
import time
import csv
import os



font = cv2.FONT_HERSHEY_SIMPLEX
org = (5, 20)
fontScale = 0.5
color = (255, 0, 0)
thickness = 1
cam_port=int(sys.argv[1])
video_bas=int(sys.argv[3])
ploting=int(sys.argv[4])
file_module=sys.argv[5]
fig_save=int(sys.argv[6])
im_save=sys.argv[7]
kimlik=sys.argv[8]
scale_factor=int(sys.argv[9])
start=0
end=0
image_no=0
deney_no=int(sys.argv[10]) # 0 dı

im_op=int(sys.argv[11]) # 0 dı
rdr_cfg=sys.argv[12] # 0 dı
ff=0
#ft = open("txt.txt", file_module)
fc = open('/home/doga18/Desktop/mmwave_ti_ros/ros_driver/log/image_point_cvs.cvs', file_module)
fk = open('/home/doga18/Desktop/mmwave_ti_ros/ros_driver/log/deney_loglari.cvs', file_module)
start=datetime.datetime.now()
fps=0

def deney_log(deney_nog,now,damga,kimlik,file_module):

    datalist1=[]
    datalist1.append(deney_no)
    datalist1.append(now)
    datalist1.append(damga)
    datalist1.append(kimlik)
    datalist1.append(rdr_cfg)
    # print(datalist1)

    out2 = csv.writer(fk)
    out2.writerow( datalist1)
    fk.close()

def fun(image_no,x,y,z,delay,damga,image):
    plt.clf()
    a=""
    X = x
    Y = y
    Z = z
    ax = Axes3D(fig)
    # creating the plot
    #plot_geeks = ax.scatter(xs, ys, zs, color='green')
    plot_geeks = ax.scatter(zs, xs, -ys, color='green')
    ax.text2D(0.05, 0.95, str(damga)+'_'+kimlik, transform=ax.transAxes)
    # setting title and labels
    ax.set_title('3d VIZ')
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')
    a='/home/doga18/Desktop/mmwave_ti_ros/ros_driver/save/figure/figure_'+str(deney_no)+'_'+str(image_no)+'_'+str(damga)+'_'+kimlik+'_.png'
    plt.savefig(a,dpi=scale_factor)
    if ploting==1: plt.pause(delay) #is necessary for the plot to update for some reason

    if im_op==1:
        if fig_save==1:

            scale_percent = scale_factor  # percent of original size
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            image_text = cv2.putText(image, str(deney_no)+' '+str(image_no)+' '+str(damga)+'_'+nowe+'_'+kimlik, org, font,fontScale, color, thickness, cv2.LINE_AA)

            filename_img = '/home/doga18/Desktop/mmwave_ti_ros/ros_driver/save/image_pure/image_'+str(deney_no)+'_'+str(image_no)+'_'+str(damga)+'_'+kimlik+'_.png'
            filename_txt = '/home/doga18/Desktop/mmwave_ti_ros/ros_driver/save/image_txt/image_'+str(deney_no)+'_'+str(image_no)+'_'+str(damga)+'_'+kimlik+'_.png'
            resized_img = cv2.resize(image, dim, interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(filename_img,resized_img)
            resized_img_txt = cv2.resize(image_text, dim, interpolation = cv2.INTER_CUBIC)
            cv2.imwrite(filename_txt,resized_img_txt)
            if video_bas==1: cv2.imshow('MediaPipe Hands', resized_img_txt)






ilk=0;
if ilk ==0:
    if image_no==1 and ff==0 and 0 :
        subprocess.call(['gnome-terminal', '--', 'tail', '-f','/home/doga18/Desktop/mmwave_ti_ros/ros_driver/point_csv_file.cvs'])
        subprocess.call(['gnome-terminal', '--', 'tail', '-f','/home/doga18/Desktop/mmwave_ti_ros/ros_driver/connet_csv_file.cvs'])
        subprocess.call(['gnome-terminal', '--', 'tail', '-f','/home/doga18/Desktop/mmwave_ti_ros/ros_driver/deney_loglari.cvs'])
        ff+=1
    #sira_al('/home/doga18/Desktop/mmwave_ti_ros/ros_driver/deney_loglari.cvs')
    deney_no+=1
    print("deney logu işleniyor")
    deney_log(deney_no,time.ctime() ,time.time(),kimlik,file_module)
    print("deney logundan çıkılıyor")
    ilk=1

print('sistem başlatılıyor 1 saniye hazırlanın')
time.sleep(1)
# For static images:
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
#if sys.argv[0+1] is None:    cam_port=0
#else:cam_port=int(sys.argv[1])

cap = cv2.VideoCapture(0)
fig = plt.figure(dpi=scale_factor)
hand_flag=False

with handsModule.Hands(
    max_num_hands=1, # default 2
    min_detection_confidence=0.7,
    min_tracking_confidence=0.8) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Bos framei gec.")
      continue

    image.flags.writeable = True
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    imageHeight, imageWidth, _ = image.shape
    say=0
    N = 21
    x= np.zeros(N)
    y = np.zeros(N)
    z = np.zeros(N)

    x_d= np.zeros(N)
    y_d = np.zeros(N)
    z_d = np.zeros(N)
    p=0

    if results.multi_hand_landmarks:
        damga=time.time()
        nowe= time.ctime()
        hand_flag=True
        for handLandmarks in results.multi_hand_landmarks:
            drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)
            fs=    handsModule.HAND_CONNECTIONS
            l1 = list(fs)
            for item,point in enumerate(handsModule.HandLandmark):
                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
                if pixelCoordinatesLandmark ==None: hand_flag=False
                if 1==1 and hand_flag==True:
                    x[item]=normalizedLandmark.x
                    y[item]=normalizedLandmark.y
                    z[item]=normalizedLandmark.z
                    x_d[item]=pixelCoordinatesLandmark[0]
                    y_d[item]=pixelCoordinatesLandmark[1]
                    p+=1
                hand_flag=True

                if 1==0:
                    print(handsModule.HAND_CONNECTIONS)
                    print(len(handsModule.HAND_CONNECTIONS))


                    fs=    handsModule.HAND_CONNECTIONS
                    l1 = list(fs)
                    print(l1)
                    for i in range (21):
                        for t in range (2):
                            print(l1[i][t])


                    exit(9);
                    for x in handsModule.HAND_CONNECTIONS:
                        print(x)
                    d = dict(handsModule.HAND_CONNECTIONS)
                    print('The frozen set is:', d[0])

                    print(len(handsModule.HAND_CONNECTIONS))
                    exit(34)

                    print('item',item)
                    print();print('point',point);print();
                    print('p:::',p)
                    print(point)
                    print(pixelCoordinatesLandmark)
                    print(normalizedLandmark)
                #print(point)
#            if 1==1:
            #for i in range(0,21,1):

                datalist=[]
                datalist.append(deney_no)
                datalist.append(image_no)





                datalist.append(item)
                datalist.append(x[item])
                datalist.append(y[item])
                datalist.append(z[item])
                datalist.append(x_d[item])
                datalist.append(y_d[item])
                datalist.append(item)
                #datalist.append(l1[item])
                datalist.append(point)
                datalist.append(p)
                datalist.append(damga)
                datalist.append(nowe)
                datalist.append(kimlik)
                out = csv.writer(fc)
                out.writerow( datalist)
                #print(datalist)
                #print('len:',len(datalist))

##################### if sonu
                    #print('x',x);print('y',y);print('z',z);print('x_d',x_d);print('x_y',y_d);print('damga:',damga);print('no',no);

            p=0
            #d=damga%10000000
            image_no+=1
            if ploting==1 and hand_flag:
                xs = x
                ys = y
                zs = x
                delay=float(sys.argv[2])
                fun(image_no,xs,ys,zs,delay,damga,image)
                #resized_img = cv2.resize(image, dim, interpolation = cv2.INTER_CUBIC)
#                cv2.imshow('MediaPipe Hands', image_text)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
if ploting==1: cap.release()
