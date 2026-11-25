#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
# Copyright (C) 2022 by Sean D'Epagnier <https://github.com/pypilot/openplotter-pypilot>
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
from openplotterSignalkInstaller import connections
try: from .version import version
except: from version import version

def main():
	conf2 = conf.Conf()
	currentdir = os.path.dirname(os.path.abspath(__file__))
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-pypilot',currentLanguage)
	
	print(_('Removing incompatible packages...'))
	try:
		subprocess.call(['apt', '-y', 'autoremove', 'sense-hat'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Installing Pypilot...'))
	try:
		pypilotFolder = conf2.home+'/.pypilot'
		installfile = pypilotFolder+'/install.txt'
		if not os.path.exists(pypilotFolder): os.mkdir(pypilotFolder)
		skConfFile = pypilotFolder+'/pypilot_client.conf'
		if not os.path.exists(skConfFile):
			fo = open(skConfFile, "w")
			fo.write( '{"host": "localhost"}')
			fo.close()
		serialPorts = pypilotFolder+'/serial_ports'
		if not os.path.exists(serialPorts):
			fo = open(serialPorts, "w")
			fo.write('')
			fo.close()
		os.system('rm -f '+installfile)
		os.chdir('/tmp')
		os.system('rm -rf pypilot')
		os.system('git clone --depth 1 https://github.com/pypilot/pypilot')
		os.chdir('pypilot')
		os.system('python3 setup.py install --record '+installfile)
		os.system('chown -R '+conf2.user+' '+pypilotFolder)
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Creating services...'))
	try:
		fo = open('/etc/systemd/system/check-pypilot-security.service', "w")
		fo.write( '[Unit]\nBefore=pypilot.service\nBefore=pypilot_boatimu.service\nBefore=pypilot_hat.service\nBefore=pypilot_web.service\n[Service]\nExecStart=pypilot-check-security\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\n[Install]\nWantedBy=local-fs.target\n')
		fo.close()
		fo = open('/etc/systemd/system/pypilot.service', 'w')
		fo.write( '[Unit]\nDescription=pypilot\nAfter=check-pypilot-security.service\nDefaultDependencies=false\nConflicts=pypilot_boatimu.service\n\n')
		fo.write('[Service]\nType=simple\nExecStart=/usr/local/bin/pypilot\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=2\n\n')
		fo.write('[Install]\nWantedBy=local-fs.target')
		fo.close()
		fo = open('/etc/systemd/system/pypilot_boatimu.service', 'w')
		fo.write( '[Unit]\nDescription=pypilot boatimu\nAfter=check-pypilot-security.service\nDefaultDependencies=false\nConflicts=pypilot.service\n\n')
		fo.write('[Service]\nType=simple\nExecStart=pypilot_boatimu -q\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=2\n\n')
		fo.write('[Install]\nWantedBy=local-fs.target')
		fo.close()
		fo = open('/etc/systemd/system/pypilot_hat.service', 'w')
		fo.write( '[Unit]\nDescription=pypilot hat\nAfter=check-pypilot-security.service\nDefaultDependencies=false\n\n')
		fo.write('[Service]\nType=simple\nExecStart=pypilot_hat\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=3\n\n')
		fo.write('[Install]\nWantedBy=local-fs.target')
		fo.close()
		fo = open('/etc/systemd/system/pypilot_web.service', 'w')
		fo.write( '[Unit]\nDescription=pypilot web\nAfter=check-pypilot-security.service\nDefaultDependencies=false\n\n')
		fo.write('[Service]\nType=simple\nExecStart=pypilot_web 8000\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=3\n\n')
		fo.write('[Install]\nWantedBy=local-fs.target')
		fo.close()
		fo = open('/etc/systemd/system/openplotter-pypilot-read.service', 'w')
		fo.write( '[Unit]\nDescription=openplotter-pypilot-read\nDefaultDependencies=false\nConflicts=pypilot.service\n\n')
		fo.write('[Service]\nType=simple\nExecStart=openplotter-pypilot-read\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=2\n\n')
		fo.write('[Install]\nWantedBy=local-fs.target')
		fo.close()
		subprocess.call(['systemctl', 'daemon-reload'])
		subprocess.call(['systemctl', 'enable', 'check-pypilot-security.service'])
		subprocess.call(['systemctl', 'start', 'check-pypilot-security.service'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Setting version...'))
	try:
		conf2.set('APPS', 'pypilot', version)
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))
    
if __name__ == '__main__':
	main()
