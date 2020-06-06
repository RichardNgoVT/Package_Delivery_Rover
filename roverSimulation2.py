import time
import paho.mqtt.client as mqtt
import json
from collections import defaultdict
import math 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def on_connect(client, userdata, flags, rc):
    print('Connected with result code', str(rc))
    global connected
    connected = True

def on_publish(client,userdata,result):             #create function for callback
    dog = 1
    #print('Published:', userdata, 'to', client)


def pubHalt(client):
    speed1, speed2, speed3 = 0, 0, 0
    formatter = "{\"id\": \"dev\", \"mode\": 1, \"s1\": "+str(speed1)+", \"s2\": "+str(speed2)+", \"s3\": "+str(speed3)+"}"

    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)

def pubSpeed(client, speed1, speed2, speed3):
    formatter = "{\"id\": \"dev\", \"mode\": 1, \"s1\": "+str(speed1)+", \"s2\": "+str(speed2)+", \"s3\": "+str(speed3)+"}"
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)
    
def pubKp(client, kp1, kp2, kp3):
    formatter = "{\"id\": \"dev\", \"mode\": 2, \"kp1\": "+str(round(kp1,3))+", \"kp2\": "+str(round(kp2,3))+", \"kp3\": "+str(round(kp3,3))+"}"
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)
    
    
def pubKi(client, ki1, ki2, ki3):
    formatter = "{\"id\": \"dev\", \"mode\": 3, \"ki1\": "+str(round(ki1,3))+", \"ki2\": "+str(round(ki2,3))+", \"ki3\": "+str(round(ki3,3))+"}"

    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)

def pubPixy(client, x, y, wid, hei, sig):
    formatter = "{\"id\": \"pixy\", \"x\": "+str(int(x))+", \"y\": "+str(int(y))+", \"wid\": "+str(int(wid))+", \"hei\": "+str(int(hei))+", \"sig\": "+str(int(sig))+"}"
    #formatter = "{\"id\": \"pixy\", \"x\": "+str(int(x))+", \"y\": "+str(int(y))+", \"wid\": "+str(int(wid))+", \"hei\": "+str(int(hei))+"}"
    print("Pixy: x=", x, "size=", wid)
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("pixy", formatter)

def pubUltra(client, dist):
    formatter = "{\"id\": \"ultra\", \"dist\": "+str(int(dist))+"}"
    print("Ultra: dist = ", dist)
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("ultra", formatter)

def pubArm(client, grabbed): 
    if grabbed:
        status = 'retrieved'
    else:
        status = 'searching'
        
    formatter = "{\"id\": \"arm\", \"stat\": "+status+"}"
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("arm", formatter)

def pubSig(client, speed1):
    speed2, speed3 = 0, 0
    formatter = "{\"id\": \"dev\", \"mode\": 4, \"s1\": "+str(speed1)+", \"s2\": "+str(speed2)+", \"s3\": "+str(speed3)+"}"
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)

