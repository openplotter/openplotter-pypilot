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
	subprocess.call(['systemctl', 'stop', 'pypilot'])
	subprocess.call(['systemctl', 'stop', 'pypilot_boatimu'])

if sys.argv[1]=='boatimu':
	subprocess.call(['systemctl', 'disable', 'pypilot'])
	subprocess.call(['systemctl', 'enable', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'stop', 'pypilot'])
	subprocess.call(['systemctl', 'restart', 'pypilot_boatimu'])

if sys.argv[1]=='pypilot':
	subprocess.call(['systemctl', 'disable', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'stop', 'pypilot_boatimu'])
	subprocess.call(['systemctl', 'enable', 'pypilot'])
	subprocess.call(['systemctl', 'restart', 'pypilot'])

if sys.argv[1]=='enableWeb':
	subprocess.call(['systemctl', 'enable', 'pypilot_web'])
	subprocess.call(['systemctl', 'restart', 'pypilot_web'])

if sys.argv[1]=='disableWeb':
	subprocess.call(['systemctl', 'disable', 'pypilot_web'])
	subprocess.call(['systemctl', 'stop', 'pypilot_web'])

if sys.argv[1]=='enableHat':
	subprocess.call(['systemctl', 'enable', 'pypilot_hat'])
	subprocess.call(['systemctl', 'restart', 'pypilot_hat'])

if sys.argv[1]=='disableHat':
	subprocess.call(['systemctl', 'disable', 'pypilot_hat'])
	subprocess.call(['systemctl', 'stop', 'pypilot_hat'])
        
