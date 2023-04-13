#python3 config_excel.py 1 
#argummman config nodur

#girilen argumandaki conf dosyasını drivedan ceker gerekli işlemleri yaparak gerekli yere kaydeder
#kullanıcıya açıklama dosya bilgisini çıktı olarak verebilir.



import pandas as pd
import sys
import math
import numpy as np

def find_last(yy,conf_no):
	aciklama='';name='';
	val=yy.iloc[0:150,conf_no]
	df = val.replace(np.nan, '', regex=True)
	for i,item in enumerate(df):
		if i==1:aciklama=item
		if i==2:name=item
		#print(type(item),"index is",i)
		if item=='':
				break
	return i,aciklama,name

def get_config_from_drive(path,id,sheet_id,sheet_name):
	path='';id='';
	sheet_id = "1rgDXUd2MF09pKZw3l5f3DgwmLn_lf0AZuhibcorhaCk"
	sheet_name = "conf"
	url = f"https://docs.google.com/spreadsheets/d/1rgDXUd2MF09pKZw3l5f3DgwmLn_lf0AZuhibcorhaCk/gviz/tq?tqx=out:csv&sheet=conf"

	yy=pd.read_csv(url)
	return yy

path='';id='';sheet_id='';sheet_name='';
yy=get_config_from_drive(path,id,sheet_id,sheet_name);
shifter=3
conf_no=shifter+int(sys.argv[1])

val=yy.iloc[0:500,conf_no]
lister=val.values.tolist()
last=find_last(yy,conf_no)
lister=lister[3:last[0]]

with open ("/home/inosens/Desktop/prevla_sensors/mmwave_ti_ros/ros_driver/src/ti_mmwave_rospkg/cfg/1843_3d.cfg","w") as f:
	for s in lister:
		f.write(str(s) +"\n" )

print("Configuration is success")
print("Aciklama   :: ",last[1])    # config hakkında bilgi basılabilir
print("dosya ismi :: ",last[2])

#https://docs.google.com/spreadsheets/d/1rgDXUd2MF09pKZw3l5f3DgwmLn_lf0AZuhibcorhaCk/edit?usp=sharing
