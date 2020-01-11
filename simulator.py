
import paho.mqtt.client as mqtt

import json
import time
import random
import config.config as c

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))

client = mqtt.Client()
client.connect(c.MQTT_BROKER, c.MQTT_BROKER_PORT, 60)
for i in range(1):
    msg = {
        "timestamp": "1578775363",
        "id": "303401B5F005A74004F014B6",
    }
    payload = json.dumps(msg)
    print(payload)
    client.publish(c.MQTT_TOPIC, payload)
    time.sleep(5)


client = mqtt.Client()
client.connect(c.MQTT_BROKER, c.MQTT_BROKER_PORT,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()


