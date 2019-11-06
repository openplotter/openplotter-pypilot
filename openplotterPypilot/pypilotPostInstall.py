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
from openplotterSettings import platform

def call(command):
    os.system(command)

pt = platform.Platform()
def sudo(command):
    call(pt.admin + ' ' + command)

def main():
    conf2 = conf.Conf()
    currentdir = os.path.dirname(os.path.abspath(__file__))
    currentLanguage = conf2.get('GENERAL', 'lang')
    language.Language(currentdir,'openplotter-pypilot',currentLanguage)

    print(_('Removing incompatible packages...'))
    try:
        sudo('apt -y autoremove sense-hat')
        print(_('DONE'))
    except Exception as e: print(_('FAILED: ')+str(e))

    # instead these shouold be dependencies of the openplotter-pypilot debian package
    print(_('Installing packages'))
    packages = ['python3-serial libpython3-dev python3-numpy python3-scipy swig',
                'python3-pil python3-flask',
                'python3-opengl']
    try:
        for p in packages:
            sudo('apt install -y ' + p)
    except Exception as e: print(_('FAILED: ')+str(e))

    print(_('Installing python dependencies...'))
    sudo('pip3 install gps ujson pyudev pyglet pywavefront flask-socketio gevent-websocket')
    
    print(_('Compiling RTIMULib2 for python2 and python3...'))
    try:
        call('rm -f master.zip')
        call('rm -rf python-RTIMULib2-master')
        call('wget https://github.com/openplotter/python-RTIMULib2/archive/master.zip')
        call('unzip master.zip')
        call('rm -f master.zip')
        os.chdir('python-RTIMULib2-master')
        call('python setup.py build')
        sudo('python setup.py install')
        call('python3 setup.py build')
        sudo('python3 setup.py install')
        os.chdir('..')
        sudo('rm -rf python-RTIMULib2-master')
        print(_('DONE'))
    except Exception as e: print(_('FAILED: ')+str(e))

    print(_('Compiling Pypilot for python3...'))
    try:
        call('rm -f master.zip')
        call('rm -rf pypilot-master')
        call('rm -rf pypilot_data-master')
        call('wget https://github.com/pypilot/pypilot/archive/master.zip')
        call('unzip master.zip')
        call('rm -f master.zip')
        call('wget https://github.com/pypilot/pypilot_data/archive/master.zip')
        call('unzip master.zip')
        call('rm -f master.zip')
        call('cp -rv pypilot_data-master/. pypilot-master')
        os.chdir('pypilot-master')
        call('python3 setup.py build')
        sudo('python3 setup.py install')
        os.chdir('..')
        sudo('rm -rf pypilot-master')
        call('rm -rf pypilot_data-master')
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
        call('chown -R ' + conf2.user + ' ' + pypilotFolder)
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
            fo.write('\n[Service]\nType=simple\nExecStart='+name+' '+args+'\nStandardOutput=syslog\nStandardError=syslog\nWorkingDirectory='+pypilotFolder+'\nUser='+conf2.user+'\nRestart=always\nRestartSec=2\n\n[Install]\nWantedBy='+wanted)
            fo.close()
            sudo('mv -f ' + tempname + ' /etc/systemd/system')

        writeservice('pypilot_boatimu', 'local-fs.target', 'pypilot', '-q')
        writeservice('pypilot', 'local-fs.target', 'pypilot_boatimu')
        writeservice('pypilot_lcd', 'local-fs.target')
        writeservice('pypilot_webapp', 'local-fs.target', False, '8000')
        writeservice('openplotter-pypilot-read', 'multi-user.target')
        sudo('systemctl daemon-reload')
        print(_('DONE'))
    except Exception as e: print(_('FAILED: ')+str(e))

        # read script is part of openplotter-pypilot
    print(_('Copying openplotter-pypilot-read script manually...'))
    try:
        call('chmod +x data/openplotter-pypilot-read')
        sudo('cp -v data/openplotter-pypilot-read /usr/bin')
        print(_('DONE'))
    except Exception as e: print(_('FAILED: ')+str(e))

if __name__ == '__main__':
    main()

