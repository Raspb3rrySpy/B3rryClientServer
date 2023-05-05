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
    def __init__(self, host, port, motor_handler, logname="server.log"):
        # Initialize Flask:
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.motor_handler = motor_handler
        # Configure the server's log:
        logging.basicConfig(filename=logname,
                            format="%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s",
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.NOTSET)
        # Set up routes:
        self.app.route("/")(self.index)
        self.app.route("/client")(self.client)
        self.app.route("/joystick")(self.joystick)
        self.app.route("/pantilt")(self.pantilt)

    def index(self):
        return render_template("client.html")

    def client(self):
        return render_template("client.html")

    def joystick(self):
        data = json.loads(request.args.get("data"))
        if data:
            # Package data:
            data = self.motor_handler.parse_joystick_data(data)
            data = json.dumps(data)
            self.motor_handler.send_motor_data(bytes(data, "utf-8"))
        return ""

    def pantilt(self):
        data = json.loads(request.args.get("data"))
        if data:
            pass
        return ""

    def start(self):
        self.motor_handler.connect()
        # Run the app:
        logging.info(f"Preparing to run on {self.host}:{self.port}...")
        app.run(host=self.host, port=self.port)
