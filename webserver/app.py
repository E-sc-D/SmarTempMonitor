import time
import eventlet
import random
import serial

eventlet.monkey_patch() #serve davvero????????

from utils.stopwatch import Stopwatch
from utils.temperature_fsm import TemperatureFSM  
from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

windowIsAuto = False
timer = Stopwatch()
fsm = TemperatureFSM(T1=20, T2=30, F1=5000, F2=2000, DT=4)
app = Flask(__name__)
socketio = SocketIO(app)
Scss(app)
arduino = None
client = None
arduino_mode = "mode:-1"

def arduino_send(valore):
    global arduino
    if arduino is not None:
        arduino.write(valore.encode())  # Send data with newline
        print(f"Valore inviato: {valore}")

#when is connected via mqtt to esp
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        # Subscribe to a topic
        client.subscribe("esp32/temperature")

#when receiving a message by esp32, mqtt
def on_message(client, userdata, msg):
    global windowIsAuto, timer, arduino_mode

    line = arduino.readline().decode('utf-8').strip()
    if line.startswith("mode:"):
        arduino_mode = line

    fsm.update(float(msg.payload.decode()), timer.resetElapsed())
    print(f"Message received: {msg.topic} -> {msg.payload.decode()}")
    socketio.emit("temp_reading", {"temp": msg.payload.decode(), 
        "window" : fsm.window_percentage, 
        "status" : fsm.get_state()})
        
    if fsm.is_frequency_sent() == 0:
        client.publish("CU/frequency", str(fsm.get_frequency()))
        fsm.frequency_sent = 1

    if arduino_mode == "mode:1":
        arduino_send(f"temp:{msg.payload.decode()}\0")

    if windowIsAuto and arduino_mode == "mode:-1":
        arduino_send(f"win:{fsm.window_percentage}\0")

@app.route("/")
def index():
   return render_template("index.html")

@socketio.on("connect") 
def on_webClient_connect():
    global arduino,timer
    
    print("Client connected")
    timer.start()
    connect_mqtt()
    arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

@socketio.on("client_data")
def on_webClient_data(data):
    arduino_send(f"win:{data["window"]}\0")

@socketio.on("reset")
def on_webClient_reset(data):
    fsm.resetState()

@socketio.on("auto")
def on_webClient_windowModeToggle(data):
    global windowIsAuto
    windowIsAuto = not windowIsAuto

def connect_mqtt():
    global client

    # Controlla se il client MQTT è già connesso
    if client is None or not client.is_connected():
        print("Connessione MQTT...")
        broker = "192.168.1.5"
        port = 1883
        client = mqtt.Client(client_id="CU_01")
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker, port, 60)

        # Inizia il ciclo di gestione dei messaggi MQTT in background
        client.loop_start()
    else:
        print("Connessione MQTT già attiva.")

@socketio.event
def disconnect():
    print("Disconnesso da SocketIO")

    # Disconnessione MQTT se necessario
    if client:
        client.disconnect()
        client.loop_stop()

socketio.run(app, debug=True)
