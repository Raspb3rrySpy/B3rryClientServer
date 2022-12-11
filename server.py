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
from flask import Flask, Response, render_template, request

# Initialize the Flask app
app = Flask(__name__)
# Start video capture
camera = cv2.VideoCapture(0)


def get_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/stream')
def stream():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/client')
def client():
    return render_template("client.html")


@app.route("/joystick")
def joystick():
    data = json.loads(request.args.get("data"))
    if data:
        print(data)
    return ""


@app.route("/pantilt")
def pantilt():
    data = json.loads(request.args.get("data"))
    if data:
        print(data)
    return ""


app.run(host="192.168.42.6", port=8080)
