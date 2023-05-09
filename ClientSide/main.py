"""
main.py
One .py file to rule them all... (Frontend)
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
import threading
import logging
import server
import motorfrontend


logging.basicConfig(filename="b3rry.log",
                    format="%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s",
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.NOTSET)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

logging.info("Creating and connecting motor handler...")
motor_handler = motorfrontend.MotorHandler("10.42.0.1", 30000)
motor_handler.connect()

logging.info("Starting server...")
client_server = server.Server("localhost", 8080, motor_handler)
server_thread = threading.Thread(target=client_server.start)
server_thread.start()
logging.info("Server thread started!")
