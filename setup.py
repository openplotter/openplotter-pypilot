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

from setuptools import setup
from openplotterMyapp import version

setup (
	name = 'openplotterMyapp',
	version = version.version,
	description = 'This is a template to help create apps for OpenPlotter',
	license = 'GPLv3',
	author="xxxx",
	author_email='xxxx@xxxx.com',
	url='https://github.com/xxxx/openplotter-myapp',
	packages=['openplotterMyapp'],
	classifiers = ['Natural Language :: English',
	'Operating System :: POSIX :: Linux',
	'Programming Language :: Python :: 3'],
	include_package_data=True,
	entry_points={'console_scripts': ['openplotter-myapp=openplotterMyapp.openplotterMyapp:main','openplotter-myapp-read=openplotterMyapp.openplotterMyappRead:main','myappPostInstall=openplotterMyapp.myappPostInstall:main','myappPreUninstall=openplotterMyapp.myappPreUninstall:main']},
	# entry_points: creating entry points you will be able to run these python scripts from everywhere.
		# openplotter-myapp = This is the GUI of your app
		# openplotter-myapp-read = You will use this file to be ran at startup as a service when needed using "sudo systemctl enable openplotter-myapp-read" in your code. See myappPostInstall file to see how to create services. If your script is a GUI script you need to start it in startup.py and not as a service.
		# myappPostInstall = This file will be run just after package installation and it should contain any extra task to do like installing pip packages, creating services... If you are not using openplotter-settings to install this app (as for development), you will need to run myappPostInstall manually. 
		# myappPreUninstall = This file will be run just before package uninstall. Here you should revert all changes in myappPostInstall.
	scripts=['bin/myScript'],
	# scripts: if you need to create entry points for python and non-python scripts like shell scripts you can use this.
		# myScript = a shell script
		# myappPostInstall = if your myappPostInstall file has to be a non-python script, put it in "scripts" and not in "entry_points".
		# myappPreUninstall = if your myappPreUninstall file has to be a non-python script, put it in "scripts" and not in "entry_points".
	data_files=[('share/applications', ['openplotterMyapp/data/openplotter-myapp.desktop']),('share/pixmaps', ['openplotterMyapp/data/openplotter-myapp.png']),],
	# data_files = Add files to the host system. This will work only when installed as debian package, not as a python package.
	)
