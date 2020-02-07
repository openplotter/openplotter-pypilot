#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by sailoog <https://github.com/openplotter/openplotter-pypilot>
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

import time, os, subprocess, sys, ujson
from openplotterSettings import language
from openplotterSettings import platform

class Start():
	def __init__(self, conf, currentLanguage):
		self.initialMessage = ''

	def start(self):
		green = '' 
		black = '' 
		red = '' 

		return {'green': green,'black': black,'red': red}

class Check():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-pypilot',currentLanguage)
		self.initialMessage = _('Checking Pypilot...')
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_boatimu']).decode(sys.stdin.encoding)
			self.pypilot_boatimu = True
		except: self.pypilot_boatimu = False
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot']).decode(sys.stdin.encoding)
			self.pypilot = True
		except: self.pypilot = False
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_web']).decode(sys.stdin.encoding)
			self.webapp = True
		except: self.webapp = False
	def check(self):
		platform2 = platform.Platform()
		green = '' 
		black = '' 
		red = '' 

		sklist = []
		try:
			setting_file = platform2.skDir+'/settings.json'
			data = ''
			with open(setting_file) as data_file:
				data = ujson.load(data_file)
			if 'pipedProviders' in data:
				for i in data['pipedProviders']:
					if i['pipeElements'][0]['options']['type']=='SignalK':
						if i['pipeElements'][0]['options']['subOptions']['type']=='udp':
							if i['pipeElements'][0]['options']['subOptions']['port']=='20220':
								sklist.append([i['id'],'UDP',i['enabled']])
					if i['pipeElements'][0]['options']['type']=='NMEA0183':
						if i['pipeElements'][0]['options']['subOptions']['type']=='tcp':
							if i['pipeElements'][0]['options']['subOptions']['port']=='20220':
								sklist.append([i['id'],'TCP',i['enabled']])
		except:pass

		if not self.pypilot_boatimu and not self.pypilot: 
			black = _('disabled')
			if sklist:
				for i in sklist:
					if i[2]:
						msg = _('Please disable this Signal K connection. ID: ')+ i[0]
						if not red: red = msg
						else: red += '\n'+msg
		elif self.pypilot_boatimu: 
			green = _('Only compass')
			exists = False
			if sklist:
				for i in sklist:
					if i[1] == 'TCP' and i[2]:
						msg = _('Please disable this Signal K connection. ID: ')+ i[0]
						if not red: red = msg
						else: red += '\n'+msg
					if i[1] == 'UDP' and i[2]: exists = True
			if not exists:
				msg = _('Please enable a Signal K connection fot Pypilot Signal K data')
				if not red: red = msg
				else: red += '\n'+msg
		elif self.pypilot: 
			green = _('Autopilot')
			if self.webapp: green += ' | '+_('Browser controlller')
			exists = False
			if sklist:
				for i in sklist:
					if i[1] == 'TCP' and i[2]: exists = True
			if not exists:
				msg = _('Please enable a Signal K connection fot Pypilot NMEA 0183 data')
				if not red: red = msg
				else: red += '\n'+msg
		
		udp = []
		tcp = []
		if sklist:
			for i in sklist:
				if i[1] == 'TCP': tcp.append(i[0])
				if i[1] == 'UDP': udp.append(i[0])
		if len(udp) > 1:
			msg = _('There are duplicate Signal K connections: ')
			msg2 = ''
			for i in udp:
				if not msg2: msg2 = i
				else: msg2 += ', '+i
			msg = msg+msg2
			if not red: red = msg
			else: red += '\n'+msg
		if len(tcp) > 1:
			msg = _('There are duplicate Signal K connections: ')
			msg2 = ''
			for i in tcp:
				if not msg2: msg2 = i
				else: msg2 += ', '+i
			msg = msg+msg2
			if not red: red = msg
			else: red += '\n'+msg

		return {'green': green,'black': black,'red': red}

