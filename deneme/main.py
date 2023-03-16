import tkinter as tk
import os
import sys
import subprocess
import time
#import ntplib
import psutil
import csv

#Disable tf warning and info
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#print(os.environ.get("PATH"))

proclist = []
procPid = -1000

def run_selected_programs():
    #selected_programs = [program for program, selected in zip(programs, program_vars) if selected.get()]
    
    logText = ""
    logstrvar = tk.StringVar(root,value=logText)
    logLabel = tk.Label(root,textvariable=logstrvar)
    logLabel.grid(row=15,column=1)
    logLabel.update()
    #root.update()
    
    
    #logLabel.update()
    
    global proclist, procPid

    for proc in proclist:
        parent = psutil.Process(proc.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()

    #print(mediapipe_var.get())
    
    #################################
    #Taking expr_no from /home/inosens/Desktop/data_collection/sensor_data/log.csv
    with open('/home/inosens/Desktop/data_collection/sensor_data/log.csv') as csv_file:
    
        csv_reader = csv.reader(csv_file, delimiter=',')
        dataList = list(csv_reader)

        if(dataList):
            expr_no = int(dataList[-1][1]) + 1
            
        else:
            expr_no = 1    
    #################################
    

    #Mediapipe
    if(mediapipe_var.get()):
	
        logText += "\nMediapipe is running."
        logstrvar.set(logText)
        logLabel.update()
        #print("Mediapipe is running...",end="",flush=True)

        #Data size before the run
        mediaLogFile1 = os.path.getsize('/home/inosens/Desktop/data_collection/sensor_data/burak.csv')

        #Run command
        media = "cd media && conda run -n mp python mypose.py 0 0.0000001 1 1 w 1 1 burak 1 "+ str(expr_no)+" 0 0"
        
        #Run mediapipe
        proc = subprocess.Popen(media,shell=True)
        
        #Start time of proc
        mediaStart = time.time()

        mediaLogFile2=mediaLogFile1

        #
        while not (mediaLogFile2>mediaLogFile1):
            
            
            #If current data is not bigger than before, restart the proc
            if(time.time()-mediaStart > 20):
                logText = logText + "\nMediaPipe Restarting."
                logstrvar.set(logText)
                logLabel.update()
                print("\nMediaPipe Restarting.")
                
                #Killing Proc
                parent = psutil.Process(proc.pid)
                
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()

                #Restart Proc
                proc = subprocess.Popen(media,shell=True)
                #Start time of proc
                mediaStart = time.time()

            
            
            time.sleep(0.5)
            logText = logText + "."
            logstrvar.set(logText)
            logLabel.update()
            #print(".",end="",flush=True)

            #Size of current data
            mediaLogFile2 = os.path.getsize('/home/inosens/Desktop/data_collection/sensor_data/burak.csv')


        #Add proc to proclist
        proclist.append(proc)
        logText = logText + "\nMediapipe is started"
        logstrvar.set(logText)
        logLabel.update()
        #print("\nMediapipe is started")

        

    if(kinect_var.get()):
        proc = subprocess.Popen("cd && ./Desktop/burak-kinect2/libfreenect2/build/bin/Protonect",shell=True)
        proclist.append(proc)
        #print(proc.pid)
        #procPid = proc.pid
        
        #

    if(radar_var.get()):

        
        logText += "\nRadar is running."
        logstrvar.set(logText)
        logLabel.update()
        #print("Radar is running...",end="",flush=True)

        #Data size before the run
        radarLogFile1 = os.path.getsize('/home/inosens/Desktop/data_collection/sensor_data/radar_data_doga.csv')

        #Run radar
        proc = subprocess.Popen("cd && cd /home/inosens/Desktop/prevla_sensors/mmwave_ti_ros/ros_driver && source devel/setup.bash && roslaunch ti_mmwave_rospkg 1843_multi_3d_0.launch",shell=True,executable="/bin/bash")
        
        
        #Start time of proc
        radarStart = time.time()

        radarLogFile2=radarLogFile1

        #
        while not (radarLogFile2>radarLogFile1):
            
            
            #If current data is not bigger than before, restart the proc
            if(time.time()-radarStart > 20):
                
                logText = logText + "\nRadar is Restarting."
                logstrvar.set(logText)
                logLabel.update()
                
                #Killing Proc
                parent = psutil.Process(proc.pid)
                
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()

                #Restart Proc
                proc = subprocess.Popen("cd && cd /home/inosens/Desktop/prevla_sensors/mmwave_ti_ros/ros_driver && source devel/setup.bash && roslaunch ti_mmwave_rospkg 1843_multi_3d_0.launch",shell=True,executable="/bin/bash")
                #Start time of proc
                radarStart = time.time()

            
            
            time.sleep(0.5)
            logText = logText + "."
            logstrvar.set(logText)
            logLabel.update()

            #Size of current data
            radarLogFile2 = os.path.getsize('/home/inosens/Desktop/data_collection/sensor_data/radar_data_doga.csv')


        #Add proc to proclist
        proclist.append(proc)
        logText = logText + "\nRadar is started"
        logstrvar.set(logText)
        logLabel.update()
        
        
        
        proclist.append(proc)
        #print(proc.pid)

    if(leap_var.get()):
        proc = subprocess.Popen("cd  && cd /home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws && source devel/setup.bash &&  roslaunch leap_motion visualization.launch",shell=True,executable="/bin/bash")
        proclist.append(proc)
        #print(proc.pid)

    
    #proc = subprocess.Popen("python3 media/mypose.py 0 0.0000001 1 1 w 1 1 burak 1 0 0 0",shell=True)
    
    

    

    #proc = subprocess.Popen(["python3","2.py"])

    row = raw_var.get() and radar_var.get()
    
    print(row)

    proc = subprocess.Popen(["python3", "2.py" ,str(int(row))])
    proclist.append(proc)


def restart_application():
    # Uygulamayı yeniden başlatmak için burada gerekli kodlar yazılabilir.
    #print("Uygulama Yeniden Başlatılıyor...")
    for proc in proclist:
        parent = psutil.Process(proc.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    
    python = sys.executable
    os.execl(python, python, * sys.argv)

def exit_program():
    
    global procPid

    for proc in proclist:
        parent = psutil.Process(proc.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    
    root.destroy()
    #print("Exit")
    exit()

def run_app():
    global programs, program_vars, root,programList,radar_var,kinect_var,leap_var,mediapipe_var,raw_var

  

    time.sleep(1)
    root = tk.Tk()
    root.title("Program Seçici")
    root.geometry('600x1000+0+0')

    #root.attributes('-fullscreen',True)
    root.grid_anchor(anchor="n")
    #root.geometry(root.winfo_screenwidth(),root.winfo_screenheight())

    label = tk.Label(root, font=("Calibri","80"),text="Choose:")
    label.grid(row=0,column=1)

    programs = ["Radar","Kinect", "Mediapipe", "LeapMoniton"]
    program_vars = [tk.BooleanVar() for program in programs]
    
    """  x = 3
    for i, (program, program_var) in enumerate(zip(programs, program_vars)):
        tk.Checkbutton(root, text=program, variable=program_var,font=("Calibri","64")).grid(row=x,column=1,sticky="w")
        x +=1 """

    
    """ programList = [tk.BooleanVar() for program in range(len(programs))]
    
    for i in range(len(programs)):
        tk.Checkbutton(root,text=programs[i],variable=programList[i],font=("Calibri","64")).grid(row=i+3,column=1,sticky="w") """


    radar_var = tk.BooleanVar()
    leap_var = tk.BooleanVar()
    mediapipe_var = tk.BooleanVar()
    kinect_var = tk.BooleanVar()
    raw_var = tk.BooleanVar()

    radar_check = tk.Checkbutton(root,text="Radar",variable=radar_var,font=("Calibri","50"))
    radar_check.grid(row=3,column=1,sticky="w")

    raw_check = tk.Checkbutton(root,text="Row",variable=raw_var,font=("Calibri","20"))
    raw_check.grid(row=3,column=2,sticky="w")

    kinect_check = tk.Checkbutton(root,text="Kinect",variable=kinect_var,font=("Calibri","50"))
    kinect_check.grid(row=4,column=1,sticky="w")

    mediapipe_check = tk.Checkbutton(root,text="Mediapipe",variable=mediapipe_var,font=("Calibri","50"))
    mediapipe_check.grid(row=5,column=1,sticky="w")

    leap_check = tk.Checkbutton(root,text="LeapMotion",variable=leap_var,font=("Calibri","50"))
    leap_check.grid(row=6,column=1,sticky="w")

    

    
    
    run_button = tk.Button(root, text="RUN",width=12,height=1,font=("Calibri","24"),command=run_selected_programs)
    run_button.grid(row=10,column=1)
    
    

    restart_button = tk.Button(root, width=12,height=1,font=("Calibri","24"),text="Restart", command=restart_application)
    restart_button.grid(row=11,column=1)

    quit_button = tk.Button(root,width=12,height=1,font=("Calibri","24"), text="Exit", command=exit_program)
    quit_button.grid(row=14,column=1)

    

    root.mainloop()

run_app()
