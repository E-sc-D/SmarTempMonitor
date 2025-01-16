from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)
Scss(app)

broker = "192.168.141.58"
port = 1883
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_forever()


if __name__ in "__main__":
    app.run(debug=True)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to a topic
    client.subscribe("esp32/temperature")

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} -> {msg.payload.decode()}")

@app.route("/")
def index():
   return render_template("index.html")

@socketio.on("connect")
def on_connect():
    print("Client connected")
    emit("server_message", {"message": "Welcome to the server!"})

# Handle messages from the client
@socketio.on("client_message")
def handle_client_message(data):
    print(f"Received from client: {data['message']}")
    # Respond back to the same client
    emit("server_message", {"message": f"Server received: {data['message']}"})

# Server-side initiated messages
def background_updates():
    while True:
        socketio.emit("server_message", {"message": "Periodic update from server"})
        time.sleep(5)

