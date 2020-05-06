#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
# Copyright (C) 2019 by Sean D'Epagnier <https://github.com/pypilot/openplotter-pypilot>
#
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.

import subprocess, sys

class SerialPorts:
	def __init__(self,conf):
		self.conf = conf
		self.connections = []
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot']).decode(sys.stdin.encoding)
			self.pypilot = True
		except: self.pypilot = False


	def usedSerialPorts(self):
		# {'app':'xxx', 'id':'xxx', 'data':'NMEA0183/NMEA2000/SignalK', 'device': '/dev/xxx', "baudrate": nnnnnn, "enabled": True/False}
		devices = []
		try:
			path = self.conf.home + '/.pypilot/serial_ports'
			with open(path, 'r') as f:
				for line in f:
					line = line.replace('\n', '')
					line = line.strip()
					devices.append(line)
		except: pass
		c = 1
		for i in devices:
			self.connections.append({'app':'Pypilot','id':str(c), 'data':'NMEA0183', 'device': i, 'baudrate': 'auto', "enabled": self.pypilot})
			c = c + 1
		return self.connections