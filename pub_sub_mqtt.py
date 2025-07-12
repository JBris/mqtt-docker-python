import paho.mqtt.client as mqtt
import time
import random
import json

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {msg.topic} -> {payload}")

    payload_dict = json.loads(payload)

    if payload_dict["value"] == "exit":
        print("Exiting")
        client.exit_flag = True

topic = "paho/temperature"
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.exit_flag = False 

mqttc.connect("localhost", 1883, 60)
mqttc.subscribe(topic)

mqttc.loop_start()

while not mqttc.exit_flag:
    sensor_reading = random.uniform(5, 15)
    print(sensor_reading)

    json_message = json.dumps({"value": sensor_reading })
    mqttc.publish(topic, json_message)

    time.sleep(5)

mqttc.loop_stop()
mqttc.disconnect()