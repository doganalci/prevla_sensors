import tkinter as tk

import time
import csv
import beepy

def on_start_button_click():
    
    Font_tuple = ("Times Roman", 100, "bold")
    time_font = ("Times Roman", 50, "bold")

    movement = str(movement_var.get())
    repetitions = int(repetitions_entry.get())
    duration = float(duration_entry.get())
    delay = float(delay_entry.get())
    new = tk.Toplevel()
    new.grid_anchor(anchor="center")

    if(repetitions <= 0 and delay <= 0):
        return

    with open('out.csv') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        dataList = list(csv_reader)

        if(dataList):
            id = int(dataList[-1][0]) + 1
            expr_no = int(dataList[-1][1]) + 1
        else:
            expr_no = 1
            id = 0
    
    lab = tk.Label(new)

    lab.config(text = "Wait",font=Font_tuple)
    lab.grid()
    new.update()
    s = movement + " " + str(repetitions) + " times"
    
    data = []

    total_Label = tk.Label(new,text="Total Time: 0.00",font=time_font)
    total_Label.grid()

    """ for i in range(repetitions):
        
        time.sleep(1.5)
        lab.config(text = "START", width = "100",height="100",font=Font_tuple)
        lab.pack()
        new.update()
        beepy.beep(1)
        start = time.time()
        time.sleep(duration)
        lab.config(text = "END", width = "100",height="100",font=Font_tuple)
        lab.pack()
        new.update()
        beepy.beep(1)
        row = []
        row.append(expr_no)
        row.append("burak")
        row.append(movement)
        row.append(i+1)
        row.append(repetitions)
        row.append(duration)
        row.append(start)
        row.append(start + duration)
        data.append(row) """
    
    for i in range(repetitions):
        time.sleep(delay)
        lab.config(text = "START",font=Font_tuple)
        #lab.grid()
        new.update()
        beepy.beep(1)

        totalStart = time.time()
        

        
        for j in range(len(partOfMovement)):
        
            start = time.time()
            while time.time() - start < partOfMovement[j]:
                ##############################################
                clock = partOfMovement[j] -(time.time()-start)
                totalTime = (time.time() - totalStart)
                
                ##############################################
                clockText = "Part " + str(j+1) + ": " +  "{:.2f}".format(clock)
                lab.config(text = clockText , font=Font_tuple)
                lab.update()
                ##############################################

                ##############################################
                
                totalTimeText = "Total Time: " + "{:.2f}".format(totalTime)
                total_Label.config(text=totalTimeText)
                total_Label.update()
                ##############################################

            new.update()
            #time.sleep(duration)
            lab.config(text = "END",font=Font_tuple)
            new.update()

            bug = time.time()
            beepy.beep(1)
            

            

            row = []
            row.append(id)
            row.append(expr_no)
            row.append("burak")
            row.append(movement)
            row.append(j+1)
            row.append(i+1)
            row.append(repetitions)
            row.append(partOfMovement[j])
            row.append(start)
            row.append(start + partOfMovement[j])
            data.append(row)
            
            id += 1
            bug = time.time()-bug
            totalStart +=bug + 0.02
    
    total_Label.destroy()
    with open("out.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    lab.config(text = "FINISH",font=Font_tuple)
    
    new.update()
    time.sleep(1.5)
    
    new.destroy()


def rep_plus_button():
    rep = int(repetitions_entry.get()) + 1
    repetitions_entry.delete(0,"end")
    repetitions_entry.insert(0,rep)

def rep_minus_button():
    rep = int(repetitions_entry.get()) - 1
    if(rep <=0 ):
        return
    repetitions_entry.delete(0,"end")
    repetitions_entry.insert(0,rep)

def duration_plus_button():
    du = float(duration_entry.get()) + 0.1
    duration_entry.delete(0,"end")
    duration_entry.insert(0,"{:.1f}".format(du))

def duration_minus_button():

    du = float(duration_entry.get()) - 0.1
    if(du <=0 ):
        return
    duration_entry.delete(0,"end")
    duration_entry.insert(0,"{:.1f}".format(du))

def details():

    def details_entry():
       
        for i in entryBox:
            i.destroy()
        
        for i in labels:
            i.destroy()

        entryBox.clear()
        labels.clear()

        for i in range(int(movement_number_entry.get())):
            labels.append(tk.Label(detail,text="Time" + str(i+1)))
            labels[i].grid(row=i+3,column=0,sticky="w")
            
            entryBox.append(tk.Entry(detail))
            entryBox[i].insert(0,0)
            entryBox[i].grid(row=i+3,column=1,sticky="")
        
    def save():
        partOfMovement.clear()
        for i in entryBox:
            partOfMovement.append(float(i.get()))

        if sum(partOfMovement) != float(duration_entry.get()):
            partOfMovement.clear()
            tk.Label(detail,text="Sum of parts is not \nsame as duration",fg="red").grid(row=1,column=2)
            
            return
        
        detail.destroy()
        
        
    entryBox  = []
    labels  = [] 
    detail = tk.Toplevel()
    detail.grid_anchor(anchor="n")
    detail.title("Details")

    movement_number_label = tk.Label(detail, text = "Number of movement:")
    movement_number_label.grid(row=0,column=1,padx=5,pady=5)

    movement_number_entry = tk.Entry(detail)
    movement_number_entry.insert(0,str(0))
    movement_number_entry.grid(row=1,column=1)

    details_button = tk.Button(detail, text="Ok", command=details_entry)
    details_button.grid(row=2,column=1)

    save_button = tk.Button(detail, text="Save", command=save)
    save_button.grid(row=0,column=2)
    detail.mainloop()




root = tk.Tk()
root.grid_anchor(anchor="n")
root.title("Movement Tracker")

partOfMovement = []

#root.attributes('-fullscreen',True)
movement_var = tk.StringVar()
xd = tk.StringVar()
hmm = tk.BooleanVar()

####################################
tk.Radiobutton(root, text="Movement 1", font=("Calibri","64"),variable=movement_var, value="Movement 1").grid(row=0)
tk.Radiobutton(root, text="Movement 2", font=("Calibri","64"),variable=movement_var, value="Movement 2").grid(row=1)
tk.Radiobutton(root, text="Movement 3", font=("Calibri","64"),variable=movement_var, value="Movement 3").grid(row=2)
####################################

####################################
repetitions_label = tk.Label(root, text="Repetitions:")
repetitions_label.grid(row=3,column=0,padx=5,pady=5)

repetitions_entry = tk.Entry(root)
repetitions_entry.insert(0,str(1))
repetitions_entry.grid(row=4,column=0,sticky="nsew")
####################################

####################################
plus_button_for_rep = tk.Button(root,text="+",command=rep_plus_button)
plus_button_for_rep.grid(row=4,column=1,sticky=tk.E)

minus_button_for_rep = tk.Button(root,text="-",command=rep_minus_button)
minus_button_for_rep.grid(row=4,column=2,sticky=tk.E)
####################################

####################################
duration_label = tk.Label(root, text="Duration (in seconds):")
duration_label.grid(row=5)

duration_entry = tk.Entry(root)
duration_entry.insert(0,str(1.5))
duration_entry.grid(row=6,column=0,sticky="nsew")
####################################

####################################
subject_label = tk.Label(root, text="Subject Name")
subject_label.grid(row=7)

subject_entry = tk.Entry(root)
subject_entry.insert(0,"inosens")
subject_entry.grid(row=8,column=0,sticky="nsew")
####################################

####################################
plus_button_for_dur = tk.Button(root,text="+",command=duration_plus_button)
plus_button_for_dur.grid(row=6,column=1,sticky=tk.E)
####################################

####################################
minus_button_for_dur = tk.Button(root,text="-",command=duration_minus_button)
minus_button_for_dur.grid(row=6,column=2,sticky=tk.E)
####################################

####################################
duration_label = tk.Label(root, text="Delay between per repetitions (in seconds):")
duration_label.grid(row=7)

delay_entry = tk.Entry(root)
delay_entry.insert(0,str(1.5))
delay_entry.grid(row=8,column=0,sticky="nsew")
####################################

####################################
details_button = tk.Button(root, text="Details", command=details)
details_button.grid()
####################################

####################################
start_button = tk.Button(root, text="Start", command=on_start_button_click)
start_button.grid()
####################################

####################################
exit_button = tk.Button(root, text="Exit", command=exit)
exit_button.grid()
####################################

# The time between the start and end of the movement.


root.mainloop()

