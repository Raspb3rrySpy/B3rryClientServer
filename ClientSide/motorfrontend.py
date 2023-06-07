"""
motorfrontend.py
Frontend motor handlers for B3rry client
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
import cmdpipe
import logging


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class MotorHandler:
    def __init__(self, hostname, port):
        self.command_pipe = cmdpipe.Transmitter(hostname, port)
        self.last_data_sent = None
        self.turbo = False

    def parse_joystick_data(self, data: dict, scale=1):
        """
        Takes raw joystick data and converts it to
        left and right motor speeds
        :param data: Raw joystick data in a python dict
        :param scale: Scale for computation of joystick values
        :return: Motor speed data in the form {"left": speed, "right": speed}
        """
        #  Reverse joystick data:
        x = -data.get("x")
        y = -data.get("y")
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            # Invalid data, so nothing else to do:
            return None
        left = scale * (y + x)
        right = -(scale * (y - x))
        if not self.turbo:
            logging.info("No turbo")
            left = left // 1.3
            right = right // 1.3
            print(left, right)
        return {"left": clamp(int(left), -100, 100), "right": clamp(int(right), -100, 100)}

    def connect(self):
        self.command_pipe.connect()

    def send_motor_data(self, data):
        #  Avoid sending redundant data:
        if data == self.last_data_sent:
            return
        self.last_data_sent = data
        self.command_pipe.send(data)

    def toggle_turbo(self):
        self.turbo = not self.turbo
