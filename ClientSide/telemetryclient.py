"""
telemetryclient.py
Socket based telemetry client.
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
    Error raised when TelemetryClient.socket is None.
    """
    pass


class TelemetryClient:
    """
    TelemetryClient:
    Connection to a TelemetryServer.
    """
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socket = None

    def connect(self):
        """
        Connect to a TelemetryServer.
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))

    def request_telemetry(self, data: bytes, timeout: int):
        """
        Sends data to a remote Reciever.
        You MUST call connect first, otherwise it
        will raise a NotConnected error.
        :param data: Data to be sent
        :param timeout: Time to wait for response
        :return: Server's Response
        """
        if self.socket is None:
            raise NotConnected("You must run TelemetryClient.connect() before attempting to send data.")
        self.socket.sendall(data)
        self.socket.settimeout(timeout)
        try:
            data = self.socket.recv(2048)
        except socket.timeout:
            logging.debug("Telemetry timed out...")
            data = None
        return data
