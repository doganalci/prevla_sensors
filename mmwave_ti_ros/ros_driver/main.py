import tkinter as tk
import os
import sys
import subprocess
import time

#print(os.environ.get("PATH"))

proclist = []
procPid = -1000

def run_selected_programs():
    #selected_programs = [program for program, selected in zip(programs, program_vars) if selected.get()]
    # Burada seçilen programların kodları yazılabilir.
    
    global proclist, procPid

    for proc in proclist:
        proc.kill()

    print(mediapipe_var.get())
    
        
    
    
    if(mediapipe_var.get()):
        proc = subprocess.Popen("cd media && python3 mypose.py 0 0.0000001 1 1 w 1 1 burak 1 0 0 0",shell=True)
        proclist.append(proc)
        procPid = proc.pid

        print(proc.pid)

    if(kinect_var.get()):
        proc = subprocess.Popen("cd && ./Desktop/burak-kinect2/libfreenect2/build/bin/Protonect",shell=True)
        proclist.append(proc)
        print(proc.pid)
        #procPid = proc.pid
        
        #

    if(radar_var.get()):
        proc = subprocess.Popen("cd devel",shell=True)
        proclist.append(proc)
        print(proc.pid)

    
    #proc = subprocess.Popen("python3 media/mypose.py 0 0.0000001 1 1 w 1 1 burak 1 0 0 0",shell=True)
    
    

    

    #proc = subprocess.Popen(["python3","2.py"])
    

    proc = subprocess.Popen(["python3", "2.py"])
    proclist.append(proc)

    print(os.getpgid(proc.pid))
    
    subprocess.Popen("gnome-terminal")
    #print(proc.pid)
    
    #print("Çalıştırılan Programlar:", selected_programs)

def restart_application():
    # Uygulamayı yeniden başlatmak için burada gerekli kodlar yazılabilir.
    print("Uygulama Yeniden Başlatılıyor...")
    if(proclist):
        for proc in proclist:
            proc.kill()
        print("hey")

    if procPid > 0:
        command = "kill -9 " + str(procPid+1)
        subprocess.Popen(command,shell=True)
        procPid = -1000
    
    python = sys.executable
    os.execl(python, python, * sys.argv)

def exit_program():
    
    global procPid

    for proc in proclist:
        proc.kill()

    if procPid > 0:
        command = "kill -9 " + str(procPid+1)
        subprocess.Popen(command,shell=True)
        procPid = -1000
    
    root.destroy()
    print("Exit")
    exit()

def run_app():
    global programs, program_vars, root,programList,radar_var,kinect_var,leap_var,mediapipe_var

  

    time.sleep(1)
    root = tk.Tk()
    root.title("Program Seçici")

    #root.attributes('-fullscreen',True)
    root.grid_anchor(anchor="n")
    #root.geometry(root.winfo_screenwidth(),root.winfo_screenheight())

    label = tk.Label(root, font=("Calibri","100"),text="Choose:")
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

    radar_check = tk.Checkbutton(root,text="Radar",variable=radar_var,font=("Calibri","64"))
    radar_check.grid(row=3,column=1,sticky="w")

    kinect_check = tk.Checkbutton(root,text="Kinect",variable=kinect_var,font=("Calibri","64"))
    kinect_check.grid(row=4,column=1,sticky="w")

    mediapipe_check = tk.Checkbutton(root,text="Mediapipe",variable=mediapipe_var,font=("Calibri","64"))
    mediapipe_check.grid(row=5,column=1,sticky="w")

    leap_check = tk.Checkbutton(root,text="LeapMonition",variable=leap_var,font=("Calibri","64"))
    leap_check.grid(row=6,column=1,sticky="w")

    

    
    
    run_button = tk.Button(root, text="Programı Çalıştır",width=15,height=2,font=("Calibri","32"),command=run_selected_programs)
    run_button.grid(row=10,column=1)
    
    

    restart_button = tk.Button(root, width=15,height=2,font=("Calibri","32"),text="Yeniden Başlat", command=restart_application)
    restart_button.grid(row=11,column=1)

    quit_button = tk.Button(root,width=15,height=2,font=("Calibri","32"), text="Çıkış", command=exit_program)
    quit_button.grid(row=14,column=1)

    

    root.mainloop()

run_app()
