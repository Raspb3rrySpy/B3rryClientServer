"""
logserver.py
Serves up logs using Flask.
Copyright (C) 2023 Aiden Bohlander

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
from flask import Flask, Response, render_template, request
import logging


class LogServer:
    def __init__(self, host, port):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.app.route("/log")(self.log)

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

    def start(self):
        logging.info(f"Preparing to start log server on {self.host}:{self.port}...")
        self.app.run(host=self.host, port=self.port)
