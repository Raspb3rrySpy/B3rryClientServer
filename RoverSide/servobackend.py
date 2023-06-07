"""
servobackend.py
Backend servo handler for B3rry client
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
import robohat.robohat

# TODO: Fully implement servo software, it's just a stub for now.
robohat.robohat.startServod()
pins = []
angles = []
for pin, angle in zip(pins, angles):
    robohat.robohat.pinServod(pin, angle)