def on_message(client, userdata, msg):  
    
    
    try:
        d = json.loads(msg.payload.decode('utf-8'))

    except Exception as ex:
        print(ex)
    
    if msg.topic == 'm_Data':
        
        global wheelLDistP
        global wheelRDistP
        global wheelBDistP        
        global counterman
        global inSight
        counterman+=1
        
        wheelLDist = d['t1']
        wheelRDist = d['t2']
        wheelBDist = d['t3']
        
        wheelLSpeed = d['s1']
        wheelRSpeed = d['s2']
        wheelBSpeed = d['s3']
        
        wheelLTrav = wheelLDist-wheelLDistP
        wheelRTrav = wheelRDist-wheelRDistP
        wheelBTrav = wheelBDist-wheelBDistP
        
        wheelLDistP = wheelLDist
        wheelRDistP = wheelRDist
        wheelBDistP = wheelBDist
        
        if abs(wheelLTrav) > 700 or abs(wheelRTrav) > 700 or abs(wheelBTrav) > 700:
            wheelLTrav = 0
            wheelRTrav = 0
            wheelBTrav = 0
        
        
        tic2Rad = 1/1600*2*math.pi
        tic2Cm = 1/15
        
        global posx
        global posy
        global posxB
        global posyB
        global goalx
        global goaly
        global direction
        minDist = 400
        mode = 'SP'
        
        
        
        if wheelLSpeed > 0 and wheelRSpeed > 0 and wheelBSpeed > 0:
            mode = 'TL'
        
        if wheelLSpeed < 0 and wheelRSpeed < 0 and wheelBSpeed < 0:
            mode = 'TR'
        
        if wheelLSpeed < 0 and wheelRSpeed > 0 and wheelBSpeed == 0:
            mode = 'N'
            
        if wheelLSpeed > 0 and wheelRSpeed < 0 and wheelBSpeed == 0:
            mode = 'S'
            
        if wheelLSpeed < 0 and wheelRSpeed == 0 and wheelBSpeed > 0:
            mode = 'NE'
            
        if wheelLSpeed > 0 and wheelRSpeed == 0 and wheelBSpeed < 0:
            mode = 'SW'
        
        if wheelLSpeed == 0 and wheelRSpeed > 0 and wheelBSpeed < 0:
            mode = 'NW'
            
        if wheelLSpeed == 0 and wheelRSpeed < 0 and wheelBSpeed > 0:
            mode = 'SE'    
        
        
        if mode == 'TL':
            direction -= abs(wheelBTrav)*tic2Rad
        
        if mode == 'TR':
            direction += abs(wheelBTrav)*tic2Rad
            
        while (direction>math.pi): 
            direction-=math.pi*2
            
        while (direction<-math.pi): 
            direction+=math.pi*2
        
        if mode == 'N':
            posxB += abs(wheelRTrav)*tic2Cm*math.sin(direction)#direction * dist
            posyB += abs(wheelRTrav)*tic2Cm*math.cos(direction)
        
        if mode == 'S':
            posxB -= abs(wheelRTrav)*tic2Cm*math.sin(direction)
            posyB -= abs(wheelRTrav)*tic2Cm*math.cos(direction)
        
        if mode == 'NE':
            posxB += abs(wheelLTrav)*tic2Cm*math.sin(direction+math.pi/4)
            posyB += abs(wheelLTrav)*tic2Cm*math.cos(direction+math.pi/4)
            
        if mode == 'SW':
            posxB -= abs(wheelLTrav)*tic2Cm*math.sin(direction+math.pi/4)
            posyB -= abs(wheelLTrav)*tic2Cm*math.cos(direction+math.pi/4)

        if mode == 'NW':
            posxB += abs(wheelRTrav)*tic2Cm*math.sin(direction-math.pi/4)
            posyB += abs(wheelRTrav)*tic2Cm*math.cos(direction-math.pi/4)
            
        if mode == 'SE':
            posxB -= abs(wheelRTrav)*tic2Cm*math.sin(direction-math.pi/4)
            posyB -= abs(wheelRTrav)*tic2Cm*math.cos(direction-math.pi/4)
            
        #print(direction/math.pi*180)
        #print(160+(math.atan2(goalx-posx, goaly-posy)-direction)/(math.pi/4)*150)
        posx = math.sin(direction)*10+posxB
        posy = math.cos(direction)*10+posyB
        
        
        
        angDiff = math.atan2(goalx-posx, goaly-posy)
        while (angDiff>math.pi): 
            angDiff-=math.pi*2
            
        while (angDiff<=-math.pi): 
            angDiff+=math.pi*2
        
        
        a = (direction-angDiff)%(2*math.pi)
        b = (-direction+angDiff)%(2*math.pi)
        
        if a<b:
            angApart = -a
        else:
            angApart = b
            
        
        
        if abs(angApart) <= math.pi/4:

            carrot = 160+(angApart)/(math.pi/4)*150
            carrSize = 60/abs(math.hypot(goalx-posx, goaly-posy))*60
            pubPixy(client, carrot, 0, carrSize, carrSize, 1)
            
            if abs(angApart) <= math.pi/8:# or abs(math.hypot(goalx-posx, goaly-posy)*math.sin(angApart))<20 or abs(math.hypot(goalx-posx, goaly-posy)) < 5:
                
                minDist = abs(math.hypot(goalx-posx, goaly-posy))
                
            inSight = True
            
        elif inSight:
            pubPixy(client, 0, 0, 0, 0, 5)
            inSight = False

        
        
        
        for o in obst:
            if (o[0] > posy and abs(direction) <= math.pi/2) or (o[0] < posy and abs(direction) > math.pi/2):
                #print(direction, posy, o[0])
                xcord = abs(o[0]-posy)*math.tan(direction)+posx
                if  xcord > o[1] and xcord < o[2]:
                    dist = abs((o[0]-posy)/math.cos(direction))
                    if dist < minDist:
                        minDist = dist
                        #print(minDist)
                    
        #print(minDist)
        pubUltra(client, minDist)
        if mode != 'SP' or counterman < 2:
            if counterman > 0:
                plt.plot(goalx/100,goaly/100,'bo',markersize=10) #<-- plot a black point at the origin
                plt.plot(posxB/100,posyB/100,'ok', markersize=10)
                plt.arrow(posxB/100,posyB/100,0.01*math.sin(direction),0.01*math.cos(direction),head_width=.2,head_length=.25)
                plt.plot(posx/100,posy/100,'go', markersize=5)
                for o in obst:
                    plt.arrow(o[1]/100,o[0]/100,(o[2]-o[1])/100,0, width=0.1, head_width = 0)
                   
                
                
            
                plt.xlim([-2,2]) #<-- set the x axis limits
                plt.ylim([-2,2]) #<-- set the y axis limits
                plt.grid(b=True, which='major') #<-- plot grid lines
                plt.pause(.001)
            
        
        
        
        
            
        
            
        
            

connected = False
pub = {}#times board thinks it published
pub = defaultdict(lambda:0,pub)
pubS = {}#times board successfully published
pubS = defaultdict(lambda:0,pubS)
pubT = {}#Last time that board successfully published
pubT = defaultdict(lambda:0,pubT)
rec = {}#times board should have recieved message
rec = defaultdict(lambda:0,rec)
recS = {}#times board successfully recieved message
recS = defaultdict(lambda:0,recS)
recM = {}#times board missed message
recM = defaultdict(lambda:0,recM)
subs = {}#boards that belong to each topic
subs = defaultdict(lambda:[],subs)

speed1 = []
speed2 = []
speed3 = []

#rovertest
goalx = 0
goaly = 100

dropx = 50
dropy = 100


obst = [[0, -50, 50]]


posxB = 0
posyB = -100

posx = posxB

posy = posyB

direction = math.pi
#direction = 0

wheelLDistP=0
wheelRDistP=0
wheelBDistP=0

inSight = False

counterman = 0

broker_address = 'soldier.cloudmqtt.com'
port = 12769
user = 'Richard'
password = 'Ngo'

client = mqtt.Client('StatsAndVerify')
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(broker_address, port=port)

client.loop_start()

while connected != True:
    time.sleep(0.1)

client.subscribe('ultra')
client.subscribe('pixy')
client.subscribe('arm')
client.subscribe('rover')
client.subscribe('m_Data')
client.subscribe('topics')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('Exiting')
    client.disconnect()
    client.loop_stop()




