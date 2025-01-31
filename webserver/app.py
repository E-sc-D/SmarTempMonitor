import time
import eventlet
import random
import serial

eventlet.monkey_patch()

from stopwatch import Stopwatch
from temperature_fsm import TemperatureFSM  
from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

windowState = False
timer = Stopwatch()
fsm = TemperatureFSM(T1=30, T2=50, F1=2000, F2=500, DT=4)
app = Flask(__name__)
socketio = SocketIO(app)
Scss(app)
arduino = None

def arduino_send(valore):
    global arduino
    if arduino is not None:
        arduino.write(f"{valore}".encode())  # Send data with newline
        print(f"Valore inviato: {valore}")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to a topic
    client.subscribe("esp32/temperature")

def on_message(client, userdata, msg):
    global windowState
    fsm.update(float(msg.payload.decode()), timer.resetElapsed())
    print(f"Message received: {msg.topic} -> {msg.payload.decode()}")
    socketio.emit("temp_reading", {"temp": msg.payload.decode(), 
        "window" : msg.payload.decode(), 
        "status" : fsm.get_state()})
    client.publish("CU/frequency", str(fsm.get_frequency()))
    if windowState:
        valore = fsm.window_percentage
        arduino_send(valore)

@app.route("/")
def index():
   return render_template("index.html")

@socketio.on("connect") 
def on_connect_web():
    global arduino
    print("Client connected")
    timer.start()
    arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

@socketio.on("client_data")
def client_data(data):
    valore = data["window"]
    arduino_send(valore)

@socketio.on("reset")
def client_reset(data):
    fsm.resetState()

@socketio.on("auto")
def toggle_auto(data):
    global windowState
    windowState = not windowState

def background_task():
    broker = "192.168.1.5"
    port = 1883
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.loop_forever()

if __name__ in "__main__":
    socketio.start_background_task(background_task)
    socketio.run(app, debug=True)

