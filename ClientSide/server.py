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
import json
import logging
from flask import Flask, Response, render_template, request


class Server:
    def __init__(self, host, port, motor_handler):
        # Initialize Flask:
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.motor_handler = motor_handler

        # Set up routes:
        self.app.route("/")(self.index)
        self.app.route("/client")(self.client)
        self.app.route("/joystick")(self.joystick)
        self.app.route("/pantilt")(self.pantilt)
        self.app.route("/turbo")(self.turbo)
        self.app.route("/connect")(self.connect)

    def index(self):
        return render_template("index.html")

    def connect(self):
        return ""

    def client(self):
        return render_template("client.html")

    def joystick(self):
        data = json.loads(request.args.get("data"))
        if data:
            # Package data:
            logging.info(data)
            data = self.motor_handler.parse_joystick_data(data)
            logging.info(data)
            data = json.dumps(data)
            self.motor_handler.send_motor_data(bytes(data, "utf-8"))
        return ""

    def pantilt(self):
        data = json.loads(request.args.get("data"))
        if data:
            pass
        return ""

    def turbo(self):
        self.motor_handler.toggle_turbo()
        return ""

    def start(self):
        self.motor_handler.connect()
        # Run the app:
        logging.info(f"Preparing to client server on {self.host}:{self.port}...")
        self.app.run(host=self.host, port=self.port)
