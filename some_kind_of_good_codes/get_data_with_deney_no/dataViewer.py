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

log_sql_query = "SELECT * FROM Data_Logs WHERE deney_no = ?;" #"SELECT * FROM Data_Logs" #

log_df = pd.read_sql(log_sql_query, cnxn,params=[exp])

if(log_df.empty):
    print("Experiment not found")
    exit(1)





## Save start and end timestamp of experiment
startTime = float(log_df.loc[0,"startTimestamp_current_part"])
endTime = float(log_df.loc[log_df.index[-1],"endTimestamp_current_part"])
duration = endTime-startTime
params = (startTime,endTime)

print("starTime:",startTime , " type",type(startTime))
print("endTime:",endTime)

################################################

#Taking mediapipe data from database
mediapipe_sql_query = "SELECT * FROM MediapipeDatas WHERE mp_1_p1_mp_h_p_timestamp BETWEEN ? AND ?;"
mediaDF = pd.read_sql(mediapipe_sql_query, cnxn,params=params)

if(not (mediaDF.empty)):

    path = str("mediapipe" + str(exp) + ".csv" )
    mediaDF.to_csv(path,index=False)
else:
    print("There in no mediapipe data")


#Taking radar data from database
radar_sql_query = "SELECT * FROM RadarDatas WHERE rdr_timestamp BETWEEN ? AND ?;"
radar_data = pd.read_sql(radar_sql_query, cnxn,params=params)
#print(radar_data)

if(not(radar_data.empty)):
    path = str("radar" + str(exp) + ".csv" )
    radar_data.to_csv(path,index=False)
else:
    print("There is no radar data")
   


#Taking kinect data from database
kinect_sql_query = "SELECT * FROM KinectDatas WHERE kinect_timestamp4_real BETWEEN ? AND ?;"
kinect_data = pd.read_sql(kinect_sql_query,cnxn,params=params)


if(not(kinect_data.empty)):
    path = "kinect" + str(exp) + ".csv" 
    kinect_data.to_csv(path,index=False)
    
else:
    print("There is no kinect data")



