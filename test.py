#!/usr/bin/env python3
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import http.client as http
import urllib
import json
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.IN)

deviceId = "D60PrHmj"
deviceKey = "9RjbLG00rHv6dJ5W" 

def post_to_mcs(payload): 
        headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
        not_connected = 1 
        while (not_connected):
                try:
                        conn = http.HTTPConnection("api.mediatek.com:80")
                        conn.connect() 
                        not_connected = 0 
                except (http.HTTPException, socket.error) as ex: 
                        print ("Error: %s" % ex)
                        time.sleep(10)
			 # sleep 10 seconds 
        conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
        response = conn.getresponse() 
        print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
        data = response.read() 
        conn.close() 
try:
    while True:
        h0, t0= Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
        Switch = GPIO.input(17)
        if SwitchStatus == 1:
            print("Button Pressed")
            time.sleep(3)
        else:
            print("Button not Pressed")
            time.sleep(3)
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t0, h0))
        payload = {"datapoints":[{"dataChnId":"Switch","values":{"value":Switch}}]}	
        post_to_mcs(payload)
        time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
