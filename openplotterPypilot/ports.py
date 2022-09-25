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
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-pypilot',currentLanguage)
		self.connections = []

	def usedPorts(self):
		pypilot = not os.system('systemctl is-active pypilot')
		pypilot_boatimu = not os.system('systemctl is-active pypilot_boatimu')
		pypilot_web = not os.system('systemctl is-active pypilot_web')
		pypilot_hat = not os.system('systemctl is-active pypilot_hat')
		usedPorts = []

		if pypilot_boatimu or pypilot:
			usedPorts.append({'id':'Pypilot1', 'description':_('Pypilot Server'), 'data':[], 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':'23322', 'editable':'0'})
			if pypilot:
				usedPorts.append({'id':'Pypilot2', 'description':_('Pypilot NMEA 0183 Server'), 'data':[], 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':'20220', 'editable':'0'})
		if pypilot_web:
			usedPorts.append({'id':'Pypilot3', 'description':_('Pypilot Web Control'), 'data':[], 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':'8000', 'editable':'0'})
		if pypilot_hat:
			usedPorts.append({'id':'Pypilot4', 'description':_('Pypilot HAT Control'), 'data':[], 'type':'TCP', 'mode':'server', 'address':'localhost', 'port':'33333', 'editable':'0'})

		return usedPorts
