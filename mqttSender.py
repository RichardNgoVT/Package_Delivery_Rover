import paho.mqtt.client as mqtt
import json
from collections import defaultdict

# Function ran whenever script publishes anything
def on_publish(client,userdata,result):             #create function for callback
    print('Published:', userdata, 'to', client)

def pubHalt():
    speed1, speed2, speed3 = 0, 0, 0
    formatter = "{\"id\": \"dev\", \"mode\": 1, \"s1\": "+str(speed1)+", \"s2\": "+str(speed2)+", \"s3\": "+str(speed3)+"}"

    # Set-up info for cloudmqtt
    broker_address = 'soldier.cloudmqtt.com'
    port = 12769
    user = 'Richard'
    password = 'Ngo'
    
    # Establishing connection with cloudmqtt server
    client = mqtt.Client('commander')
    client.username_pw_set(user, password=password)
    client.on_publish = on_publish
    client.connect(broker_address, port=port)
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)

def pubSpeed(speed1, speed2, speed3):
    formatter = "{\"id\": \"dev\", \"mode\": 1, \"s1\": "+str(speed1)+", \"s2\": "+str(speed2)+", \"s3\": "+str(speed3)+"}"

    # Set-up info for cloudmqtt
    broker_address = 'soldier.cloudmqtt.com'
    port = 12769
    user = 'Richard'
    password = 'Ngo'
    
    # Establishing connection with cloudmqtt server
    client = mqtt.Client('commander')
    client.username_pw_set(user, password=password)
    client.on_publish = on_publish
    client.connect(broker_address, port=port)
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)
    
def pubKp(kp1, kp2, kp3):
    formatter = "{\"id\": \"dev\", \"mode\": 2, \"kp1\": "+str(round(kp1,3))+", \"kp2\": "+str(round(kp2,3))+", \"kp3\": "+str(round(kp3,3))+"}"

    # Set-up info for cloudmqtt
    broker_address = 'soldier.cloudmqtt.com'
    port = 12769
    user = 'Richard'
    password = 'Ngo'
    
    # Establishing connection with cloudmqtt server
    client = mqtt.Client('commander')
    client.username_pw_set(user, password=password)
    client.on_publish = on_publish
    client.connect(broker_address, port=port)
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)
    
    
def pubKi(ki1, ki2, ki3):
    formatter = "{\"id\": \"dev\", \"mode\": 3, \"ki1\": "+str(round(ki1,3))+", \"ki2\": "+str(round(ki2,3))+", \"ki3\": "+str(round(ki3,3))+"}"

    # Set-up info for cloudmqtt
    broker_address = 'soldier.cloudmqtt.com'
    port = 12769
    user = 'Richard'
    password = 'Ngo'
    
    # Establishing connection with cloudmqtt server
    client = mqtt.Client('commander')
    client.username_pw_set(user, password=password)
    client.on_publish = on_publish
    client.connect(broker_address, port=port)
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)
    
def pubArm(grabbed): 
    if grabbed:
        status = 'retrieved'
    else:
        status = 'searching'
    
    formatter = "{\"id\": \"arm\", \"stat\": "+status+"}"
    
    # Set-up info for cloudmqtt
    broker_address = 'soldier.cloudmqtt.com'
    port = 12769
    user = 'Richard'
    password = 'Ngo'
    
    # Establishing connection with cloudmqtt server
    client = mqtt.Client('commander')
    client.username_pw_set(user, password=password)
    client.on_publish = on_publish
    client.connect(broker_address, port=port)
    
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)

def pubSig(signature):
    speed1 = -1
    if signature == 'blue':
        speed1 = 1
    speed2, speed3 = 0, 0
    formatter = "{\"id\": \"dev\", \"mode\": 4, \"s1\": "+str(speed1)+", \"s2\": "+str(speed2)+", \"s3\": "+str(speed3)+"}"
    
    # Set-up info for cloudmqtt
    broker_address = 'soldier.cloudmqtt.com'
    port = 12769
    user = 'Richard'
    password = 'Ngo'
    
    # Establishing connection with cloudmqtt server
    client = mqtt.Client('commander')
    client.username_pw_set(user, password=password)
    client.on_publish = on_publish
    client.connect(broker_address, port=port)
    # publishing topic information for all components with one second sleeps in between
    ret =  client.publish("dev", formatter)