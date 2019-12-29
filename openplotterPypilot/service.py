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

import sys, subprocess

if sys.argv[1]=='disable':
	subprocess.call(['systemctl', 'disable', 'pypilot'])
	subprocess.call(['systemctl', 'disable', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'disable', 'openplotter-pypilot-read'])
	subprocess.call(['systemctl', 'disable', 'pypilot_lcd'])
	subprocess.call(['systemctl', 'disable', 'pypilot_webapp'])
	subprocess.call(['systemctl', 'stop', 'pypilot'])
	subprocess.call(['systemctl', 'stop', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'stop', 'openplotter-pypilot-read'])
	subprocess.call(['systemctl', 'stop', 'pypilot_lcd'])
	subprocess.call(['systemctl', 'stop', 'pypilot_webapp'])

if sys.argv[1]=='boatimu':
	subprocess.call(['systemctl', 'disable', 'pypilot'])
	subprocess.call(['systemctl', 'disable', 'pypilot_lcd'])
	subprocess.call(['systemctl', 'disable', 'pypilot_webapp'])
	subprocess.call(['systemctl', 'enable', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'enable', 'openplotter-pypilot-read'])
	subprocess.call(['systemctl', 'stop', 'pypilot'])
	subprocess.call(['systemctl', 'stop', 'pypilot_lcd'])
	subprocess.call(['systemctl', 'stop', 'pypilot_webapp'])
	subprocess.call(['systemctl', 'restart', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'restart', 'openplotter-pypilot-read'])

if sys.argv[1]=='pypilot':
	subprocess.call(['systemctl', 'disable', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'enable', 'pypilot'])
	subprocess.call(['systemctl', 'enable', 'openplotter-pypilot-read'])
	subprocess.call(['systemctl', 'stop', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'restart', 'pypilot'])
	subprocess.call(['systemctl', 'restart', 'openplotter-pypilot-read'])

if sys.argv[1]=='enableBrowser':
	subprocess.call(['systemctl', 'enable', 'pypilot_webapp'])
	subprocess.call(['systemctl', 'restart', 'pypilot_webapp'])

if sys.argv[1]=='disableBrowser':
	subprocess.call(['systemctl', 'disable', 'pypilot_webapp'])
	subprocess.call(['systemctl', 'stop', 'pypilot_webapp'])

if sys.argv[1]=='enableLcd':
	subprocess.call(['systemctl', 'enable', 'pypilot_lcd'])
	subprocess.call(['systemctl', 'restart', 'pypilot_lcd'])

if sys.argv[1]=='disableLcd':
	subprocess.call(['systemctl', 'disable', 'pypilot_lcd'])
	subprocess.call(['systemctl', 'stop', 'pypilot_lcd'])

if sys.argv[1]=='restart':
	subprocess.call(['systemctl', 'stop', 'signalk.service'])
	subprocess.call(['systemctl', 'stop', 'signalk.socket'])
	subprocess.call(['systemctl', 'start', 'signalk.socket'])
	subprocess.call(['systemctl', 'start', 'signalk.service'])
