#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2015 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
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
import os, subprocess
from openplotterSettings import conf
from openplotterSettings import language

def main():
	conf2 = conf.Conf()
	currentdir = os.path.dirname(__file__)
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-pypilot',currentLanguage)

	print(_('Removing incompatible packages and installing new ones...'))
	try:
		subprocess.call(['apt', '-y', 'autoremove', 'sense-hat'])
		subprocess.call(['pip', 'install', 'pywavefront'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Compiling RTIMULib2 for python2 and python3...'))
	try:
		subprocess.call(['rm', '-f', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['rm', '-rf', 'python-RTIMULib2-master'], cwd=conf2.home+'/')
		subprocess.call(['wget', 'https://github.com/openplotter/python-RTIMULib2/archive/master.zip'], cwd=conf2.home+'/')
		subprocess.call(['unzip', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['rm', '-f', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['python', 'setup.py', 'build'], cwd=conf2.home+'/python-RTIMULib2-master/')
		subprocess.call(['python', 'setup.py', 'install'], cwd=conf2.home+'/python-RTIMULib2-master/')
		subprocess.call(['python3', 'setup.py', 'build'], cwd=conf2.home+'/python-RTIMULib2-master/')
		subprocess.call(['python3', 'setup.py', 'install'], cwd=conf2.home+'/python-RTIMULib2-master/')
		subprocess.call(['rm', '-rf', 'python-RTIMULib2-master'], cwd=conf2.home+'/')
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Compiling Pypilot for python2...'))
	try:
		subprocess.call(['rm', '-f', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['rm', '-rf', 'pypilot-master'], cwd=conf2.home+'/')
		subprocess.call(['rm', '-rf', 'pypilot_data-master'], cwd=conf2.home+'/')
		subprocess.call(['wget', 'https://github.com/openplotter/pypilot/archive/master.zip'], cwd=conf2.home+'/')
		subprocess.call(['unzip', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['rm', '-f', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['wget', 'https://github.com/pypilot/pypilot_data/archive/master.zip'], cwd=conf2.home+'/')
		subprocess.call(['unzip', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['rm', '-f', 'master.zip'], cwd=conf2.home+'/')
		subprocess.call(['cp', '-rv', 'pypilot_data-master/.', 'pypilot-master'], cwd=conf2.home+'/')
		subprocess.call(['python', 'setup.py', 'build'], cwd=conf2.home+'/pypilot-master/')
		subprocess.call(['python', 'setup.py', 'install'], cwd=conf2.home+'/pypilot-master/')
		subprocess.call(['rm', '-rf', 'pypilot-master'], cwd=conf2.home+'/')
		subprocess.call(['rm', '-rf', 'pypilot_data-master'], cwd=conf2.home+'/')
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Creating config files...'))
	try:
		pypilotFolder = conf2.home+'/.pypilot'
		if not os.path.exists(pypilotFolder): os.mkdir(pypilotFolder)
		skConfFile = pypilotFolder+'/signalk.conf'
		if not os.path.exists(skConfFile):
			fo = open(skConfFile, "w")
			fo.write( '{"host": "localhost"}')
			fo.close()
		subprocess.call(['chown', '-R', conf2.user, pypilotFolder])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Adding pypilot, pypilot_boatimu and openplotter-pypilot-read services...'))
	try:
		fo = open('/etc/systemd/system/pypilot_boatimu.service', "w")
		fo.write( '[Unit]\nDescription=pypilot boatimu\nDefaultDependencies=false\nConflicts=pypilot.service\n\n[Service]\nType=simple\nExecStart=pypilot_boatimu -q\nStandardOutput=syslog\nStandardError=syslog\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=2\n\n[Install]\nWantedBy=local-fs.target')
		fo.close()
		fo = open('/etc/systemd/system/pypilot.service', "w")
		fo.write( '[Unit]\nDescription=pypilot\nDefaultDependencies=false\nConflicts=pypilot_boatimu.service\n\n[Service]\nType=simple\nExecStart=pypilot\nStandardOutput=syslog\nStandardError=syslog\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=2\n\n[Install]\nWantedBy=local-fs.target')
		fo.close()
		fo = open('/etc/systemd/system/openplotter-pypilot-read.service', "w")
		fo.write( '[Service]\nExecStart=openplotter-pypilot-read\nStandardOutput=syslog\nStandardError=syslog\nUser='+conf2.user+'\n[Install]\nWantedBy=multi-user.target')
		fo.close()
		subprocess.call(['systemctl', 'daemon-reload'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Copying openplotter-pypilot-read script manually...')) # pypilot is still python 2, so it have to be installed independent from openplotter-pypilot that is python 3
	try:
		subprocess.call(['cp', '-v', 'data/openplotter-pypilot-read', '/usr/bin'], cwd=currentdir+'/')
		subprocess.call(['chmod', '+x', '/usr/bin/openplotter-pypilot-read'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

if __name__ == '__main__':
	main()

