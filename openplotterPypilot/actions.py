#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2024 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
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

import os, sys
from openplotterSettings import language
from pypilot.client import *

class Actions:
	def __init__(self,conf,currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-pypilot',currentLanguage)
		if self.conf.get('GENERAL', 'debug') == 'yes': self.debug = True
		else: self.debug = False
		self.available = []
		self.available.append({'ID':'com','name':_('Pypilot: command'),"module": "openplotterPypilot",'data':True,'default':'+10','help':_('Positive and negative relative values or absolute values are allowed: 270, +10, -10...')})
		self.available.append({'ID':'apOn','name':_('Pypilot: engage AP'),"module": "openplotterPypilot",'data':False,'default':'','help':''})
		self.available.append({'ID':'apOff','name':_('Pypilot: disengage AP'),"module": "openplotterPypilot",'data':False,'default':'','help':''})
		self.available.append({'ID':'tackS','name':_('Pypilot: tack starboard'),"module": "openplotterPypilot",'data':False,'default':'','help':''})
		self.available.append({'ID':'tackP','name':_('Pypilot: tack port'),"module": "openplotterPypilot",'data':False,'default':'','help':''})
		self.available.append({'ID':'tackC','name':_('Pypilot: tack cancel'),"module": "openplotterPypilot",'data':False,'default':'','help':''})

	def getValues(self):
		values = {}
		watches = list(self.client.watches)
		while len(values) < len(watches):
			self.client.poll(.1)
			msgs = self.client.receive()
			for name in msgs:
				values[name] = msgs[name]
		self.client.clear_watches()
		self.client.disconnect()
		return values

	def run(self,action,data):
		if action == 'apOff':
			try:
				self.client = pypilotClientFromArgs(["ap.enabled=false"])
				values = self.getValues()
			except Exception as e:
				if self.debug: 
					print('Error disengaging AP: '+str(e))
					sys.stdout.flush()
			else:
				if not 'ap.enabled' in values or values['ap.enabled']:
					if self.debug: 
						print('Error disengaging AP')
						sys.stdout.flush()

		elif action == 'apOn':
			try:
				self.client = pypilotClientFromArgs(["ap.heading"])
				values = self.getValues()
				if not 'ap.heading' in values:
					if self.debug: 
						print('Error reading heading')
						sys.stdout.flush()
				else:
					self.client = pypilotClientFromArgs(["ap.heading_command="+str(values['ap.heading']),"ap.enabled=true"])
					values2 = self.getValues()
			except Exception as e:
				if self.debug: 
					print('Error engaging AP: '+str(e))
					sys.stdout.flush()
			else:
				if not 'ap.enabled' in values2 or not values2['ap.enabled']:
					if self.debug: 
						print('Error engaging AP')
						sys.stdout.flush()

		elif action == 'com':
			if data:
				operator = ''
				data = data.strip()
				if data[0] == '+': operator = '+'
				elif data[0] == '-': operator = '-'
				try: data = float(data)
				except:
					if self.debug: 
						print('Error processing command data: '+str(e))
						sys.stdout.flush()
				else:
					if not operator:
						try:
							self.client = pypilotClientFromArgs(["ap.heading_command="+str(data)])
							values = self.getValues()
						except Exception as e:
							if self.debug: 
								print('Error adding absolute value to command: '+str(e))
								sys.stdout.flush()
					else:
						try:
							self.client = pypilotClientFromArgs(["ap.heading_command"])
							values = self.getValues()
						except Exception as e:
							if self.debug: 
								print('Error getting command value: '+str(e))
								sys.stdout.flush()
						else:
							if not 'ap.heading_command' in values:
								if self.debug: 
									print('Error getting command value')
									sys.stdout.flush()
							else:
								if operator == '+' or operator == '-':
									try:
										self.client = pypilotClientFromArgs(["ap.heading_command="+str(values['ap.heading_command']+data)])
										values2 = self.getValues()
									except Exception as e:
										if self.debug:
											if operator == '+': print('Error adding positive value to command: '+str(e))
											elif operator == '-': print('Error adding negative value to command: '+str(e))
											sys.stdout.flush()
									else:
										if not 'ap.heading_command' in values2:
											if self.debug: 
												if operator == '+': print('Error adding positive value to command')
												elif operator == '-': print('Error adding negative value to command')
												sys.stdout.flush()


		elif action == 'tackP':
			try:
				self.client = pypilotClientFromArgs(["ap.tack.direction=port","ap.tack.state=begin"])
				values = self.getValues()
			except Exception as e:
				if self.debug: 
					print('Error tacking port: '+str(e))
					sys.stdout.flush()
			else:
				if not 'ap.tack.state' in values or values['ap.tack.state'] != 'tacking':
					if self.debug: 
						print('Error tacking port')
						sys.stdout.flush()

		elif action == 'tackS':
			try:
				self.client = pypilotClientFromArgs(["ap.tack.direction=starboard","ap.tack.state=begin"])
				values = self.getValues()
			except Exception as e:
				if self.debug: 
					print('Error tacking starboard: '+str(e))
					sys.stdout.flush()
			else:
				if not 'ap.tack.state' in values or values['ap.tack.state'] != 'tacking':
					if self.debug: 
						print('Error tacking starboard')
						sys.stdout.flush()

		elif action == 'tackC':
			try:
				self.client = pypilotClientFromArgs(["ap.tack.state=none"])
				values = self.getValues()
			except Exception as e:
				if self.debug: 
					print('Error canceling tack: '+str(e))
					sys.stdout.flush()
			else:
				if not 'ap.tack.state' in values or values['ap.tack.state'] != 'none':
					if self.debug: 
						print('Error canceling tack')
						sys.stdout.flush()
