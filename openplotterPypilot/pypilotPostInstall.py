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
from .version import version

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

	print(_('Installing python packages...'))
	try:
		#add libatlas-base-dev apt package and tensorflow pip3 if support for tensorflow is added
		subprocess.call(['pip3', 'install', 'pywavefront', 'pyglet', 'gps', 'gevent-websocket', 'python-socketio'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))
	
	print(_('Compiling RTIMULib2...'))
	try:
		subprocess.call(['rm', '-f', 'master.zip'])
		subprocess.call(['rm', '-rf', 'RTIMULib2-master'])
		subprocess.call(['wget', 'https://github.com/openplotter/RTIMULib2/archive/master.zip'])
		subprocess.call(['unzip', 'master.zip'])
		subprocess.call(['rm', '-f', 'master.zip'])
		os.chdir('RTIMULib2-master/Linux/python')
		subprocess.call(['python3', 'setup.py', 'build'])
		subprocess.call(['python3', 'setup.py', 'install'])
		os.chdir('../../..')
		subprocess.call(['rm', '-rf', 'RTIMULib2-master'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Compiling Pypilot...'))
	try:
		subprocess.call(['rm', '-f', 'master.zip'])
		subprocess.call(['rm', '-rf', 'pypilot-master'])
		subprocess.call(['rm', '-rf', 'pypilot_data-master'])
		subprocess.call(['wget', 'https://github.com/openplotter/pypilot/archive/master.zip'])
		subprocess.call(['unzip', 'master.zip'])
		subprocess.call(['rm', '-f', 'master.zip'])
		subprocess.call(['wget', 'https://github.com/openplotter/pypilot_data/archive/master.zip'])
		subprocess.call(['unzip', 'master.zip'])
		subprocess.call(['rm', '-f', 'master.zip'])
		subprocess.call(['cp', '-rv', 'pypilot_data-master/.', 'pypilot-master'])
		os.chdir('pypilot-master')
		subprocess.call(['python3', 'setup.py', 'build'])
		subprocess.call(['python3', 'setup.py', 'install'])
		os.chdir('..')
		subprocess.call(['rm', '-rf', 'pypilot-master'])
		subprocess.call(['rm', '-rf', 'pypilot_data-master'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Creating config files...'))
	try:
		pypilotFolder = conf2.home+'/.pypilot'
		if not os.path.exists(pypilotFolder): os.mkdir(pypilotFolder)
		skConfFile = pypilotFolder+'/pypilot_client.conf'
		if not os.path.exists(skConfFile):
			fo = open(skConfFile, "w")
			fo.write( '{"host": "localhost"}')
			fo.close()
		subprocess.call(['chown', '-R', conf2.user, pypilotFolder])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Adding pypilot, pypilot_boatimu and openplotter-pypilot-read services...'))
	try:
		def writeservice(name, wanted, conflicts=False, args=''):
			tempname = '/tmp/'+name+'.service'
			fo = open(tempname, 'w')
			fo.write( '[Unit]\nDescription='+name+'\nDefaultDependencies=false\n')
			if conflicts:
				fo.write('Conflicts='+conflicts+'.service\n')
			fo.write('\n[Service]\nType=simple\nExecStart='+name+' '+args+'\nStandardOutput=null\nStandardError=null\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=2\n\n[Install]\nWantedBy='+wanted)
			fo.close()
			subprocess.call(['mv', '-f', tempname, '/etc/systemd/system'])

		writeservice('pypilot_boatimu', 'local-fs.target', 'pypilot', '-q')
		writeservice('pypilot', 'local-fs.target', 'pypilot_boatimu')
		writeservice('pypilot_web', 'local-fs.target', False, '8080')
		writeservice('openplotter-pypilot-read', 'multi-user.target')
		subprocess.call(['systemctl', 'daemon-reload'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Setting version...'))
	try:
		conf2.set('APPS', 'pypilot', version)
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))
	
if __name__ == '__main__':
	main()

