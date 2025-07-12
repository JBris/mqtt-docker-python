import paho.mqtt.client as mqtt
import time
import json
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()
    ERROR = auto()
    MAINTENANCE = auto()

class Vehicle:
    def __init__(self):
        self.state = State.IDLE

car = Vehicle()

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {msg.topic} -> {payload}")

    payload_dict = json.loads(payload)
    event = payload_dict.get("value")
    
    if event is None:
        print("Value not provided in message")
        return

    try:
        vehicle_state = State[event]
        car.state = vehicle_state
        print(car.state)
    except KeyError:
        print(f"Invalid state: {event}")

topic = "paho/temperature"
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.exit_flag = False 

mqttc.connect("localhost", 1883, 60)
mqttc.subscribe(topic)
mqttc.loop_start()

while car.state != State.STOPPED:
    time.sleep(5)

mqttc.loop_stop()
mqttc.disconnect()
