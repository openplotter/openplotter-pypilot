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

class Gpio:
	def __init__(self,conf):
		self.conf = conf
		self.used = [] # {'app':'xxx', 'id':'xxx', 'physical':'n'}

	def usedGpios(self):

		pypilot = self.conf.get('PYPILOT', 'pypilot')
		pypilot_boatimu = self.conf.get('PYPILOT', 'pypilot_boatimu')
		pypilot_hat = self.conf.get('PYPILOT', 'pypilot_hat')

		if pypilot_boatimu == '1' or pypilot == '1':
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'6'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'9'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'14'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'20'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'25'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'30'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'34'})
			self.used.append({'app':'pypilot', 'id':'ground', 'physical':'39'})
			self.used.append({'app':'pypilot', 'id':'power', 'physical':'1'})
			self.used.append({'app':'pypilot', 'id':'power', 'physical':'17'})
			self.used.append({'app':'pypilot', 'id':'IMU', 'physical':'3'})
			self.used.append({'app':'pypilot', 'id':'IMU', 'physical':'5'})
			if pypilot == '1':
				if pypilot_hat == '1':
					self.used.append({'app':'pypilot', 'id':'power', 'physical':'2'})
					self.used.append({'app':'pypilot', 'id':'power', 'physical':'4'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'7'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'11'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'13'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'15'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'19'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'21'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'23'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'27'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'29'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'31'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'33'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'37'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'12'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'16'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'18'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'22'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'24'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'26'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'28'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'32'})
					self.used.append({'app':'pypilot', 'id':'pypilot hat', 'physical':'36'})

		return self.used