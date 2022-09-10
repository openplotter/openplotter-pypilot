#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
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

import os, sys, subprocess
from openplotterSettings import language
from openplotterSignalkInstaller import connections

class Start():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		self.initialMessage = _('Starting pypilot...')

	def start(self):
		green = '' 
		black = '' 
		red = '' 

		subprocess.call(['pkill', '-f', 'pypilot'])

		skConnections = connections.Connections('PYPILOT')
		result = skConnections.checkConnection()
		if result[0] == 'approved' or result[0] == 'validated':
			token = self.conf.get('PYPILOT', 'token')
			try:
				file = open(self.conf.home+'/.pypilot/signalk-token', 'r')
				token2 = file.read()
				token2 = token2.rstrip()
				file.close()
				if token != token2:
					file = open(self.conf.home+'/.pypilot/signalk-token', 'w')
					file.write(token)
					file.close()
			except:
				file = open(self.conf.home+'/.pypilot/signalk-token', 'w')
				file.write(token)
				file.close()
			pypilot = self.conf.get('PYPILOT', 'pypilot')
			pypilot_boatimu = self.conf.get('PYPILOT', 'pypilot_boatimu')
			pypilot_web = self.conf.get('PYPILOT', 'pypilot_web')
			pypilot_hat = self.conf.get('PYPILOT', 'pypilot_hat')
			if pypilot_boatimu == '1':
				msg = _('starting IMU only...')
				if not black: black = msg
				else: black+= ' | '+msg
				subprocess.Popen(['pypilot_boatimu','-q'], cwd = self.conf.home+'/.pypilot')
				subprocess.Popen('openplotter-pypilot-read')
			elif pypilot == '1':
				msg = _('starting autopilot...')
				if not black: black = msg
				else: black+= ' | '+msg
				subprocess.Popen('pypilot', cwd = self.conf.home+'/.pypilot')
				if pypilot_web == '1':
					msg = _('starting web control...')
					if not black: black = msg
					else: black+= ' | '+msg
					subprocess.Popen('pypilot_web')
				if pypilot_hat == '1':
					msg = _('starting HAT control...')
					if not black: black = msg
					else: black+= ' | '+msg
					subprocess.Popen('pypilot_hat')

		return {'green': green,'black': black,'red': red}

class Check():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-pypilot',currentLanguage)
		self.initialMessage = _('Checking pypilot...')


	def check(self):
		green = '' 
		black = '' 
		red = '' 

		#access
		skConnections = connections.Connections('PYPILOT')
		result = skConnections.checkConnection()
		if result[0] == 'pending' or result[0] == 'error' or result[0] == 'repeat' or result[0] == 'permissions':
			if not red: red = result[1]
			else: red+= '\n    '+result[1]
		if result[0] == 'approved' or result[0] == 'validated':
			msg = _('Access to Signal K server validated')
			if not black: black = msg
			else: black+= ' | '+msg

		#services status
		running = subprocess.check_output(['ps','aux']).decode(sys.stdin.encoding)
		running2 = running.replace('openplotter-pypilot-read','')
		running2 = running2.replace('openplotter-pypilot','')
		running2 = running2.replace('pypilot_web','')
		running2 = running2.replace('pypilot_hat','')
		running2 = running2.replace('pypilot_boatimu','')

		pypilot = self.conf.get('PYPILOT', 'pypilot')
		pypilot_boatimu = self.conf.get('PYPILOT', 'pypilot_boatimu')
		pypilot_web = self.conf.get('PYPILOT', 'pypilot_web')
		pypilot_hat = self.conf.get('PYPILOT', 'pypilot_hat')

		if pypilot_boatimu == '1':
			if not 'pypilot_boatimu' in running:
				msg = _('IMU only not running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('IMU only running')
				if not green: green = msg
				else: green+= ' | '+msg
			if 'pypilot' in running2:
				msg = _('IMU only and Autopilot running')
				if red: red += '\n   '+msg
				else: red = msg
			if not 'openplotter-pypilot-read' in running:
				msg = _('openplotter-pypilot-read not running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('openplotter-pypilot-read running')
				if not green: green = msg
				else: green+= ' | '+msg
		else:
			if 'pypilot_boatimu' in running:
				msg = _('IMU only running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('IMU only not running')
				if not black: black = msg
				else: black+= ' | '+msg
			if 'openplotter-pypilot-read' in running:
				msg = _('openplotter-pypilot-read running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('openplotter-pypilot-read not running')
				if not black: black = msg
				else: black+= ' | '+msg
		if pypilot == '1':
			if not 'pypilot' in running2:
				msg = _('Autopilot not running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('Autopilot running')
				if not green: green = msg
				else: green+= ' | '+msg
		else:
			if 'pypilot' in running2:
				msg = _('Autopilot running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('Autopilot not running')
				if not black: black = msg
				else: black+= ' | '+msg

		if pypilot_web == '1':
			if not 'pypilot_web' in running:
				msg = _('Web control not running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('Web control running')
				if not green: green = msg
				else: green+= ' | '+msg
			if not 'pypilot' in running2:
				msg = _('Autopilot not running')
				if red: red += '\n   '+msg
				else: red = msg
		else:
			if 'pypilot_web' in running:
				msg = _('Web control running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('Web control not running')
				if not black: black = msg
				else: black+= ' | '+msg

		if pypilot_hat == '1':
			if not 'pypilot_hat' in running:
				msg = _('HAT control not running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('HAT control running')
				if not green: green = msg
				else: green+= ' | '+msg
			if not 'pypilot' in running2:
				msg = _('Autopilot not running')
				if red: red += '\n   '+msg
				else: red = msg
		else:
			if 'pypilot_hat' in running:
				msg = _('HAT control running')
				if red: red += '\n   '+msg
				else: red = msg
			else:
				msg = _('HAT control not running')
				if not black: black = msg
				else: black+= ' | '+msg

		return {'green': green,'black': black,'red': red}

