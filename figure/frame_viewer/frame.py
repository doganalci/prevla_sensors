import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

import matplotlib

mediaDF = pd.read_csv('radar.csv', sep=',', header=0)

media_x_points = mediaDF[mediaDF.columns[mediaDF.columns.str.contains('x_point')]].to_numpy()
media_y_points = mediaDF[mediaDF.columns[mediaDF.columns.str.contains('y_point')]].to_numpy()
media_z_points = mediaDF[mediaDF.columns[mediaDF.columns.str.contains('z_point')]].to_numpy()


kinectDF = pd.read_csv("kinect.csv",sep = ',',header=0)

#Kinect x,y,z points
kinect_x_points = kinect_data[kinect_data.columns[kinect_data.columns.str.contains('x_pos')]].to_numpy()
kinect_y_points = kinect_data[kinect_data.columns[kinect_data.columns.str.contains('y_pos')]].to_numpy()
kinect_z_points = kinect_data[kinect_data.columns[kinect_data.columns.str.contains('z_pos')]].to_numpy()

radar_data = pd.read_csv('radar.csv', sep=',', header=None,names=["rdr_experiment_no","rdr_frame_no","rdr_total_points_in_frame","rdr_point_no_in_frame","rdr_y_radar","rdr_x_radar","rdr_z_radar","rdr_vel_radar","rdr_intensity_radar","rdr_timestamp","rdr_user","rdr_date"])


x_radar = radar_data['rdr_x_radar'].to_numpy()
y_radar = radar_data['rdr_y_radar'].to_numpy()
z_radar = radar_data['rdr_z_radar'].to_numpy()


plt.get_backend()
matplotlib.use("QTAgg")

fig = plt.figure(figsize=(10,5))
media_x = fig.add_subplot(131,projection='3d')
radar_x = fig.add_subplot(132,projection='3d')
kinect_x = fig.add_subplot(133,projection='3d')


#mediapipe plot settings
#media_text=bx.text2D(0, 0, "2D Text", transform=bx.transAxes)
media_x.set_title("MediaPipe")
media_x.set_xlabel('x-axis')
media_x.set_ylabel('y-axis')
media_x.set_zlabel('z-axis')
media_x.set_xlim(0,1)
media_x.set_ylim(0,1)
media_x.set_zlim(0,1)


#radar plot settings
#radar_text=ax.text2D(0, 0, "2D Text", transform=ax.transAxes)
radar_x.set_title("Radar")
radar_x.set_ylabel('y-axis')
radar_x.set_zlabel('z-axis')
radar_x.set_xlabel('x-axis')
radar_x.set_xlim(-11,11)
radar_x.set_ylim(-11,11)
radar_x.set_zlim(-11,11)

#kinect plot settings
#kinect_text=ax.text2D(0, 0, "2D Text", transform=kinect_x.transAxes)
kinect_x.set_title("Kinect")
kinect_x.set_ylabel('y-axis')
kinect_x.set_zlabel('z-axis')
kinect_x.set_xlabel('x-axis')
kinect_x.set_xlim(0,10)
kinect_x.set_ylim(0,1)
kinect_x.set_zlim(0,1)



media_x.scatter3D(media_x_points,media_x_points,media_y_points)

radar_x.scatter3D(y_radar,x_radar,z_radar)

kinect_x.scatter3D(kinect_z_points,kinect_x_points,kinect_y_points)

plt.show()




