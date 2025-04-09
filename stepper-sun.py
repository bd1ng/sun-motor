# subscriber.py
import paho.mqtt.client as mqtt
import time
import json
from time import sleep
from adafruit_crickit import crickit		 
from adafruit_motor import stepper 				

STEP_MOTOR = crickit.stepper_motor 
INTERSTEP_DELAY = 0.01
STEPS_PER_REV = 200

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
        # Subscribe to topic
        client.subscribe("pythontest/sensors/mysensor")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        temperature = payload.get('temperature')

        print(f"temperature: {payload.get('temperature')}")

        if temperature > 23:
                for i in range(STEPS_PER_REV):	
                    STEP_MOTOR.onestep(direction=stepper.FORWARD)
                    time.sleep(INTERSTEP_DELAY)
                    STEP_MOTOR.release()
        else:
                sleep(1)
    except Exception as e:
        print("Error processing message:", e)

# Create subscriber client
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

# Connect to public broker
print("Connecting to broker...")
subscriber.connect("test.mosquitto.org", 1883, 60)

# Start the subscriber loop
subscriber.loop_start()

try:
    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping subscriber...")
    subscriber.loop_stop()
    subscriber.disconnect()