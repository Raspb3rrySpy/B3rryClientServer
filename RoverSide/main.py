"""
main.py
One .py file to rule them all... (Backend)
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
import logging
import threading
import heartbeatserver
import telemetryserver
import logserver
import json
import fpv
import sys


logging.basicConfig(filename="b3rry.log",
                    format="%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s",
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.NOTSET)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

debug = False

private_ip = socket.gethostbyname(socket.gethostname())
fpv_port = 20000
motor_port = 30000
telemetry_port = 40000
heart_port = 50000
log_port = 60000


def handle_telemetry(data):
    if not data:
        logging.debug(f"Invalid telemetry data: {data}")
    try:
        data = json.loads(data)
        if data.get("type") == "connect_data_request":
            # Client wants connection data, let's give it to them:
            return_data = {"type": "connect_data_response", "content": {"private_ip": private_ip,
                                                                        "fpv_port": fpv_port,
                                                                        "motor_port": motor_port,
                                                                        "heart_port": heart_port,
                                                                        "log_port": log_port}}
            return bytes(json.dumps(return_data), "ascii")

    except json.JSONDecodeError as e:
        logging.error(f"Error decoding telemetry data: {e}")


def on_heart_attack():
    # Defibrillate:
    from robohat import robohat
    robohat.setRightSpeed(0)
    robohat.setLeftSpeed(0)


if debug:
    def on_heart_attack():
        pass


if not debug:
    import motorbackend
    logging.info("Starting motor server...")
    motor_server = motorbackend.MotorServer(private_ip, motor_port)
    motor_server_thread = threading.Thread(target=motor_server.start)
    motor_server_thread.start()
    logging.info("Motor server thread started!")

    import servobackend

logging.info("Starting heartbeat server...")
heart_server = heartbeatserver.HeartBeatServer(private_ip, heart_port)
heart_server_thread = threading.Thread(target=heart_server.start, args=(on_heart_attack,))
heart_server_thread.start()
logging.info("Heartbeat server thread started!")

logging.info("Starting telemetry server...")
telemetry_server = telemetryserver.TelemetryServer(private_ip, telemetry_port)
telemetry_server_thread = threading.Thread(target=telemetry_server.start, args=(handle_telemetry,))
telemetry_server_thread.start()
logging.info("Telemetry server thread started!")

logging.info("Starting log server...")
log_server = logserver.LogServer(private_ip, log_port)
log_server_thread = threading.Thread(target=log_server.start)
log_server_thread.start()
logging.info("Log server thread started...")

logging.info("Starting FPV server...")
fpv_server = fpv.FPVServer(private_ip, fpv_port)
fpv_server_thread = threading.Thread(target=fpv_server.start)
fpv_server_thread.start()
logging.info("FPV server thread started!")
