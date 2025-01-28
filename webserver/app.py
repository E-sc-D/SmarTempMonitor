import time
import eventlet
import random
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

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

@socketio.on("disconnect")
def handle_disconnect():
    socketio.s

def background_task():
    while True:
        socketio.emit("temp_reading", {"temp": random.randint(10, 100)})
        time.sleep(5)


if __name__ in "__main__":
    socketio.start_background_task(background_task)
    socketio.run(app, debug=True)

