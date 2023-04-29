"""
motorbackend.py
Backend motor handlers for B3rry client
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

logging.basicConfig(filename="b3rry.log",
                    format="%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s",
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.NOTSET)


def handle_data(data):
    if not data:
        return
    data = json.loads(data)
    if not isinstance(data.get("left"), int) or not isinstance(data.get("right"), int):
        logging.info(f"Invalid data: {data}")
        return
    robohat.setLeftSpeed(data.get("left"))
    robohat.setRightSpeed(data.get("right"))


motor_host = "localhost"
motor_port = 10000
logging.info(f"Initializing RoboHat...")
robohat.init()
logging.info(f"Preparing to start reciever on: {motor_host}:{motor_port}")
reciever = cmdpipe.Reciever(motor_host, motor_port)
reciever.listen(handle_data)
