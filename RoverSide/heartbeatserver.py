"""
heartbeatserver.py
Calls back when host goes out of range.
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
import time


class HeartBeatServer:
    """
    HeartBeatServer:
    Calls back when client disconnects, and sends ping time to client.
    """
    def __init__(self, hostname, port, max_wait=5):
        self.hostname = hostname
        self.port = port
        self.last_packet_time = None
        self.socket = None
        self.max_wait = max_wait

    def start(self, callback):
        """
        This function blocks indefinitely, listening on a socket, so run it
        in a new thread.
        :param callback: Function to be called when a packet is recieved.
        :return: None
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(10)
        while True:
            connection, address = self.socket.accept()
            with connection:
                logging.debug(f"HeartBeatServer - connection from: {address}")
                timeout_count = 0
                while True:
                    connection.settimeout(self.max_wait)
                    try:
                        _ = connection.recv(2048)
                        connection.sendall(bytes(str(int(time.time())), "ascii"))
                        timeout_count = 0
                    except (socket.timeout, ConnectionResetError, ConnectionError, BrokenPipeError) as e:
                        # Uh, oh
                        logging.critical(f"Heartbeat lost due to: {e}")
                        # I said I'd call you back, right?
                        callback()
                        # EMT's worst nightmare: client died:
                        if timeout_count > 5:
                            logging.critical("Failed to recieve more than 5 heartbeats. Giving up...")
                            break
                        timeout_count += 1
