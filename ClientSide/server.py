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
from flask import Flask, Response, render_template, request, redirect, url_for
from werkzeug.exceptions import HTTPException
import threading
import motorfrontend
import telemetryclient
import heartbeatclient


class Server:
    def __init__(self, host, port, debug):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self.motor_handler = None
        self.telemetry_client = None
        self.heart_client = None

        # Set up routes:
        self.app.route("/")(self.index)
        self.app.route("/client")(self.client)
        self.app.route("/joystick")(self.joystick)
        self.app.route("/pantilt")(self.pantilt)
        self.app.route("/turbo")(self.turbo)
        self.app.route("/connect")(self.connect)
        self.app.route("/log")(self.log)
        self.app.register_error_handler(HTTPException, self.handle_http_error)

    def index(self):
        return render_template("index.html")

    def connect(self):
        ip = request.args.get("ip")
        try:
            port = int(request.args.get("port"))
        except ValueError:
            port = None
        if ip and port:
            logging.info(f"Preparing to send connect_data_request to {ip}:{port}...")
            self.telemetry_client = telemetryclient.TelemetryClient(ip, port)
            request_data = {"type": "connect_data_request"}
            request_data = json.dumps(request_data)
            self.telemetry_client.connect()
            telemetry = self.telemetry_client.request_telemetry(bytes(request_data, "ascii"), 5)
            telemetry = json.loads(telemetry)
            if telemetry.get("type") == "connect_data_response":
                content = telemetry.get("content")
                remote_ip = content.get("private_ip")
                fpv_port = content.get("fpv_port")
                motor_port = content.get("motor_port")
                heart_port = content.get("heart_port")
                rover_log_port = content.get("log_port")
                self.motor_handler = motorfrontend.MotorHandler(remote_ip, motor_port)
                self.heart_client = heartbeatclient.HeartBeatClient(remote_ip, heart_port)
                heart_thread = threading.Thread(target=self.heart_client.start_beating)
                heart_thread.start()
                if not self.debug:
                    self.motor_handler.connect()
                return render_template("client.html",
                                       fpv_url=f"http://{remote_ip}:{fpv_port}",
                                       client_log_url=f"http://{self.host}:{self.port}/log",
                                       rover_log_url=f"http://{remote_ip}:{rover_log_port}/log")
            else:
                return self.error(f"Invalid telemetry type in telemetr: {telemetry}"), 500
        return self.error(f"Invalid port or IP address"), 400

    def client(self):
        return render_template("client.html")

    def joystick(self):
        data = json.loads(request.args.get("data"))
        if data and not self.debug:
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
        if not self.debug:
            self.motor_handler.toggle_turbo()
        return ""

    def log(self):
        resp = Response(self.get_log())
        resp.headers.add('Access-Control-Allow-Origin', '*')
        return resp

    @staticmethod
    def get_log():
        file_path = logging.getLoggerClass().root.handlers[0].baseFilename
        try:
            with open(file_path, "r") as file:
                log_data = file.read()
                return log_data
        except (FileNotFoundError, OSError) as e:
            logging.debug(f"Unable to get log data - error: {e}")
            return ""

    @staticmethod
    def error(msg):
        """Custom error handler"""
        return render_template("error.html", msg=msg)

    def handle_http_error(self, e):
        return self.error(f"{e.code} {e.name}: {e.description}"), e.code

    def start(self):
        logging.info(f"Preparing to client server on {self.host}:{self.port}...")
        self.app.run(host=self.host, port=self.port)
