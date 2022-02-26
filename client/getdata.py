#!/usr/bin/env python

# Reference: https://thingsboard.io/docs/samples/raspberry/temperature/
import os
import smbus2
import bme280
import socket
import time
import paho.mqtt.client as mqtt
import json
from gpiozero import CPUTemperature

local_cache = r'/home/pi/Documents/getdata.tmp'
Host = "Host"
mqtt_port = 1883
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
INTERVAL = 5
sensor_data = {'temperature': 0, 'pressure' : 0, 'humidity' : 0, 'cputemp' : 0}
next_reading = time.time()

# MQTT Client Config
client = mqtt.Client()
client.connect(Host, mqtt_port, 60)
client.loop_start()

try:
    while True:
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

        # Checking if server is available
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((Host,mqtt_port))
        if result == 0:
           # if local data exists, upload and delete local data
           if os.path.exists(local_cache):
               print('file already exists')
               with open(local_cache, 'r') as lc:
                   content = lc.read()
                   lc.close()
                   #### left off here
           else:
               # create a file
               with open(file_path, 'w') as fp:
                   # uncomment if you want empty file
                   fp.write('This is first line')
             # read local, add to sensor_data and delete local
           # Sending humidity and temperature data
           client.publish(socket.gethostname(), json.dumps(sensor_data), 1)
        else:
            # Append sensor_data to local storage
            print()
        sock.close()

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
