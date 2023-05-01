"""
server.py
Flask server for B3rry client
Copyright (C) 2022  Aiden Bohlander

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Import necessary libraries
import cv2
import json
import logging
import motorfrontend
from flask import Flask, Response, render_template, request

host = "192.168.42.5"
port = 8080
# Initialize the Flask app:
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("client.html")


@app.route('/client')
def client():
    return render_template("client.html")


@app.route("/joystick")
def joystick():
    data = json.loads(request.args.get("data"))
    if data:
        # Package data:
        data = control_handler.parse_joystick_data(data)
        data = json.dumps(data)
        print(data)
        control_handler.send_motor_data(bytes(data, "utf-8"))
    return ""


@app.route("/pantilt")
def pantilt():
    data = json.loads(request.args.get("data"))
    if data:
        print(data)
    return ""


# Configure the server's log:
logging.basicConfig(filename="b3rry.log",
                    format="%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s",
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.NOTSET)
# Start a video capture:
camera = cv2.VideoCapture(0)
logging.debug("Started video...")
# Create a control handler:
control_handler = motorfrontend.MotorHandler("localhost", 32000)
#control_handler.connect()
# Run the app:
logging.debug(f"Preparing to run on {host}:{port}...")
app.run(host=host, port=port)
