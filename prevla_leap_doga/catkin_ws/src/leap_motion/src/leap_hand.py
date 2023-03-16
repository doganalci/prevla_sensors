


import numpy as np
import matplotlib.pyplot as plt
import csv
import time
xs=[];ys=[];zs=[];t_low=[];indis=[];parmak=[];point=[];no=[];

data_path = "/home/doga18/Desktop/2023/catkin_ws/log/tt.csv"
#data = csv.load("/home/doga18/Desktop/2023/catkin_ws/log/tt.csv")
# data.dtype is [('x', '<f4'), ('y', '<f4'), ('z', '<f4'), ('intensity', '<f4'), ('t_low', '<u4'), ('t_high', '<u4')]
with open(data_path, newline='') as csvfile:
    data2 = csv.reader(csvfile, delimiter=',', quotechar='|')
    
    ttt=0
    for row in data2:

        txx=""
        hh=0
        for v in row :
            print(v)
            
            #txx=str(v)+"_"+str(v)+"_"+str(v)
            

            if   hh%13==1 : 
                point.append(float(v))
                txx+=str(v)+"_"
                print(txx)
            if hh%13==3  : 
                indis.append(float(v))
                txx+=str(v)    +"_"
                print(txx)

            if hh%13==4  : 
                parmak.append(float(v))
                txx+=str(v)
                print(txx)


            if hh%13==3  : d=0
            if hh%13==4  : pr=0
            if hh%13==5  : pr=0
            if hh%13==6 :  xs.append(float(v))
            if hh%13==7  : ys.append(float(v))
            if hh%13==8  : zs.append(float(v))
            
            #elif hh%4==3  : t_low.append('o')
            hh+=1
        if ttt>0: no.append(txx)
        ttt+=1
        print('txx:: ',txx)
        
            
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].


ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
print("no")
print(no)

print("xs:: ",xs)
print("ys:: ",ys)
print("zs:: ",zs)



for i in range(len(xs)):
    ttt="x: "+str(xs[i])+" - y: "+str( ys[i])+" - z: "+str(zs[i])
    ax.set_ylabel("Y   i-->   "+ str(i) +ttt)
    ax.scatter( xs[i], ys[i],zs[i],marker='o')
    print("i--> xs[i], ys[i],zs[i]:: ",i , xs[i], ys[i],zs[i])

    fig.canvas.draw()

    fig.canvas.flush_events()#    plt.close() # Close a figure window
    time.sleep(0.5)
    plt.savefig('hand_'+ str(i)+' .png')

 #   ax.scatter( xs[i], ys[i],zs[i],marker='o')

#ax.scatter(xs[0],ys[0],zs[0],marker='o')
#ax.scatter(xs[1],ys[1],zs[1],marker='o')



#plt.show()



print("go")

