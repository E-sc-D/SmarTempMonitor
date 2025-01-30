import time
import eventlet
import random
eventlet.monkey_patch()

from temperature_fsm import TemperatureFSM  
from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

fsm = TemperatureFSM(T1=30, T2=50, F1=1, F2=2, DT=10)
app = Flask(__name__)
socketio = SocketIO(app)
Scss(app)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to a topic
    client.subscribe("esp32/temperature")

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} -> {msg.payload.decode()}")

""" broker = "192.168.1.5"
port = 1883
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_forever() """


@app.route("/")
def index():
   return render_template("index.html")

@socketio.on("connect") 
def on_connect():
    print("Client connected")

@socketio.on("client_data")
def client_data(data):
    print(data["window"])

@socketio.on("reset")
def client_reset(data):
    print(data["btn"])

def background_task():
    while True:
        socketio.emit("temp_reading", {"temp": random.randint(10, 100), 
        "window" : random.randint(0,100), 
        "status" : 0})
        time.sleep(0.5)
        #fsm.update(temp, elapsed_time)


if __name__ in "__main__":
    socketio.start_background_task(background_task)
    socketio.run(app, debug=True)

