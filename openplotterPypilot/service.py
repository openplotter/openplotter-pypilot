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
import sys, subprocess

def disablestop(name):
    subprocess.call(['systemctl', 'disable', name])
    subprocess.call(['systemctl', 'stop', name])

def enablestart(name):
    subprocess.call(['systemctl', 'enable', name])
    subprocess.call(['systemctl', 'start', name])

config = {'disabled' : [],
          'imu' : ['pypilot_boatimu'],
          'autopilot' : ['pypilot', 'openplotter-pypilot-read']}
    
mode = sys.argv[1]

if not mode in config:
    print('invalid openplotter pypilot mode:', mode)

# make table of all possible pypilot services
allservices = {}
for name in config:
    for service in config[name]:
        allservices[service] = True

# remove from list services we are starting
services = config[mode]
for service in services:
    del allservices[service]

# stop unused services
for service in allservices:
    disablestop(service)

# start needed services
for service in services:
    enablestart(service)

