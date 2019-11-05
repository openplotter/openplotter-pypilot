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

import wx, os, webbrowser, subprocess, socket, RTIMU
import wx.richtext as rt
from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import platform
from .openplotter_pypilot_ui import openplotter_pypilotBase

class openplotter_pypilot(openplotter_pypilotBase):
    def __init__(self):
        super(openplotter_pypilot, self).__init__(None)
        self.conf = conf.Conf()
        self.conf_folder = self.conf.conf_folder
        self.platform = platform.Platform()
        self.currentdir = os.path.dirname(os.path.abspath(__file__))
        self.currentLanguage = self.conf.get('GENERAL', 'lang')
        self.language = language.Language(self.currentdir,'openplotter-pypilot',self.currentLanguage)

        self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        icon = wx.Icon(self.currentdir+"/data/openplotter-pypilot.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        font_statusBar = self.GetStatusBar().GetFont()
        font_statusBar.SetWeight(wx.BOLD)
        self.GetStatusBar().SetFont(font_statusBar)
        
        self.Centre()

        SETTINGS_FILE = "RTIMULib2"
        s = RTIMU.Settings(SETTINGS_FILE)
        imu = RTIMU.RTIMU(s)

        keys = {}
        with open(SETTINGS_FILE+'.ini', "r") as infile:
            for line in infile:
                for i in range(20):
                    key = '#   %d' % i
                    if key in line:
                        keys[i] = line[8:]
                        
                if 'IMUType=' in line:
                    tmp = line.split("=")
                    imunum = int(tmp[1].strip())
                    if imunum in keys:
                        imuname = keys[imunum]
                    else:
                        imuname = 'unknown: ' + imunum
                    self.stDetected.SetLabel(imuname)
                    break
#        subprocess.call(['rm', '-f', 'RTIMULib2'])

    def ShowStatusBar(self, w_msg, colour):
        self.GetStatusBar().SetForegroundColour(colour)
        self.SetStatusText(w_msg)

    def ShowStatusBarRED(self, w_msg):
        self.ShowStatusBar(w_msg, (130,0,0))

    def ShowStatusBarGREEN(self, w_msg):
        self.ShowStatusBar(w_msg, (0,130,0))

    def ShowStatusBarBLACK(self, w_msg):
        self.ShowStatusBar(w_msg, wx.BLACK) 

    def ShowStatusBarYELLOW(self, w_msg):
        self.ShowStatusBar(w_msg,(255,140,0)) 

    def OnToolHelp(self, event): 
        url = "/usr/share/openplotter-doc/pypilot/pypilot_app.html"
        webbrowser.open(url, new=2)

    def OnToolSettings(self, event): 
        subprocess.call(['pkill', '-f', 'openplotter-settings'])
        subprocess.Popen('openplotter-settings')
    def OnToolClient(self,e):
        subprocess.call(['pkill', '-f', 'signalk_client_wx'])
        subprocess.Popen('signalk_client_wx')

    def OnToolScope(self,e):
        subprocess.Popen('signalk_scope_wx')

    def OnToolControl(self,e):
        subprocess.call(['pkill', '-f', 'pypilot_control'])
        subprocess.Popen('pypilot_control')

    def OnOpenWebControl(self,e):
        webbrowser.open('http://localhost:%d' % self.sPort.GetValue(), new=2)
        
    def OnToolImu(self,e):
        self.notebook.ChangeSelection(0)

    def OnToolPypilot(self,e):
        self.notebook.ChangeSelection(1)

    def OnToolCalibration(self,e):
        subprocess.call(['pkill', '-f', 'pypilot_calibration'])
        subprocess.Popen('pypilot_calibration')

    def OnToolOK(self,e):
        exit(0)

    def OnMode(self,e):
        mode = self.cMode.GetStringSelection()
        self.conf.set('PYPILOT', 'mode', mode)
        subprocess.Popen([self.platform.admin, 'python3', self.currentdir+'/service.py', mode])

################################################################################

def main():
    app = wx.App()
    openplotter_pypilot().Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
