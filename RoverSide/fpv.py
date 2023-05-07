"""
fpv.py
WebSocket FPV server for B3rry client
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
import sys
import time
import cv2
import asyncio
import websockets
import base64
import logging


class FPVServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.camera = None

    async def handle_connection(self, websocket):
        """
        Websocket connection handler
        :param websocket: Conected websocket
        :return: None
        """
        for frame in get_frames():
            await websocket.send(frame)

    def get_frames(self):
        """
        Generator function that uses cv2 to stream frames to a websocket,
        yielding byte-encoded frames.
        :return: None
        """
        while True:
            success, frame = camera.read()  # read the camera frame
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.png', frame)
                frame = base64.b64encode(buffer)
                yield bytes(str(time.time() * 1000), "ascii") + b':time:' + b'data:image/png;base64,' + frame

    def start(self):
        # Start video capture
        self.camera = cv2.VideoCapture(0)
        # Start the server
        start_server = websockets.serve(self.handle_connection, self.host, self.port)
        # Do async stuff
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(start_server)
        logging.info("Started server on " + "ws://" + str(self.host) + ":" + str(self.port) + "/")
