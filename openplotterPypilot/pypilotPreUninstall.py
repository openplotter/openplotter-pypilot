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

def main():
	conf2 = conf.Conf()
	currentdir = os.path.dirname(os.path.abspath(__file__))
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-pypilot',currentLanguage)

	print(_('Removing Pypilot...'))
	try:
		os.system('xargs rm -rf < '+conf2.home+'/.pypilot/install.txt')
		os.system('rm -rf '+conf2.home+'/.pypilot')
		subprocess.call(['systemctl', 'disable', 'pypilot'])
		subprocess.call(['systemctl', 'disable', 'pypilot_boatimu'])
		subprocess.call(['systemctl', 'disable', 'openplotter-pypilot-read'])
		subprocess.call(['systemctl', 'disable', 'pypilot_web'])
		subprocess.call(['systemctl', 'disable', 'pypilot_hat'])
		subprocess.call(['systemctl', 'stop', 'pypilot'])
		subprocess.call(['systemctl', 'stop', 'pypilot_boatimu'])
		subprocess.call(['systemctl', 'stop', 'openplotter-pypilot-read'])
		subprocess.call(['systemctl', 'stop', 'pypilot_web'])
		subprocess.call(['systemctl', 'stop', 'pypilot_hat'])
		os.system('rm -f /etc/systemd/system/pypilot.service')
		os.system('rm -f /etc/systemd/system/pypilot_boatimu.service')
		os.system('rm -f /etc/systemd/system/openplotter-pypilot-read.service')
		os.system('rm -f /etc/systemd/system/pypilot_hat.service')
		os.system('rm -f /etc/systemd/system/pypilot_web.service')
		subprocess.call(['systemctl', 'daemon-reload'])
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Removing version...'))
	try:
		conf2.set('APPS', 'pypilot', '')
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))
	
if __name__ == '__main__':
	main()
