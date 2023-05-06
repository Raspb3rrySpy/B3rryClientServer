"""
cmdpipe.py
Class definitions for commandpipe module.
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
import socket


class NotConnected(Exception):
    """
    Error raised when Transmitter socket is None.
    """
    pass


class Transmitter:
    """
    Transmitter:
    Transmits packets via socket to a Reciever.
    """
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socket = None

    def connect(self):
        """
        Connect to a Reciever.
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.hostname, self.port))

    def send(self, data: bytes):
        """
        Sends data to a remote Reciever.
        You MUST call connect first, otherwise it
        will raise a NotConnected error.
        :param data: Data to be sent
        :return: None
        """
        if self.socket is None:
            raise NotConnected("You must run Transmitter.connect() before attempting to send data.")
        self.socket.sendall(data)


class Reciever:
    """
    Reciever:
    Recieves packets sent via socket from a Transmitter.
    """
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.socket = None
        self.callback = None

    def listen(self, callback):
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
                    self.callback(data)
