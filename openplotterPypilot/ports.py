#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2015 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
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
import os
from openplotterSettings import language

class Ports:
	def __init__(self,conf,currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-pypilot',currentLanguage)
		self.connections = []
		try: port = int(self.conf.get('PYPILOT', 'pypilotConn2'))
		except: port = 52000 #default port
		self.connections.append({'id':'pypilotConn1', 'description':_('Internal Pypilot Signal K server'), 'data':_('Own Signal K format'), 'direction':'3', 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':21311, 'editable':'0'})
		self.connections.append({'id':'pypilotConn2', 'description':_('Pypilot Signal K output'), 'data':_('Signal K keys: '), 'direction':'2', 'type':'UDP', 'mode':'client', 'address':'localhost', 'port':port, 'editable':'1'})
		self.connections.append({'id':'pypilotConn3', 'description':_('Pypilot NMEA 0183 output'), 'data':'NMEA 0183: ', 'direction':'3', 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':20220, 'editable':'0'})
	
	def usedPorts(self):
		usedPorts = []
		mode = self.conf.get('PYPILOT', 'mode')
		if mode == '1': # imu
			usedPorts.append(self.connections[0])
			usedPorts.append(self.connections[1])
		elif mode == '2': # pypilot
			usedPorts.append(self.connections[0])
			usedPorts.append(self.connections[1])
			usedPorts.append(self.connections[2])
		if usedPorts: return usedPorts
