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
	        os.system('sudo cp -rv scripts/debian/etc/systemd /etc')
		subprocess.call(['systemctl', 'daemon-reload'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Creating config files...'))
	try:
		pypilotFolder = conf2.home+'/.pypilot'
		if not os.path.exists(pypilotFolder):
			os.mkdir(pypilotFolder)
		skConfFile = pypilotFolder+'/pypilot_client.conf'
		if not os.path.exists(skConfFile):
			fo = open(skConfFile, "w")
			fo.write( '{"host": "localhost"}')
			fo.close()
		serialPorts = pypilotFolder+'/serial_ports'
		if not os.path.exists(serialPorts):
			fo = open(skConfFile, "w")
			fo.write('/dev/ttyAMA0\n')
			fo.close()
		subprocess.call(['chown', '-R', conf2.user, pypilotFolder])
		print(_('DONE'))
	except Exception as e:
		print(_('FAILED: ')+str(e))
        
	print(_('Checking access to Signal K server...'))
	try:
		from openplotterSignalkInstaller import connections
		skConnections = connections.Connections('PYPILOT')
		result = skConnections.checkConnection()
		if result[1]: print(result[1])
		else: print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Setting version...'))
	try:
		conf2.set('APPS', 'pypilot', version)
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))
    
if __name__ == '__main__':
	main()
