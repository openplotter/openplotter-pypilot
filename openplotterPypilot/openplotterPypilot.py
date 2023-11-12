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

import wx, os, webbrowser, subprocess, sys, time, ujson
from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import ports
from openplotterSettings import platform
from openplotterSettings import selectConnections
from openplotterSignalkInstaller import connections

try: import RTIMU
except: RTIMU = None

try: from .version import version
except: from version import version

class pypilotFrame(wx.Frame):
	def __init__(self):
		self.conf = conf.Conf()
		if self.conf.get('GENERAL', 'debug') == 'yes': self.debug = True
		else: self.debug = False
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
		aproveSK = self.toolbar1.AddTool(107, _('Approve'), wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.onAproveSK, aproveSK)
		connectionSK = self.toolbar1.AddTool(108, _('Reconnect'), wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.onConnectionSK, connectionSK)
		self.toolbar1.AddSeparator()
		toolRefresh = self.toolbar1.AddTool(103, _('Refresh'), wx.Bitmap(self.currentdir+"/data/refresh.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolRefresh, toolRefresh)

		self.toolbar2 = wx.ToolBar(self, style=wx.TB_TEXT)
		toolControl = self.toolbar2.AddTool(201, _('Control'), wx.Bitmap(self.currentdir+"/data/control.png"))
		self.Bind(wx.EVT_TOOL, self.onToolControl, toolControl)
		toolWebControl = self.toolbar2.AddTool(205, _('Web Control'), wx.Bitmap(self.currentdir+"/data/open.png"))
		self.Bind(wx.EVT_TOOL, self.onToolWebControl, toolWebControl)
		self.toolbar2.AddSeparator()
		toolCalibration= self.toolbar2.AddTool(202, _('Calibration'), wx.Bitmap(self.currentdir+"/data/calibration.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCalibration, toolCalibration)
		self.toolbar2.AddSeparator()
		toolScope= self.toolbar2.AddTool(203, _('Scope'), wx.Bitmap(self.currentdir+"/data/scope.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolScope, toolScope)
		toolClient= self.toolbar2.AddTool(204, _('Client'), wx.Bitmap(self.currentdir+"/data/client.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolClient, toolClient)

		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.services = wx.Panel(self.notebook)
		self.serial = wx.Panel(self.notebook)
		self.notebook.AddPage(self.services, _('Services'))
		self.notebook.AddPage(self.serial, _('Serial'))
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/process.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/serial.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.toolbar2, 0, wx.EXPAND)
		#vbox.Add(self.pypilot, 1, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		maxi = self.conf.get('GENERAL', 'maximize')
		if maxi == '1': self.Maximize()
	   
		self.Centre()
		
		self.pageServices()
		self.pageSerial()
		self.onRead()

	def OnToolRefresh(self, event):
		self.onRead()
		
	def onRead(self):
		self.SetStatusText('')

		def enable_tools(v):
			self.systemd_services.SetSelection(v)
			if v == 2: self.toolbar2.EnableTool(201,True)
			else: self.toolbar2.EnableTool(201,False)
			self.toolbar2.EnableTool(202,v)
			self.toolbar2.EnableTool(203,v)
			self.toolbar2.EnableTool(204,v)

		#SK connection
		self.toolbar1.EnableTool(107,False)
		skConnections = connections.Connections('PYPILOT')
		result = skConnections.checkConnection()
		if result[0] == 'pending':
			self.toolbar1.EnableTool(107,True)
			self.ShowStatusBarYELLOW(result[1]+_(' Press "Approve" and then "Refresh".'))
			if self.active('pypilot') or self.active('pypilot_boatimu'): 
				#self.service('disable')
				enable_tools(0)
		elif result[0] == 'error':
			self.ShowStatusBarRED(result[1]+_(' Try "Reconnect".'))
			if self.active('pypilot') or self.active('pypilot_boatimu'): 
				#self.service('disable')
				enable_tools(0)
		elif result[0] == 'repeat':
			self.ShowStatusBarYELLOW(result[1]+_(' Press "Refresh".'))
			if self.active('pypilot') or self.active('pypilot_boatimu'): 
				#self.service('disable')
				enable_tools(0)
		elif result[0] == 'permissions':
			self.ShowStatusBarYELLOW(result[1])
			if self.active('pypilot') or self.active('pypilot_boatimu'): 
				#self.service('disable')
				enable_tools(0)
		elif result[0] == 'approved' or result[0] == 'validated':
			if result[1]: self.ShowStatusBarGREEN(result[1])
			token = self.conf.get('PYPILOT', 'token')
			try:
				file = open(self.conf.home+'/.pypilot/signalk-token', 'r')
				token2 = file.read()
				token2 = token2.rstrip()
				file.close()
				if token != token2:
					file = open(self.conf.home+'/.pypilot/signalk-token', 'w')
					file.write(token)
					file.close()
					if self.active('pypilot'): self.service('pypilot')
					elif self.active('pypilot_boatimu'): self.service('boatimu')
			except:
				file = open(self.conf.home+'/.pypilot/signalk-token', 'w')
				file.write(token)
				file.close()
				if self.active('pypilot'): self.service('pypilot')
				elif self.active('pypilot_boatimu'): self.service('boatimu')

		#pypilot version
		try:
			from pypilot.version import strversion
			self.pypilotVersion.SetLabel(_('pypilot version:')+' '+strversion)
		except Exception as e:
			self.pypilotVersion.SetLabel(_('pypilot version:')+' '+str(e))

		#check services
		if self.active('pypilot'): enable_tools(2)
		elif self.active('pypilot_boatimu'): enable_tools(1)
		else: enable_tools(0)

		self.WebControl.SetValue(self.active('pypilot_web'))
		self.HatControl.SetValue(self.active('pypilot_hat'))
		if self.WebControl.GetValue(): self.toolbar2.EnableTool(205,True)
		else: self.toolbar2.EnableTool(205,False)
		if self.HatControl.GetValue(): self.HatControlConfig.Enable()
		else: self.HatControlConfig.Disable()

		#IMU
		label = _('Detected IMU:')+' '
		try:
			subprocess.check_output(['i2cdetect', '-y', '1']).decode(sys.stdin.encoding)
		except:
			self.ShowStatusBarRED(_('I2C is disabled. Please enable I2C interface in Preferences -> Raspberry Pi configuration -> Interfaces'))
			self.imuDetected.SetLabel(label+_('Failed'))
		else:
			SETTINGS_FILE = "RTIMULibTemp"
			s = RTIMU.Settings(SETTINGS_FILE)
			imu = RTIMU.RTIMU(s)
			imuname = imu.IMUName()

			if imuname == 'Null IMU':
				imuname = _('None')
			self.imuDetected.SetLabel(label+imuname)
			subprocess.call(['rm', '-f', 'RTIMULibTemp.ini'])

		#hardware
		label = _('Detected Hardware:')+' '
		configfile = '/proc/device-tree/hat/custom_0'
		config = None
		try:
			with open(configfile) as f:
				config = ujson.loads(f.read())
			self.hardware.SetLabel(label+str(config['arduino']['hardware']))
			if not self.active('pypilot_hat'):
				self.ShowStatusBarRED(_('Detected pypilot HAT, but the service is not enabled'))
		except Exception as e:
			self.hardware.SetLabel(label+_("no pypilot HAT detected"))

		#serial
		self.relistSerial()

		if self.active('pypilot'):
			path = self.conf.home + '/.pypilot/serial_ports'
			exists = False
			if os.path.exists(path):
				with open(path, 'r') as f:
					for line in f:
						line = line.replace('\n', '')
						line = line.strip()
						if '/dev/ttyAMA' in os.path.realpath(line) : exists = True
			if not exists:
				wx.MessageBox(_('At least one UART interface for the pypilot controller must be added to the list of serial devices'), _('warning'), wx.OK | wx.ICON_WARNING)

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
		try:self.SetStatusText('')
		except:pass

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

	def onToolWebControl(self,e): 
		url = "http://localhost:8000"
		webbrowser.open(url, new=2)

	def onAproveSK(self, e):
		if self.platform.skPort: 
			url = self.platform.http+'localhost:'+self.platform.skPort+'/admin/#/security/access/requests'
			webbrowser.open(url, new=2)

	def onConnectionSK(self, e):
		self.conf.set('PYPILOT', 'href', '')
		self.conf.set('PYPILOT', 'token', '')
		self.onRead()

	def pageServices(self):
		self.systemd_services = wx.Choice(self.services, choices = (_("Disable"),_("Enable IMU Only"),_("Enable Autopilot")), style=wx.CB_READONLY)
		self.systemd_services.Bind(wx.EVT_CHOICE, self.onServices)
		self.WebControl = wx.CheckBox(self.services, label=_('Enable Web Control'))
		self.WebControl.Bind(wx.EVT_CHECKBOX, self.onWebControl)
		self.HatControl = wx.CheckBox(self.services, label=_('Enable HAT Control'))
		self.HatControl.Bind(wx.EVT_CHECKBOX, self.onHatControl)
		self.HatControlConfig = wx.Button(self.services, label=_('Configure'))
		self.HatControlConfig.Bind(wx.EVT_BUTTON, self.onConfigureHat)
		self.pypilotVersion = wx.StaticText(self.services, label='')
		self.imuDetected = wx.StaticText(self.services, label='')
		self.hardware = wx.StaticText(self.services, label='')

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.systemd_services, 0, wx.ALL, 7)
		vbox.Add(self.WebControl, 0, wx.ALL, 7)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.HatControl, 0, wx.ALL, 7)
		hbox.Add(self.HatControlConfig, 0, wx.ALL, 7)
		vbox.Add(hbox)
		
		vbox.Add(self.pypilotVersion, 0, wx.ALL, 5)
		vbox.Add(self.imuDetected, 0, wx.ALL, 5)
		vbox.Add(self.hardware, 0, wx.ALL, 5)
		
		self.services.SetSizer(vbox)

	def active(self, name):
		return not os.system('systemctl is-active ' + name)

	def onWebControl(self,e):
		if self.WebControl.GetValue():
			self.service('enableWeb')
		else:
			self.service('disableWeb')
		self.onRead()

	def onHatControl(self,e):
		if self.HatControl.GetValue():
			self.service('enableHat')
		else:
			self.service('disableHat')
		self.onRead()

	def onConfigureHat(self, e):
		url = "http://localhost:33333"
		webbrowser.open(url, new=2)

	def service(self, command):
		subprocess.call([self.platform.admin, 'python3', os.path.dirname(__file__)+'/service.py', command])

	def onServices( self, event=None ):
		mode = self.systemd_services.GetSelection()
		self.ShowStatusBarYELLOW(_('Applying changes ...'))
		if mode == 0: self.service('disable')
		elif mode == 1: self.service('boatimu')
		elif mode == 2: self.service('pypilot')
		self.onRead()

	############################################################################

	def pageSerial(self):
		self.listSerial = wx.ListBox(self.serial, choices=[])
		self.toolbar3 = wx.ToolBar(self.serial, style=wx.TB_VERTICAL)
		self.toolbar3.AddSeparator()
		addSerial = self.toolbar3.AddTool(301, _('Add'), wx.Bitmap(self.currentdir+"/data/add.png"))
		self.Bind(wx.EVT_TOOL, self.onAddSerial, addSerial)
		self.toolbar3.AddSeparator()
		removeSerial = self.toolbar3.AddTool(302, _('Delete'), wx.Bitmap(self.currentdir+"/data/cancel.png"))
		self.Bind(wx.EVT_TOOL, self.onRemoveSerial, removeSerial)
		self.toolbar3.AddSeparator()

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.listSerial, 1, wx.ALL | wx.EXPAND, 0)
		hbox.Add(self.toolbar3, 0, wx.ALL | wx.EXPAND, 0)

		self.serial.SetSizer(hbox)

	def relistSerial(self):
		self.listSerial.Clear()
		try:
			path = self.conf.home + '/.pypilot/serial_ports'
			with open(path, 'r') as f:
				for line in f:
					line = line.replace('\n', '')
					line = line.strip()
					self.listSerial.Append(line)
		except Exception as e: 
			if self.debug: print(str(e))

	def onAddSerial(self, e): 
		dlg = selectConnections.AddPort('', True, 'auto', False)
		res = dlg.ShowModal()
		if res == wx.ID_OK:
			device = dlg.port.GetValue()
			if not device:
				self.ShowStatusBarRED(_('You have to select a device'))
				dlg.Destroy()
				return
			for i in range(self.listSerial.GetCount()):
				if device == self.listSerial.GetString(i):
					self.ShowStatusBarRED(_('This device already exists'))
					dlg.Destroy()
					return
			self.ShowStatusBarYELLOW(_('Applying changes ...'))
			path = self.conf.home + '/.pypilot/serial_ports'
			with open(path, 'a') as file:
				file.write(device + '\n')
			self.onRead()
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
			self.onRead()
		except Exception as e: 
			if self.debug: print(str(e))
		#nmeaXdevice
		path = self.conf.home + '/.pypilot/'
		tmp = os.listdir(path)
		for i in tmp:
			if i[:4] == 'nmea' and i[-6:] == 'device':
				subprocess.call(['rm', '-f', path+i])

################################################################################

def main():
	try:
		platform2 = platform.Platform()
		if not platform2.postInstall(version,'pypilot'):
			subprocess.Popen(['openplotterPostInstall', platform2.admin+' pypilotPostInstall'])
			return
	except: pass

	app = wx.App()
	pypilotFrame().Show()
	time.sleep(1)
	app.MainLoop()

if __name__ == '__main__':
	main()
	
