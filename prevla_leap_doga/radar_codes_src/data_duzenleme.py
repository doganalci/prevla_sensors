import pandas as pd
import numpy as np
import matplotlib as plt


data = pd.read_csv('/home/doga18/Desktop/mmwave_ti_ros/ros_driver/log/radar_data_doga.csv',sep=";")


data.columns = ["sepal_length"]
data.columns
