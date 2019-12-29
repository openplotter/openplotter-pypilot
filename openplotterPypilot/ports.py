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
import os, subprocess, sys
from openplotterSettings import language

class Ports:
	def __init__(self,conf,currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-pypilot',currentLanguage)
		self.connections = []
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_boatimu']).decode(sys.stdin.encoding)
			self.pypilot_boatimu = True
		except: self.pypilot_boatimu = False
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot']).decode(sys.stdin.encoding)
			self.pypilot = True
		except: self.pypilot = False
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_webapp']).decode(sys.stdin.encoding)
			self.webapp = True
		except: self.webapp = False

	def usedPorts(self):
		usedPorts = []
		if self.pypilot_boatimu or self.pypilot:
			usedPorts.append({'id':'pypilotConn1', 'description':_('Internal Pypilot Signal K server'), 'data':_('Own Signal K format'), 'direction':'3', 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':21311, 'editable':'0'})
			usedPorts.append({'id':'pypilotConn2', 'description':_('Pypilot Signal K output'), 'data':'Signal K', 'direction':'2', 'type':'UDP', 'mode':'client', 'address':'localhost', 'port':20220, 'editable':'0'})
			if self.webapp:
				usedPorts.append({'id':'pypilotConn4', 'description':_('Autopilot browser controller'), 'data':'', 'direction':'3', 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':8000, 'editable':'0'})
		
		if self.pypilot:
			usedPorts.append({'id':'pypilotConn3', 'description':_('Pypilot NMEA 0183 output'), 'data':'NMEA 0183', 'direction':'3', 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':20220, 'editable':'0'})
		return usedPorts
