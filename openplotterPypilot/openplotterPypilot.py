#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
# Copyright (C) 2021 by Sean D'Epagnier <https://github.com/pypilot/openplotter-pypilot>
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



import wx, os, webbrowser, subprocess, sys, time, ujson
from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import ports
from openplotterSettings import platform
from openplotterSettings import selectConnections

try:
	import RTIMU
except:
	RTIMU = None

try:
    from .version import version
except:
    from version import version

try:
    from .pypilotOpenplotter_ui import pypilotPanelBase
except:
    from pypilotOpenplotter_ui import pypilotPanelBase


class pypilotPanel(pypilotPanelBase):
    def __init__(self, parent):
        super(pypilotPanel, self).__init__(parent)
        self.conf = conf.Conf()
        self.platform = self.GetParent().platform

        try:
            from pypilot.version import strversion
            self.version.SetLabel(strversion)
        except Exception as e:
            self.version.SetLabel(str(e))
            
        # look for eeprom of hat for hints as to what hardware is available
        configfile = '/proc/device-tree/hat/custom_0'
        config = None
        try:
            with open(configfile) as f:
                config = ujson.loads(f.read())
            self.hardware.SetLabel(str(config['arduino']['hardware']))
            if not self.active('pypilot_hat'):
                wx.MessageBox(_('Detected pypilot hat, but the service is not enabled.\nEnable the hat service touse the lcd display and remote controls'), _('warning'), wx.OK | wx.ICON_WARNING)

        except Exception as e:
            self.hardware.SetLabel(_("no pypilot hat detected"))

        self.WarnHardwareSerial()
            
        if self.active('pypilot'):
            self.services.SetSelection(2)
        elif self.active('boatimu'):
            self.services.SetSelection(1)

        if self.active('pypilot_web'):
            self.WebControl.SetValue(True)

        if self.active('pypilot_hat'):
            self.HatControl.SetValue(True)

        try:
            subprocess.check_output(['i2cdetect', '-y', '1']).decode(sys.stdin.encoding)
        except:
            self.GetParent().ShowStatusBarRED(_('I2C is disabled. Please enable I2C interface in Preferences -> Raspberry Pi configuration -> Interfaces'))
            self.imuDetected.SetLabel(_('Failed'))

        if RTIMU:
            self.imuDetected.SetLabel(_('none'))
            SETTINGS_FILE = "RTIMULibTemp"
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
                            imuname = _('unknown: ') + imunum
                        imuname = imuname.replace('\n', '')
                        self.imuDetected.SetLabel(imuname)
                        break
            subprocess.call(['rm', '-f', 'RTIMULibTemp.ini'])

        self.relistSerial()

    def active(self, name):
        sys.stdout.write('service ' + name + ': ')
        sys.stdout.flush()
        return not os.system('systemctl is-active ' + name)

    def relistSerial(self):
        self.listSerial.Clear()
        try:
            path = self.conf.home + '/.pypilot/serial_ports'
            with open(path, 'r') as f:
                for line in f:
                    line = line.replace('\n', '')
                    line = line.strip()
                    self.listSerial.Append(line)
                    #self.listSerial.SetItemBackgroundColour(self.listSerial.GetItemCount()-1,(102,205,170))
        except:
            pass

            
    def WarnHardwareSerial(self):
        # test if hardware serial is enabled
        if os.path.realpath('/dev/serial0') != '/dev/ttyAMA0':
            wx.MessageBox(_('hardware serial must be enabled for motor controller communication'), _('warning'), wx.OK | wx.ICON_WARNING)
            self.hardwareSerial.SetLabel(_('warning: no hardware serial'))

        self.hardwareSerial.SetLabel(_('hardware serial detected'))

        # test that /dev/ttyAMA0 is in ~/.pypilot/serial_ports
        path = self.conf.home + '/.pypilot/serial_ports'
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    line = line.replace('\n', '')
                    line = line.strip()
                    if os.path.realpath(line) == '/dev/ttyAMA0':
                        break
                else:
                    wx.MessageBox(_('the hardware serial port for the motor /dev/ttyAMA0 should be added to the list of serial ports pypilot manages'), _('warning'), wx.OK | wx.ICON_WARNING)            

    def service(self, command):
        subprocess.call([self.platform.admin, 'python3', os.path.dirname(__file__)+'/service.py', command])

    def onServices( self, event=None ):
        services = self.services.GetSelection()

        self.GetParent().ShowStatusBarYELLOW(_('Applying changes ...'))
        if services == 0:
            self.service('disable')
        elif services == 1:
            self.service('boatimu')
        elif services == 2:
            self.service('pypilot')
            self.WarnHardwareSerial()
            
        self.relistSerial()
        self.GetParent().ShowStatusBarGREEN(_('Changes applied'))
            
    def onWebControl( self, event ):
        if self.WebControl.GetValue():
            self.service('enableWeb')
        else:
            self.service('disableWeb')

    def onHatControl( self, event ):
        if self.HatControl.GetValue():
            self.service('enableHat')
        else:
            self.service('disableHat')

    def onOpenBrowser(self, e): 
        url = "http://localhost:8080"
        webbrowser.open(url, new=2)

    def onConfigureHat(self, e):
        url = "http://localhost:33333"
        webbrowser.open(url, new=2)

    def onHardwareSerial(self, e):
        subprocess.call([self.platform.admin, 'python3', os.path.dirname(__file__)+'/hardwareserial.py'])
        wx.MessageBox(_('must reboot to update changes to hardware serial'), _('reboot'), wx.OK)

    def onAddSerial(self, e): 
        dlg = selectConnections.AddPort('', True, 'auto', False)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            device = dlg.port.GetValue()
            if not device:
                self.GetParent().ShowStatusBarRED(_('You have to select a device'))
                dlg.Destroy()
                return
            for i in range(self.listSerial.GetCount()):
                if device == self.listSerial.GetString(i):
                    self.ShowStatusBarRED(_('This device already exists'))
                    dlg.Destroy()
                    return
            self.GetParent().ShowStatusBarYELLOW(_('Applying changes ...'))
            path = self.conf.home + '/.pypilot/serial_ports'
            with open(path, 'a') as file:
                file.write(device + '\n')

            self.onServices()
            self.relistSerial()

        dlg.Destroy()

    def onRemoveSerial(self, e): 
        index = self.listSerial.GetSelection()
        if index == -1: return
        device = self.listSerial.GetString(index)

        try:
            new = ''
            path = self.conf.home + '/.pypilot/serial_ports'
            with open(path, 'r') as f:
                for line in f:
                    line = line.replace('\n', '')
                    line = line.strip()
                    if device != line: new = new+line+'\n'
            with open(path, 'w') as f:
                f.write(new)
        except: pass


        #nmeaXdevice
        path = self.conf.home + '/.pypilot/'
        tmp = os.listdir(path)
        for i in tmp:
            if i[:4] == 'nmea' and i[-6:] == 'device':
                subprocess.call(['rm', '-f', path+i])

        self.onServices()
        self.relistSerial()

    def onConsoleTimer(self, event):
        if self.installProcess.poll() != None:
            self.installConsoleTimer.Stop()
            self.bReinstall.Enable(True)

            self.installConsole.SetInsertionPoint(-1)
            self.installConsole.ShowPosition(self.installConsole.GetLastPosition())
            self.installConsole.Refresh()
            self.installConsole.Update()
            return
            
        try:
            for f in [self.installProcess.stdout, self.installProcess.stderr]:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    self.installConsole.WriteText(line)

        except Exception as e:
            print('exception', e)
        self.installConsole.SetInsertionPoint(-1)
        self.installConsole.ShowPosition(self.installConsole.GetLastPosition())
        self.installConsole.Refresh()
        self.installConsole.Update()

    def onReinstall(self, event):
        self.installConsole.Clear()
        self.installConsoleTimer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.onConsoleTimer, id=wx.ID_ANY)
        self.bReinstall.Enable(False)

        try:
            self.installProcess = subprocess.Popen(['python3', os.path.dirname(__file__)+'/pypilotPostInstall.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            import fcntl
            for f in [self.installProcess.stdout, self.installProcess.stderr]:
                fd = f.fileno()
                fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)

            self.installConsoleTimer.Start(500, False)
        except Exception as e:
            print('exception', e)
            t = self.installConsole.GetLabel()
            self.installConsole.SetLabel(t + str(e) + '\n')
            self.installProcess.kill()
        
class MyFrame(wx.Frame):
    def __init__(self):
        self.conf = conf.Conf()

        self.platform = platform.Platform()
        self.currentdir = os.path.dirname(os.path.abspath(__file__))
        self.currentLanguage = self.conf.get('GENERAL', 'lang')
        self.language = language.Language(self.currentdir,'openplotter-pypilot',self.currentLanguage)

        wx.Frame.__init__(self, None, title='Pypilot'+' '+version, size=(800,444))
        self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        icon = wx.Icon(self.currentdir+"/data/openplotter-pypilot.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.CreateStatusBar()
        font_statusBar = self.GetStatusBar().GetFont()
        font_statusBar.SetWeight(wx.BOLD)
        self.GetStatusBar().SetFont(font_statusBar)
        
        self.toolbar1 = wx.ToolBar(self, style=wx.TB_TEXT)
        toolHelp = self.toolbar1.AddTool(101, _('Help'), wx.Bitmap(self.currentdir+"/data/help.png"))
        self.Bind(wx.EVT_TOOL, self.OnToolHelp, toolHelp)
        if not self.platform.isInstalled('openplotter-doc'): self.toolbar1.EnableTool(101,False)
        toolSettings = self.toolbar1.AddTool(102, _('Settings'), wx.Bitmap(self.currentdir+"/data/settings.png"))
        self.Bind(wx.EVT_TOOL, self.OnToolSettings, toolSettings)
        self.toolbar1.AddSeparator()
                
        toolControl = self.toolbar1.AddTool(201, _('Control'), wx.Bitmap(self.currentdir+"/data/control.png"))
        self.Bind(wx.EVT_TOOL, self.onToolControl, toolControl)
                
        toolCalibration= self.toolbar1.AddTool(104, _('Calibration'), wx.Bitmap(self.currentdir+"/data/calibration.png"))
        self.Bind(wx.EVT_TOOL, self.OnToolCalibration, toolCalibration)
        toolScope= self.toolbar1.AddTool(105, _('Scope'), wx.Bitmap(self.currentdir+"/data/scope.png"))
        self.Bind(wx.EVT_TOOL, self.OnToolScope, toolScope)
        toolClient= self.toolbar1.AddTool(106, _('Client'), wx.Bitmap(self.currentdir+"/data/client.png"))
        self.Bind(wx.EVT_TOOL, self.OnToolClient, toolClient)

        fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer1.AddGrowableCol( 0 )
        fgSizer1.AddGrowableRow( 1 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self.SetSizer(fgSizer1)

        self.pypilot = pypilotPanel(self)
        fgSizer1.Add( self.toolbar1, 1, wx.EXPAND |wx.ALL, 5 )
        fgSizer1.Add( self.pypilot, 1, wx.EXPAND |wx.ALL, 5 )

        maxi = self.conf.get('GENERAL', '`maximize')
        if maxi == '1': self.Maximize()

       
        self.Centre()

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

    def onTabChange(self, event):
        try:
            self.SetStatusText('')
        except:
            pass

    def OnToolHelp(self, event): 
        url = "/usr/share/openplotter-doc/pypilot/pypilot_app.html"
        webbrowser.open(url, new=2)

    def run(self, cmd):
        subprocess.call(['pkill', '-f', cmd])
        subprocess.Popen(cmd)

    def OnToolSettings(self, event=0): 
        self.run('openplotter-settings')

    def OnToolCalibration(self,e):
        self.run('pypilot_calibration')

    def OnToolScope(self,e):
        self.run('pypilot_scope')

    def OnToolClient(self,e):
        self.run('pypilot_client_wx')
                                                                                                 
    def onToolControl(self,e):
        subprocess.call(['pkill', '-f', 'pypilot_control'])
        subprocess.Popen(['pypilot_control', 'localhost'])


################################################################################

def main():
    try:
        platform2 = platform.Platform()
        if not platform2.postInstall(version,'pypilot'):
            subprocess.Popen(['openplotterPostInstall', platform2.admin+' pypilotPostInstall'])
            return
    except: pass

    app = wx.App()
    MyFrame().Show()
    time.sleep(1)
    app.MainLoop()

if __name__ == '__main__':
    main()
    
