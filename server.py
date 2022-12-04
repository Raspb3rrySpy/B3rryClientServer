# Import necessary libraries
import base64

import cv2
from flask import Flask, render_template

# Initialize the Flask app
app = Flask(__name__)
# Start video capture
camera = cv2.VideoCapture(0)


@app.route("/frame")
def get_frame():
    success, frame = camera.read()  # read the camera frame
    if success:
        # encode image as jpeg
        _, img_encoded = cv2.imencode('.jpg', frame)
        base64_utf8_str = base64.b64encode(img_encoded).decode('utf-8')
        return f'<img onload="setTimeout(function(){{this.reload()}}, 100)" src="data:image/jpeg;base64,' \
               f'{base64_utf8_str}">'


@app.route("/index")
def index():
    with open("index.html") as indexfile:
        return render_template(indexfile.read())


app.run(port=5000)
