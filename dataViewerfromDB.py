import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

import matplotlib
import sys
import pandas as pd
import pyodbc
exp = int(sys.argv[1]) #Take exp no via terminal argument

#Connection with database
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=193.35.200.106;DATABASE=Prevla;UID=SA;PWD=hP337^9nArG&;TrustServerCertificate=Yes')

#plt
plt.get_backend()
matplotlib.use("QTAgg")


################################################
## Taking log from database
cursor = cnxn.cursor()

""" log_sql_query = "SELECT * FROM Data_Logs WHERE deney_no = ?;" #"SELECT * FROM Data_Logs" #

log_df = pd.read_sql(log_sql_query, cnxn,params=[exp])

if(log_df.empty):
    print("Experiment not found")
    exit(1) """


# Read log.csv file
log_df = pd.read_csv('/home/inosens/Desktop/data_collection/sensor_data/log.csv', sep=',',header=None,names=["ID","experiment_no","subject","movement","part","total_part","rep","total_rep","duration","start_timestamp","end_timestamp","tarih"])


#Filter with experiment no
log_df = log_df.loc[(log_df["experiment_no"] == exp)].reset_index()


## Save start and end timestamp of experiment
startTime = float(log_df.loc[0,"start_timestamp"])
endTime = float(log_df.loc[log_df.index[-1],"end_timestamp"])
duration = endTime-startTime
params = (startTime,endTime)

print("starTime:",startTime)
print("endTime:",endTime)

################################################

#Taking mediapipe data from database
mediapipe_sql_query = "SELECT * FROM MediapipeDatas WHERE mp_1_p1_mp_h_p_timestamp BETWEEN ? AND ?;"
mediaDF = pd.read_sql(mediapipe_sql_query, cnxn,params=params)


#Mediapipe frame ratio 
mediapipeRatio = (30*duration) / len(mediaDF)
    
#Mediapipe x,y,z points
x_points = mediaDF[mediaDF.columns[mediaDF.columns.str.contains('x_point')]].to_numpy()
y_points = mediaDF[mediaDF.columns[mediaDF.columns.str.contains('y_point')]].to_numpy()
z_points = mediaDF[mediaDF.columns[mediaDF.columns.str.contains('z_point')]].to_numpy()

mediaTimeStamps = mediaDF["mp_1_p1_mp_h_p_timestamp"].to_numpy()


#Taking radar data from database
#radar_sql_query = "SELECT * FROM RadarDatas WHERE rdr_timestamp BETWEEN ? AND ?;"
#radar_data = pd.read_sql(radar_sql_query, cnxn,params=params)
radar_data = pd.read_csv('/home/inosens/Desktop/data_collection/sensor_data/radar_data_doga.csv', sep=',', header=None,names=["rdr_experiment_no","rdr_frame_no","rdr_total_points_in_frame","rdr_point_no_in_frame","rdr_y_radar","rdr_x_radar","rdr_z_radar","rdr_vel_radar","rdr_intensity_radar","rdr_timestamp","rdr_user","rdr_date"])
radar_data = radar_data.loc[(radar_data['rdr_timestamp'] >= float(startTime)) & (radar_data['rdr_timestamp'] <= float(endTime))].reset_index(drop=True)



x_radar = []
y_radar = []
z_radar = []

#Radar frame ratio
radarRatio = (30*duration)/len(range(radar_data.loc[0,"rdr_frame_no"],radar_data.loc[radar_data.index[-1],"rdr_frame_no"]))


#Taking kinect data from database
kinect_sql_query = "SELECT * FROM KinectDatas WHERE kinect_timestamp4_real BETWEEN ? AND ?;"
kinect_data = pd.read_sql(kinect_sql_query,cnxn,params=params)


#Kinect x,y,z points
kinect_x_points = kinect_data[kinect_data.columns[kinect_data.columns.str.contains('x_pos')]].to_numpy()
kinect_y_points = kinect_data[kinect_data.columns[kinect_data.columns.str.contains('y_pos')]].to_numpy()
kinect_z_points = kinect_data[kinect_data.columns[kinect_data.columns.str.contains('z_pos')]].to_numpy()


#Kinect point normalisation
kinect_x_points = (kinect_x_points + 1)/2
kinect_y_points = (kinect_y_points + 1)/2
#kinect_z_points = (kinect_z_points + 1)/2



