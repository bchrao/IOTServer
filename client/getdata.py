#!/usr/bin/env python

# Reference: https://thingsboard.io/docs/samples/raspberry/temperature/

import smbus2
import bme280
import socket
import time
import paho.mqtt.client as mqtt
import json
from gpiozero import CPUTemperature

Host = "Host"
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
INTERVAL = 5
sensor_data = {'temperature': 0, 'pressure' : 0, 'humidity' : 0, 'cputemp' : 0}
next_reading = time.time()

def mqtt_connect():
    client = mqtt.Client()
    client.connect(Host, 1883, 60)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    print('Connected to %s MQTT Broker'%(Host))
    return client

def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code: {}".format(rc))

def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(INTERVAL)

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.loop_start()
    data = bme280.sample(bus, address, calibration_params)
    tempf = float("{0:.2f}".format(((data.temperature)*1.8)+32))
    press = float("{0:.2f}".format((data.pressure)/33.863))
    humid = float("{0:.2f}".format(data.humidity))
    cpuf = float("{0:.2f}".format((((CPUTemperature()).temperature)*1.8)+32))
    print(u"Temperature: {:g}\u00b0F, Barametric: {:g}inHg, Humidity: {:g}%, CPU Temp: {:g}\u00b0F".format(tempf, press, humid, cpuf))
    sensor_data['temperature'] = tempf
    sensor_data['pressure'] = press
    sensor_data['humidity'] = humid
    sensor_data['cputemp'] = cpuf

    client.publish(socket.gethostname(), json.dumps(sensor_data), 1)
    time.sleep(INTERVAL)
    client.loop_stop()

else:
    pass
