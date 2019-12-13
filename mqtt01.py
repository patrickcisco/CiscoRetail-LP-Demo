#!/usr/bin/env python3

import paho.mqtt.client as mqtt

import json
import requests
import datetime as dt
import sys
import os
import getopt
from random import randint
import webbrowser
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.remote.webdriver import WebDriver

import config.config as c

print(c.MERAKI_MV_LINK)
print(c.CISCO_VISION_DMP_URL)
print(c.MQTT_BROKER)
print(c.MQTT_BROKER_PORT)
print(c.MQTT_TOPIC)

# options = webdriver.ChromeOptions()
# options.add_argument("user-data-dir=/private/var/folders/sw/nz0vtk5n1m312x9v2x401fn00000gn/T/.com.google.Chrome.4yV1cF/Default") #Path to your chrome profile
# driver = webdriver.Chrome(options=options)


# executor_url = driver.command_executor._url
# session_id = driver.session_id

def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver
# driver.get(c.MERAKI_MV_LINK)
# bro = attach_to_session('http://127.0.0.1:64092', '8de24f3bfbec01ba0d82a7946df1d1c3')
# bro.get(c.MERAKI_MV_LINK)


# def send_it(token, room_id, message):

#         header = {"Authorization": "Bearer %s" % token,
#                   "Content-Type": "application/json"}

#         data = {"roomId": room_id,
#                 "text": message}

#         return requests.post("https://api.ciscospark.com/v1/messages/", headers=header, data=json.dumps(data), verify=True)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(c.MQTT_TOPIC)


def on_message(client, userdata, msg):
    data = msg.payload.decode("utf-8","ignore")
    info = json.loads(data)
    timestamp = str(info["ts"]).split('.')[0] + str(random_with_N_digits(3))
    link = c.MERAKI_MV_LINK + timestamp
    webbrowser.open(c.MERAKI_MV_LINK + timestamp, new=0)

#     m_decode=str(msg.payload.decode("utf-8","ignore"))
#     m_in=json.loads(m_decode)

#     print("timestamp = ",timestamp)
#     webbrowser.open(MERAKI_MV_LINK + timestamp, new=0)
#     print("Yes!")
#     product_id = str(m_in["item"])
#     res = send_it(BOT_TOKEN, TEAMS_ROOM, str(dt.datetime.now()) + "\n" + MERAKI_MV_LINK + timestamp)
#     if res.status_code == 200:
#         print("your message was successfully posted to Webex Teams")
#     else:
#         print("failed with statusCode: %d" % res.status_code)
#         if res.status_code == 404:
#                 print ("please check the bot is in the room you're attempting to post to...")
#         elif res.status_code == 400:
#                 print ("please check the identifier of the room you're attempting to post to...")
#         elif res.status_code == 401:
#                 print ("please check if the access token is correct...")    
    
client = mqtt.Client()
client.connect(c.MQTT_BROKER, c.MQTT_BROKER_PORT,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
