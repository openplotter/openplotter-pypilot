#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
# Copyright (C) 2019 by Sean D'Epagnier <https://github.com/pypilot/openplotter-pypilot>
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

import wx, os, webbrowser, subprocess, sys, RTIMU, time, ujson
from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import ports
from openplotterSettings import platform
from openplotterSettings import selectConnections

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = conf.Conf()
		self.conf_folder = self.conf.conf_folder
		self.platform = platform.Platform()
		self.currentdir = os.path.dirname(__file__)
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = language.Language(self.currentdir,'openplotter-pypilot',self.currentLanguage)

		wx.Frame.__init__(self, None, title='Pypilot', size=(800,444))
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
		self.mode = wx.ComboBox(self.toolbar1, 103, _('Mode'), choices=[_('Disabled'),_('Only compass'),_('Autopilot')], size=(150,-1), style=wx.CB_DROPDOWN)
		toolMode = self.toolbar1.AddControl(self.mode)
		self.Bind(wx.EVT_COMBOBOX, self.OnMode, toolMode)
		self.toolbar1.AddSeparator()
		toolCalibration= self.toolbar1.AddTool(104, _('Calibration'), wx.Bitmap(self.currentdir+"/data/calibration.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCalibration, toolCalibration)
		toolScope= self.toolbar1.AddTool(105, _('Scope'), wx.Bitmap(self.currentdir+"/data/scope.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolScope, toolScope)
		toolClient= self.toolbar1.AddTool(106, _('Client'), wx.Bitmap(self.currentdir+"/data/client.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolClient, toolClient)
		self.toolbar1.AddSeparator()
		toolRefresh= self.toolbar1.AddTool(107, _('Refresh'), wx.Bitmap(self.currentdir+"/data/refresh.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolRefresh, toolRefresh)

		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.autopilot = wx.Panel(self.notebook)
		self.connections = wx.Panel(self.notebook)
		self.notebook.AddPage(self.autopilot, _('Autopilot'))
		self.notebook.AddPage(self.connections, _('Connections'))
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/autopilot.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/connections.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.pageAutopilot()
		self.pageConnections()
		self.onRead()
		
		maxi = self.conf.get('GENERAL', 'maximize')
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
		except:pass

	def OnToolRefresh(self, event):
		self.SetStatusText('')
		self.onRead()

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/pypilot/pypilot_app.html"
		webbrowser.open(url, new=2)

	def OnToolSettings(self, event=0): 
		subprocess.call(['pkill', '-f', 'openplotter-settings'])
		subprocess.Popen('openplotter-settings')

	def OnMode(self,e):
		self.ShowStatusBarYELLOW(_('Applying changes ...'))
		mode = self.mode.GetSelection()
		if mode == 0: subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'disable'])
		elif mode == 1: subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'boatimu'])
		elif mode == 2: subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'pypilot'])
		self.removeNmeaFiles()
		self.onRead()
		self.ShowStatusBarGREEN(_('Changes applied'))

	def OnToolCalibration(self,e):
		subprocess.call(['pkill', '-f', 'pypilot_calibration'])
		subprocess.Popen(['pypilot_calibration', 'localhost'])

	def OnToolScope(self,e):
		subprocess.call(['pkill', '-f', 'signalk_scope_wx'])
		subprocess.Popen(['signalk_scope_wx', 'localhost'])

	def OnToolClient(self,e):
		subprocess.call(['pkill', '-f', 'signalk_client_wx'])
		subprocess.Popen(['signalk_client_wx', 'localhost'])

	def onRead(self):
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_boatimu']).decode(sys.stdin.encoding)
			pypilot_boatimu = True
		except: pypilot_boatimu = False
		try:
			subprocess.check_output(['systemctl', 'is-enabled', 'pypilot']).decode(sys.stdin.encoding)
			pypilot = True
		except: pypilot = False

		self.disableAll()
		if not pypilot and not pypilot_boatimu: 
			self.mode.SetSelection(0)
		elif pypilot_boatimu: 
			self.mode.SetSelection(1)
			self.toolbar1.EnableTool(104,True)
			self.toolbar1.EnableTool(105,True)
			self.toolbar1.EnableTool(106,True)
		elif pypilot: 
			self.mode.SetSelection(2)
			self.toolbar1.EnableTool(104,True)
			self.toolbar1.EnableTool(105,True)
			self.toolbar1.EnableTool(106,True)
			self.toolbar2.EnableTool(201,True)
			self.toolbar2.EnableTool(202,True)
			self.toolbar2.EnableTool(204,True)
			self.toolbar3.EnableTool(301,True)
			try:
				subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_web']).decode(sys.stdin.encoding)
				self.toolbar2.ToggleTool(202,True)
				self.toolbar2.EnableTool(203,True)
			except: pass
			try:
				subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_lcd']).decode(sys.stdin.encoding)
				self.toolbar2.ToggleTool(204,True)
			except: pass
			self.listSerial.Enable()

		try:
			subprocess.check_output(['i2cdetect', '-y', '1']).decode(sys.stdin.encoding)
		except:
			self.ShowStatusBarRED(_('I2C is disabled. Please enable I2C interface in Preferences -> Raspberry Pi configuration -> Interfaces'))
			self.imuDetected.SetLabel(_('Failed'))
		else:
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

		self.listSerial.DeleteAllItems()
		try:
			path = self.conf.home + '/.pypilot/serial_ports'
			with open(path, 'r') as f:
				for line in f:
					line = line.replace('\n', '')
					line = line.strip()
					self.listSerial.InsertItem(self.listSerial.GetItemCount(), line)
					if pypilot:
						self.listSerial.SetItemBackgroundColour(self.listSerial.GetItemCount()-1,(102,205,170))
		except: pass

		self.listConnections.DeleteAllItems()
		self.onlistConnectionsDeselected()
		if pypilot:
			item = self.listConnections.InsertItem(self.listConnections.GetItemCount(), 'NMEA 0183: '+_('Heading, Heel, Pitch, Serial devices'))
			self.listConnections.SetItem(item, 1, 'TCP')
			self.listConnections.SetItem(item, 2, '20220')
			item = self.listConnections.InsertItem(self.listConnections.GetItemCount(), 'Signal K: '+_('Heel, Pitch'))
			self.listConnections.SetItem(item, 1, 'UDP')
			self.listConnections.SetItem(item, 2, '20220')
		elif pypilot_boatimu:
			item = self.listConnections.InsertItem(self.listConnections.GetItemCount(), 'Signal K: '+_('Heading, Heel, Pitch'))
			self.listConnections.SetItem(item, 1, 'UDP')
			self.listConnections.SetItem(item, 2, '20220')
		sklist = []
		try:
			setting_file = self.platform.skDir+'/settings.json'
			data = ''
			with open(setting_file) as data_file:
				data = ujson.load(data_file)
			if 'pipedProviders' in data:
				for i in data['pipedProviders']:
					if i['pipeElements'][0]['options']['type']=='SignalK':
						if i['pipeElements'][0]['options']['subOptions']['type']=='udp':
							if i['pipeElements'][0]['options']['subOptions']['port']=='20220':
								sklist.append([i['id'],'UDP',i['enabled']])
					if i['pipeElements'][0]['options']['type']=='NMEA0183':
						if i['pipeElements'][0]['options']['subOptions']['type']=='tcp':
							if i['pipeElements'][0]['options']['subOptions']['port']=='20220':
								sklist.append([i['id'],'TCP',i['enabled']])
		except:pass
		for i in sklist:
			exists = False
			for ii in range(self.listConnections.GetItemCount()):
				if not self.listConnections.GetItemText(ii, 3):
					if self.listConnections.GetItemText(ii, 1) == i[1]:
						self.listConnections.SetItem(ii, 3, i[0])
						if i[2]:
							if i[1] == 'TCP':
								self.listConnections.SetItemBackgroundColour(ii,(102,205,170))
							if i[1] == 'UDP':
								self.listConnections.SetItemBackgroundColour(ii,(255,215,0))
						exists = True
			if not exists:
				self.listConnections.Append(['', i[1], '20220', i[0]])
				self.listConnections.SetItemBackgroundColour(self.listConnections.GetItemCount()-1,(255,0,0))

	def disableAll(self):
		self.toolbar1.EnableTool(104,False)
		self.toolbar1.EnableTool(105,False)
		self.toolbar1.EnableTool(106,False)
		self.toolbar2.EnableTool(201,False)
		self.toolbar2.EnableTool(202,False)
		self.toolbar2.ToggleTool(202,False)
		self.toolbar2.EnableTool(203,False)
		self.toolbar2.EnableTool(204,False)
		self.toolbar2.ToggleTool(204,False)
		self.toolbar3.EnableTool(301,False)
		self.toolbar3.EnableTool(302,False)
		self.listSerial.Disable()

	def pageAutopilot(self):
		self.listSerial = wx.ListCtrl(self.autopilot, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listSerial.InsertColumn(0, _('Autopilot serial devices'), width=630)
		self.listSerial.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListSerialSelected)
		self.listSerial.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onListSerialDeselected)

		self.toolbar2 = wx.ToolBar(self.autopilot, style=wx.TB_TEXT)
		toolControl = self.toolbar2.AddTool(201, _('Control'), wx.Bitmap(self.currentdir+"/data/control.png"))
		self.Bind(wx.EVT_TOOL, self.onToolControl, toolControl)
		self.toolbar2.AddSeparator()
		toolBrowser = self.toolbar2.AddCheckTool(202, _('Browser Control'), wx.Bitmap(self.currentdir+"/data/control.png"))
		self.Bind(wx.EVT_TOOL, self.onToolBrowser, toolBrowser)
		toolOpen = self.toolbar2.AddTool(203, _('Open'), wx.Bitmap(self.currentdir+"/data/open.png"))
		self.Bind(wx.EVT_TOOL, self.onToolOpen, toolOpen)
		self.toolbar2.AddSeparator()
		toolLcd = self.toolbar2.AddCheckTool(204, _('LCD keypad/Remote Control'), wx.Bitmap(self.currentdir+"/data/control.png"))
		self.Bind(wx.EVT_TOOL, self.onToolLcd, toolLcd)
		self.toolbar2.AddSeparator()

		imuDetectedLabel = wx.StaticText( self.autopilot, wx.ID_ANY, _('Detected IMU:'))
		self.imuDetected = wx.StaticText( self.autopilot, wx.ID_ANY, _('none'))

		self.toolbar3 = wx.ToolBar(self.autopilot, style=wx.TB_TEXT | wx.TB_VERTICAL)
		toolAdd = self.toolbar3.AddTool(301, _('Add device'), wx.Bitmap(self.currentdir+"/data/add.png"))
		self.Bind(wx.EVT_TOOL, self.onToolAdd, toolAdd)
		toolRemove = self.toolbar3.AddTool(302, _('Remove device'), wx.Bitmap(self.currentdir+"/data/remove.png"))
		self.Bind(wx.EVT_TOOL, self.onToolRemove, toolRemove)

		h1 = wx.BoxSizer(wx.HORIZONTAL)
		h1.Add(self.listSerial, 1, wx.EXPAND, 0)
		h1.Add(self.toolbar3, 0, wx.EXPAND, 0)

		h2 = wx.BoxSizer(wx.HORIZONTAL)
		h2.AddStretchSpacer(1)
		h2.Add(imuDetectedLabel, 0, wx.EXPAND, 0)
		h2.Add(self.imuDetected, 0, wx.LEFT | wx.EXPAND, 10)
		h2.AddStretchSpacer(1)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(h2, 1, wx.EXPAND, 0)
		sizer.AddSpacer(10)
		sizer.Add(self.toolbar2, 0, wx.EXPAND, 0)
		sizer.Add(h1, 1, wx.EXPAND, 0)

		self.autopilot.SetSizer(sizer)

	def onToolControl(self,e):
		subprocess.call(['pkill', '-f', 'pypilot_control'])
		subprocess.Popen(['pypilot_control', 'localhost'])

	def onToolBrowser(self, e): 
		if self.toolbar2.GetToolState(202):
			subprocess.Popen([self.platform.admin, 'python3', self.currentdir+'/service.py', 'enableBrowser'])
			self.toolbar2.EnableTool(203,True)
		else: 
			subprocess.Popen([self.platform.admin, 'python3', self.currentdir+'/service.py', 'disableBrowser'])
			self.toolbar2.EnableTool(203,False)

	def onToolOpen(self, e): 
		url = "http://localhost:8080"
		webbrowser.open(url, new=2)

	def onToolLcd(self, e): 
		if self.toolbar2.GetToolState(204):
			subprocess.Popen([self.platform.admin, 'python3', self.currentdir+'/service.py', 'enableLcd'])
		else: 
			subprocess.Popen([self.platform.admin, 'python3', self.currentdir+'/service.py', 'disableLcd'])

	def onToolAdd(self, e): 
		dlg = selectConnections.AddPort('', True, 'auto', False)
		res = dlg.ShowModal()
		if res == wx.ID_OK:
			device = dlg.port.GetValue()
			if not device: 
				self.ShowStatusBarRED(_('You have to select a device'))
				dlg.Destroy()
				return
			for i in range(self.listSerial.GetItemCount()):
				if device == self.listSerial.GetItemText(i, 0):
					self.ShowStatusBarRED(_('This device already exists'))
					dlg.Destroy()
					return
			self.ShowStatusBarYELLOW(_('Applying changes ...'))
			path = self.conf.home + '/.pypilot/serial_ports'
			with open(path, "a") as file:
				file.write(device + '\n')
			self.removeNmeaFiles()
			subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'pypilot'])
			self.onRead()
			self.ShowStatusBarGREEN(_('Changes applied'))
		dlg.Destroy()

	def onToolRemove(self, e): 
		index = self.listSerial.GetFirstSelected()
		if index == -1: return
		device = self.listSerial.GetItemText(index, 0)
		self.ShowStatusBarYELLOW(_('Applying changes ...'))
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
		self.removeNmeaFiles()
		subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'pypilot'])
		self.onRead()
		self.ShowStatusBarGREEN(_('Changes applied'))
		
	def removeNmeaFiles(self):
		#nmeaXdevice
		path = self.conf.home + '/.pypilot/'
		tmp = os.listdir(path)
		for i in tmp:
			if i[:4] == 'nmea' and i[-6:] == 'device':
				subprocess.call(['rm', '-f', path+i])

	def onListSerialSelected(self,e):
		i = e.GetIndex()
		valid = e and i >= 0
		self.onListSerialDeselected()
		if not valid: return
		self.toolbar3.EnableTool(302,True)

	def onListSerialDeselected(self,e=0):	
		self.toolbar3.EnableTool(302,False)

	###########################################################################

	def pageConnections(self):
		self.listConnections = wx.ListCtrl(self.connections, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listConnections.InsertColumn(0, _('Data'), width=320)
		self.listConnections.InsertColumn(1, _('Type'), width=60)
		self.listConnections.InsertColumn(2, _('Port'), width=60)
		self.listConnections.InsertColumn(3, _('SK connection ID'), width=180)
		self.listConnections.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onlistConnectionsSelected)
		self.listConnections.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onlistConnectionsDeselected)

		self.toolbar4 = wx.ToolBar(self.connections, style=wx.TB_TEXT | wx.TB_VERTICAL)
		skConnections = self.toolbar4.AddTool(401, _('Add Connection'), wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.OnSkConnections, skConnections)
		self.editSKButton = self.toolbar4.AddTool(402, _('Edit connection'), wx.Bitmap(self.currentdir+"/data/edit.png"))
		self.Bind(wx.EVT_TOOL, self.OnEditSKButton, self.editSKButton)
		self.removeConnButton = self.toolbar4.AddTool(403, _('Remove connection'), wx.Bitmap(self.currentdir+"/data/remove.png"))
		self.Bind(wx.EVT_TOOL, self.OnRemoveConnButton, self.removeConnButton)

		vbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox.Add(self.listConnections, 1, wx.EXPAND, 0)
		vbox.Add(self.toolbar4, 0, wx.EXPAND, 0)

		self.connections.SetSizer(vbox)

	def onlistConnectionsSelected(self,e):
		i = e.GetIndex()
		valid = e and i >= 0
		self.onlistConnectionsDeselected()
		if not valid: return
		connection = self.listConnections.GetItemText(i, 3)
		if connection:
			self.toolbar4.EnableTool(402,True)
			self.toolbar4.EnableTool(403,True)
		else: self.toolbar4.EnableTool(401,True)

	def onlistConnectionsDeselected(self,e=0):
		self.toolbar4.EnableTool(401,False)
		self.toolbar4.EnableTool(402,False)
		self.toolbar4.EnableTool(403,False)

	def OnSkConnections(self,e):
		if self.platform.skPort:
			selected = self.listConnections.GetFirstSelected()
			if selected == -1: return
			connType = self.listConnections.GetItemText(selected, 1)
			from openplotterSignalkInstaller import editSettings
			skSettings = editSettings.EditSettings()
			if connType == 'UDP': 
				ID = 'Pypilot Signal K'
				data = 'SignalK'
			elif connType == 'TCP': 
				ID = 'Pypilot NMEA 0183'
				data = 'NMEA0183'
			c = 0
			while True:
				if skSettings.connectionIdExists(ID):
					ID = ID+str(c)
					c = c + 1
				else: break
			if skSettings.setNetworkConnection(ID,data,connType,'localhost','20220'):
				self.restart_SK(0)
				self.onRead()
			else: self.ShowStatusBarRED(_('Failed. Error creating connection in Signal K'))
		else: 
			self.ShowStatusBarRED(_('Please install "Signal K Installer" OpenPlotter app'))
			self.OnToolSettings()

	def OnEditSKButton(self,e):
		selected = self.listConnections.GetFirstSelected()
		if selected == -1: return
		skId = self.listConnections.GetItemText(selected, 3)
		url = self.platform.http+'localhost:'+self.platform.skPort+'/admin/#/serverConfiguration/connections/'+skId
		webbrowser.open(url, new=2)

	def OnRemoveConnButton(self,e):
		selected = self.listConnections.GetFirstSelected()
		if selected == -1: return
		skId = self.listConnections.GetItemText(selected, 3)
		from openplotterSignalkInstaller import editSettings
		skSettings = editSettings.EditSettings()
		if skSettings.removeConnection(skId): 
			self.restart_SK(0)
			self.onRead()
		else: self.ShowStatusBarRED(_('Failed. Error removing connection in Signal K'))

	def restart_SK(self, msg):
		if msg == 0: msg = _('Restarting Signal K server... ')
		seconds = 12
		subprocess.call([self.platform.admin, 'python3', self.currentdir+'/service.py', 'restart'])
		for i in range(seconds, 0, -1):
			self.ShowStatusBarYELLOW(msg+str(i))
			time.sleep(1)
		self.ShowStatusBarGREEN(_('Signal K server restarted'))

################################################################################

def main():
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()

if __name__ == '__main__':
	main()