if(kinect_data.empty):
    kinectRatio = 0
else:
    #Kinect Frame Ratio
    kinectRatio = (30*duration)/len(kinect_data)


#First frame of radar data 
firstFrame = radar_data.loc[0,"rdr_frame_no"]


#plt settings
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(131,projection='3d')
bx = fig.add_subplot(132,projection='3d')
kinect_x = fig.add_subplot(133,projection='3d')

sc = ax.scatter([],[],[], c='darkblue', alpha=0.5)
bc = bx.scatter([],[],[], c='green', )
kinect_scatter = kinect_x.scatter([],[],[], c='red')

#depth for mediapipe
ert = np.empty(33)
ert.fill(0.5)



#Total frames of sensors
print("total mediapipe frame:",len(mediaDF))
print("total radar frame:",len(range(radar_data.loc[0,"rdr_frame_no"],radar_data.loc[radar_data.index[-1],"rdr_frame_no"])))
print("total kinect frame",len(kinect_data))


#plot function
def update(i):
    
    label = radar_data[(radar_data['rdr_frame_no']==int(i//radarRatio) + firstFrame) ].reset_index()
    
    x_radar = label['rdr_x_radar'].to_numpy()
    y_radar = label['rdr_y_radar'].to_numpy()
    z_radar = label['rdr_z_radar'].to_numpy()

    #x_radar.fill(0)
    #print(x_radar)
    #y_radar.fill(0)
    #z_radar.fill(0)
    print(int(i//radarRatio))
    print("x_mean",x_radar.mean())
    print("y_mean",y_radar.mean())
    print("z_mean",z_radar.mean())
    print()

    #radar data normalisation
    #x_radar = (x_radar + 11)/22
    #y_radar = (y_radar + 11)/22
    #z_radar = (z_radar +11) /22
    
    #Timestamp text (kinect will be added) 
    #TODO kinect
    media_text.set_text(str(mediaTimeStamps[int(i//mediapipeRatio)]))
    radar_text.set_text(str(label.loc[0,"rdr_timestamp"]))

    #plotting point
    sc._offsets3d = (z_radar,x_radar,y_radar)
    bc._offsets3d = (ert,x_points[int(i//mediapipeRatio)],np.negative(y_points[int(i//mediapipeRatio)]))

    if(not (kinect_data.empty)):
        kinect_scatter._offsets3d = (kinect_z_points[int(i//kinectRatio)],kinect_y_points[int(i//kinectRatio)],kinect_x_points[int(i//kinectRatio)])
    


#interval variable
x = (duration / 30)*1000


#mediapipe plot settings
media_text=bx.text2D(0, 0, "2D Text", transform=bx.transAxes)
bx.set_title("MediaPipe")
bx.set_xlabel('x-axis')
bx.set_ylabel('y-axis')
bx.set_zlabel('z-axis')
bx.set_xlim(0,1)
bx.set_ylim(0,1)
bx.set_zlim(-1,0)


#radar plot settings
radar_text=ax.text2D(0, 0, "2D Text", transform=ax.transAxes)
ax.set_title("Radar")
ax.set_ylabel('y-axis')
ax.set_zlabel('z-axis')
ax.set_xlabel('x-axis')
ax.set_xlim(-5,5)
ax.set_ylim(-11,11)
ax.set_zlim(-11,11)

#kinect plot settings
kinect_text=ax.text2D(0, 0, "2D Text", transform=kinect_x.transAxes)
kinect_x.set_title("Kinect")
kinect_x.set_ylabel('y-axis')
kinect_x.set_zlabel('z-axis')
kinect_x.set_xlabel('x-axis')
kinect_x.set_xlim(0,10)
kinect_x.set_ylim(0,1)
kinect_x.set_zlim(0,1)

#animation function
ani = matplotlib.animation.FuncAnimation(fig, update, frames=range(0,int(duration*30)),interval=1 ,repeat=True)
plt.show()


#Saving as gif
f = "/home/inosens/Desktop/data_collection/figure/gifs/deney_"+str(exp)+".gif"
writergif = animation.PillowWriter(fps=30)

ani.save(f,writer = writergif)
print("GIF SAVED")