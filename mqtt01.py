#!/usr/bin/env python3

import paho.mqtt.client as mqtt

import json
import requests
import datetime as dt
import sys
import os
import getopt
from random import randint
# import webbrowser
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

import config.config as c
import platform

from webexteamssdk import WebexTeamsAPI
api = WebexTeamsAPI()

print(c.MERAKI_MV_LINK)
print(c.CISCO_VISION_DMP_URL)
print(c.MQTT_BROKER)
print(c.MQTT_BROKER_PORT)
print(c.MQTT_TOPIC)

# driver = webdriver.Chrome()
# chrome_options = Options()
# chrome_options.add_argument("--user-data-dir=datadir")
# driver = webdriver.Chrome(options=chrome_options)

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
    timestamp = str(info["timestamp"]).split('.')[0] + str(random_with_N_digits(3))
    link = c.MERAKI_MV_LINK + timestamp
    api.messages.create(c.LP_ROOM_ID, text=c.LP_TEXT + link)
    requests.get(c.CISCO_VISION_DMP_URL)

    
client = mqtt.Client(client_id='{}-{}'.format(platform.system(), random_with_N_digits(25)))
client.connect(c.MQTT_BROKER, c.MQTT_BROKER_PORT,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
