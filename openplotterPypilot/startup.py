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
		
		def active(name):
			return not os.system('systemctl is-active ' + name)
		
		def addgreen(n):
			nonlocal green
			if green:
				n = ' | ' + n
			green += n

		def addred(n):
			nonlocal red
			if red:
				n = '\n' + n
			red += n

		def addblack(n):
			nonlocal black
			if black:
				n = ' | ' + n
			black += n
			
		#access
		skConnections = connections.Connections('PYPILOT')
		result = skConnections.checkConnection()
		if result[0] == 'pending' or result[0] == 'error' or result[0] == 'repeat' or result[0] == 'permissions':
			addred(result[1])
		if result[0] == 'approved' or result[0] == 'validated':
			addblack(_('Access to Signal K server validated'))

		#services status
		pypilot = self.conf.get('PYPILOT', 'pypilot')
		pypilot_boatimu = self.conf.get('PYPILOT', 'pypilot_boatimu')
		pypilot_web = self.conf.get('PYPILOT', 'pypilot_web')
		pypilot_hat = self.conf.get('PYPILOT', 'pypilot_hat')


		running = ' ' + _('running')
		notrunning = ' ' + _('not running')

		if active('pypilot'):
			if active('pypilot_boatimu'):
				addred(_('CONFLICT: pypilot and pypilot_boatimu running'))
			else:
				addgreen('pypilot' + running)
		elif active('pypilot_boatimu'):
			addgreen('pypilot_boatimu' + running)
		else:
			addblack('pypilot_boatimu' + notrunning)


		def showservice(name):
			if active(name):
				addgreen(name + running)
			else:
				addblack(name + notrunning)

		showservice('pypilot_web')
		showservice('pypilot_hat')


		return {'green': green,'black': black,'red': red}
