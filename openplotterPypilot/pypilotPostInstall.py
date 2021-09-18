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

try:
    from .version import version
except:
    from version import version


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
        os.chdir('/tmp')
        subprocess.call(['sudo', 'rm', '-rf', 'pypilot'])
        subprocess.call(['git', 'clone', '--depth', '1', 'https://github.com/pypilot/pypilot'])
        os.chdir('pypilot')
        subprocess.call(['sudo', 'python3', 'setup.py', 'install'])

        print(_('installing debian service scripts'))
        os.system('sudo cp -rv scripts/debian/etc/systemd /etc')
        
        subprocess.call(['sudo', 'rm', '-rf', 'pypilot'])
        print(_('DONE'))
    except Exception as e: print(_('FAILED: ')+str(e))
    
    ''' Do we need to create these??'''
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
        subprocess.call(['chown', '-R', conf2.user, pypilotFolder])
        print(_('DONE'))
    except Exception as e:
        print(_('FAILED: ')+str(e))
    
    print(_('Setting version...'))
    try:
        conf2.set('APPS', 'pypilot', version)
        print(_('DONE'))
    except Exception as e: print(_('FAILED: ')+str(e))
    
if __name__ == '__main__':
    main()
            
            
