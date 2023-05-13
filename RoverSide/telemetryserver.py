"""
telemetryserver.py
Socket based telemetry server.
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


class TelemetryServer:
    """
    TelemetryServer:
    Sends and recieves from a TelemetryClient.
    """
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socket = None
        self.callback = None

    def start(self, callback):
        """
        This function blocks indefinitely, listening on a socket, so run it
        in a new thread.
        :param callback: Function to be called when a packet is recieved.
        :return: None
        """
        self.callback = callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen()
        while True:
            connection, address = self.socket.accept()
            with connection:
                logging.debug(f"Connection from: {address}")
                while True:
                    data = connection.recv(2048)
                    if not data:
                        break
                    connection.sendall(self.callback(data))
