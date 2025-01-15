from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
Scss(app)

@app.route("/")
def index():
   return render_template("index.html")


if __name__ in "__main__":
    app.run(debug=True)

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