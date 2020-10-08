#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
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

class Gpio:
	def __init__(self,conf):
		self.conf = conf
		self.used = [] # {'app':'xxx', 'id':'xxx', 'physical':'n'}

	def usedGpios(self):
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_boatimu']).decode(sys.stdin.encoding)
			pypilot_boatimu = True
		except: pypilot_boatimu = False
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot']).decode(sys.stdin.encoding)
			pypilot = True
		except: pypilot = False

		if pypilot_boatimu or pypilot:
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'6'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'9'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'14'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'20'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'25'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'30'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'34'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'39'})
		if pypilot:
			self.used.append({'app':'pypilot', 'id':'power', 'physical':'1'})
			self.used.append({'app':'pypilot', 'id':'heading', 'physical':'3'})
			self.used.append({'app':'pypilot', 'id':'heading', 'physical':'5'})
			self.used.append({'app':'pypilot', 'id':'motor controller', 'physical':'8'})
			self.used.append({'app':'pypilot', 'id':'motor controller', 'physical':'10'})
			self.used.append({'app':'pypilot', 'id':'power', 'physical':'17'})
		elif pypilot_boatimu:
			self.used.append({'app':'pypilot', 'id':'power', 'physical':'1'})
			self.used.append({'app':'pypilot', 'id':'heading', 'physical':'3'})
			self.used.append({'app':'pypilot', 'id':'heading', 'physical':'5'})
			self.used.append({'app':'pypilot', 'id':'power', 'physical':'17'})

		return self.used