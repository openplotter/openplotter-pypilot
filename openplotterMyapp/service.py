#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by xxxx <https://github.com/xxxx/openplotter-myapp>
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

# this file should be called as sudo
# in non Raspberry systems, users have to provide the admin password every time an instruction contains "sudo". 
# We should try to put all instrucctions with "sudo" in only one file and execute it as "sudo"
if sys.argv[1]=='enable':
	subprocess.call(['systemctl', 'enable', 'openplotter-myapp-read'])
	subprocess.call(['systemctl', 'restart', 'openplotter-myapp-read'])

if sys.argv[1]=='disable':
	subprocess.call(['systemctl', 'disable', 'openplotter-myapp-read'])
	subprocess.call(['systemctl', 'stop', 'openplotter-myapp-read'])