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

import os
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
		conf2.set('PYPILOT', 'pypilot_boatimu', '0')
		conf2.set('PYPILOT', 'pypilot', '0')
		conf2.set('PYPILOT', 'pypilot_hat', '0')
		conf2.set('PYPILOT', 'pypilot_web', '0')
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))

	print(_('Removing version...'))
	try:
		conf2.set('APPS', 'pypilot', '')
		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))
	
if __name__ == '__main__':
	main()
