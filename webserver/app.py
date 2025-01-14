from flask import Flask
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def index():
   return "Testing 123"


if __name__ in "__main__":
    app.run(dubug=True)