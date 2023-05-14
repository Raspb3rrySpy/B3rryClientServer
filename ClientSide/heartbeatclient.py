"""
heartbeatclient.py
Connects to a HeartBeatServer and keeps it from flipping out.
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
import socket
import logging


class NotConnected(Exception):
    """
    Error raised when HeartBeatClient.socket is None.
    """
    pass


class HeartBeatClient:
    """
    HeartBeatClient:
    Connects to a HeartBeatServer.
    """
    def __init__(self, hostname, port, max_wait=5):
        self.max_wait = max_wait
        self.hostname = hostname
        self.port = port
        self.socket = None

    def start_beating(self):
        """
        Blocks indefinitely, while sending beats to HeartBeatServer.
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))
        while True:
            self.socket.settimeout(self.max_wait)
            try:
                self.socket.sendall(b"FeelTheBeat")
                self.socket.settimeout(self.max_wait)
                _ = self.socket.recv(2048)
            except socket.timeout:
                logging.error("Sending or recieving heartbeat timed out!")
