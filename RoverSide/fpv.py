"""
fpv.py
Flask FPV server
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
import cv2
import logging
from flask import Flask, Response, render_template, request


class FPVServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.camera = None
        self.app = Flask(__name__)
        self.app.route('/')(self.stream)

    def get_frames(self):
        while True:
            success, frame = self.camera.read()  # read the camera frame
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def stream(self):
        return Response(self.get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self):
        # Start video capture
        self.camera = cv2.VideoCapture(0)
        logging.info(f"Preparing to run FPV server on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port)


if __name__ == "__main__":
    testserver = FPVServer("localhost", 8080)
    testserver.start()
