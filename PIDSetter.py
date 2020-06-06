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

def on_message(client, userdata, msg):  
    
    
    try:
        d = json.loads(msg.payload.decode('utf-8'))

    except Exception as ex:
        print(ex)
    
    if msg.topic == 'm_Data':
        
        """
        print()
        print('traveled1:', d['t1'])
        print('traveled2:', d['t2'])
        print('traveled3:', d['t3'])
        print('speed1:', d['s1'])
        print('speed2:', d['s2'])
        print('speed3:', d['s3'])
        """
        
        global speed1
        global speed2
        global speed3
        global counterman
        counterman+=1
        #speed1.append(d['s1'])
        #speed2.append(d['s2'])
        #speed3.append(d['s3'])
        
        #speed1 = speed1[-20:]
        #speed2 = speed2[-20:]
        #speed3 = speed3[-20:]
        
        
        #plt.cla()
     
        #plt.plot(speed1)
        #plt.plot(speed2)
        #plt.plot(speed3)
        
        
        #plt.pause(0.01)
        
        global goal
        
        global done
        
        global M
        global speed
        global kp
        global ki
        global once
        global act
        global phase
        global pastSpeed
        global ready
        
        global finished
        global stable
        global minFinished
        global tries
        global minKi
        
        
        speed[0] = d['s1']
        speed[1] = d['s2']
        speed[2] = d['s3']
        
        speed1.append(speed[0])
        speed2.append(speed[1])
        speed3.append(speed[2])
        
        
        if done == False:
            
            
            if ready:
                if phase == 1:
            
                    if pastSpeed > speed[M]:
                        pubHalt(client)
                        kp[M]+=0.01
                        ready = False
                        once = 0
                    pastSpeed = speed[M]
                    
                    if speed[M] > goal*.20:
                        kp[M]-=0.01
                        print(M+1,'chose Kp:', kp[M])
                        pubHalt(client)
                        ready = False
                        once = 0
                        ki[M] = 1.8
                        phase=2
                    
                elif phase == 2:
                    if speed[M] != 0:
                        finished += 1
                    if abs(speed[M]-goal) <= 1:
                        stable+=1
                    elif abs(speed[M]-goal) == 2:
                        stable -= 1
                    else:
                        stable = 0
                    
                    if finished > minFinished:
                        tries+=1
                        stable = 0
                        finished = 0
                        pubHalt(client)
                        ready = False
                        once = 0
                        if tries > 1:
                            ki[M] = minKi
                            print(M+1,'chose Ki:', minKi, 'stablizes starting at ', minFinished-20)
                            phase = 1
                            act[M] = 0
                            M+=1
                            minFinished = 100000
                            minKi = 0.05
                            tries = 0
                            
                            if M < 3:
                                act[M] = goal
                            else:
                                print('Kp: ', kp)
                                print('Ki: ', ki)
                                done = True
                    
                    if stable == 20 or finished-stable > 20:
                        if finished-stable <= 10:
                            minFinished = finished
                        minKi = ki[M]
                        ki[M]+=0.01
                        stable = 0
                        finished = 0
                        tries = 0
                        once = 0
                        ready = False
                        pubHalt(client)
                        
            if speed[M] == 0 and once == 0:
                #plt.cla()
                
                #plt.plot(speed1)
                #plt.plot(speed2)
                #plt.plot(speed3)
                
                
                #plt.pause(0.001)

                speed1 = []
                speed2 = []
                speed3 = []
                
                ready = True
                if phase == 1:
                    pubKp(client, kp[0], kp[1], kp[2])
                    #time.sleep(0.50)
                else:
                    pubKi(client, ki[0], ki[1], ki[2])
                
                pubSpeed(client, act[0],act[1],act[2])
                once = 1
                        
        else:
            
            speed1 = speed1[-20:]
            speed2 = speed2[-20:]
            speed3 = speed3[-20:]
            plt.cla()                  
            plt.plot(speed1)
            plt.plot(speed2)
            plt.plot(speed3)
            
            
            plt.pause(0.001)
            """
            if counterman >= 50:
                counterman = 0
                pubHalt(client)
                speed1 = []
                speed2 = []
                speed3 = []
            """
            if counterman == 30:
                pubHalt(client)
            
            if counterman > 30 and speed[0] == 0 and speed[1] == 0 and speed[2] == 0:
                counterman = 0
                speed1 = []
                speed2 = []
                speed3 = []
            
            
            
        #3 phases
        #1: get as close to goal as possible without sinking lower
        #if past greater than current, mark as done
        #if current greater than goal, choose one before this mark
            
            
        #2: increase Pi so that stablization at goal happens as quickly as possible
        # keep track of how many calls it takes starting from when speed>0 until reached
        #stable begins when within 1 of goal, retain this state for at least 5 to count
        #do this for each motor
        
        
        
            
        
            
        
            

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

goal = 40
done = False
        
M = 0
speed = [0, 0, 0]
kp = [.1, .1, .1]
ki = [1.5, 1.5, 1.5]
once = 0
act = [goal, 0, 0]
phase = 1
pastSpeed = 0
ready = False

finished = 0
stable = 0
minFinished = 100000
tries = 0
minKi = 0.05


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
