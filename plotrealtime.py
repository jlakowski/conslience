#Realtime clustering and plotting
#Gets mocapdata from a TCP/IP socket
#And plots it in real time
# with color coded clusters!
#J Lakowski 1/13/2014

import mocaplib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import socket
import time


fig = plt.figure(dpi=100) #hi-res dpi=1000
plt.ion()
plt.show()

TCP_IP = "zx81.isl.uiuc.edu" 
TCP_PORT = 4710
#TCP_IP= "130.126.127.114"
#TCP_IP= "kam2.isl.uiuc.edu:4712"# for realtime
#TCP_PORT = 4712

s = socket.socket() 
s.connect((TCP_IP, TCP_PORT))
counter = 0
tstart = time.time()

#while counter < 100:
while True:
    data = s.recv(8192)
    print "Raw IN"
    print data
    fs = mocaplib.parseFrame(data)
    print "Parsed"
    print fs
    
    try:
        clust = mocaplib.cluster(fs, 660)
        nclus = len(clust[2]) #get the number of clusters
    except:
        pass
    
    coms = [[] for i in range(nclus)] #initialize array of the correct size
    iten = [[] for i in range(nclus)] #initialize array of the correct size
    rho  = [[] for i in range(nclus)] #initialize array of the correct size
    for i in range(0,nclus):
        coms[i] = mocaplib.clusCOM(clust[2][i])
        #iten[i] = mocaplib.findInertiaTensor(clust[0][i],coms[i])
        #rho[i] = len(clust[2][i])/mocaplib.findStretch(iten[i])
        
    #set up the axis
    #apparently it is faster if you do this for 
    #each frame?
    ax = Axes3D(fig)
    ax.set_xlim3d(-2000,2000)
    ax.set_ylim3d(-2000,2000)
    ax.set_zlim3d(-2000,2000)

    ax.scatter(*clust[0], c=clust[1])
        
    #display an orange dot at the centers of mass
    for j in range(0,nclus):
        ax.scatter(coms[j][0], coms[j][1], coms[j][2], c='orange')
        
    plt.draw()
    plt.clf()
    print 'frame %d'%counter 
    
        
    counter = counter +1
#calculate and show the fps
tstop = time.time()
tt = tstop - tstart
fps = counter/tt
print "processed %d frames in %f seconds" %(counter, tt)
print "rate: %f frames per second" %fps
