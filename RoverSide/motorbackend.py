"""
motorbackend.py
Backend motor server for B3rry client
Copyright (C) 2023  Aiden Bohlander

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
import json
import cmdpipe
import logging
import robohat.robohat as robohat


class MotorServer:
    def __init__(self, host, port):
        self.motor_host = host
        self.motor_port = port
        self.reciever = None

    def handle_data(self, data):
        if not data:
            return
        logging.info(data)
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            logging.debug(f"{e}\ndata: {data}")
        logging.info(data)
        if not isinstance(data.get("left"), int) or not isinstance(data.get("right"), int):
            logging.info(f"Invalid data: {data}")
            return
        robohat.setLeftSpeed(data.get("left"))
        robohat.setRightSpeed(data.get("right"))

    def start(self):
        logging.info(f"Initializing RoboHat...")
        robohat.init()
        logging.info(f"Preparing to start reciever on: {self.motor_host}:{self.motor_port}")
        self.reciever = cmdpipe.Reciever(self.motor_host, self.motor_port)
        self.reciever.listen(self.handle_data)
