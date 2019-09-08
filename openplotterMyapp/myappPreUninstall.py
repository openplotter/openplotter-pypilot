#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2015 by xxxx <https://github.com/xxxx/openplotter-myapp>
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
	# This file will be ran as sudo. Do here whatever you need to remove files and programs before app uninstall.
	conf2 = conf.Conf()
	currentdir = os.path.dirname(__file__)
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-myapp',currentLanguage)

	# here we remove the services
	print(_('Removing openplotter-read-myapp service...'))
	try:
		subprocess.call(['systemctl', 'disable', 'openplotter-myapp-read'])
		subprocess.call(['systemctl', 'stop', 'openplotter-myapp-read'])
		subprocess.call(['rm', '-f', '/etc/systemd/system/openplotter-myapp-read.service'])
		subprocess.call(['systemctl', 'daemon-reload'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))


if __name__ == '__main__':
	main()