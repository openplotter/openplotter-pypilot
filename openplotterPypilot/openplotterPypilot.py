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

import wx, os, webbrowser, subprocess, socket
import wx.richtext as rt
from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import platform

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = conf.Conf()
		self.conf_folder = self.conf.conf_folder
		self.platform = platform.Platform()
		self.currentdir = os.path.dirname(__file__)
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = language.Language(self.currentdir,'openplotter-pypilot',self.currentLanguage)

		wx.Frame.__init__(self, None, title=_('OpenPlotter Pypilot'), size=(800,444))
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
		toolDisabled = self.toolbar1.AddRadioTool(107, _('Disabled'), wx.Bitmap(self.currentdir+"/data/send.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolDisabled, toolDisabled)
		toolImu = self.toolbar1.AddRadioTool(103, _('Only IMU'), wx.Bitmap(self.currentdir+"/data/send.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolImu, toolImu)
		toolPypilot = self.toolbar1.AddRadioTool(106, _('Autopilot'), wx.Bitmap(self.currentdir+"/data/send.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolPypilot, toolPypilot)
		self.toolbar1.AddSeparator()
		toolCalibration = self.toolbar1.AddTool(108, _('Calibration'), wx.Bitmap(self.currentdir+"/data/settings.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCalibration, toolCalibration)
		self.toolbar1.AddSeparator()
		toolApply = self.toolbar1.AddTool(104, _('Apply'), wx.Bitmap(self.currentdir+"/data/apply.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolApply, toolApply)
		toolCancel = self.toolbar1.AddTool(105, _('Cancel'), wx.Bitmap(self.currentdir+"/data/cancel.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCancel, toolCancel)

		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.imu = wx.Panel(self.notebook)
		self.autopilot = wx.Panel(self.notebook)
		self.connections = wx.Panel(self.notebook)
		self.notebook.AddPage(self.imu, 'IMU')
		self.notebook.AddPage(self.autopilot, _('Autopilot'))
		self.notebook.AddPage(self.connections, _('Data output'))
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/imu.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/autopilot.png", wx.BITMAP_TYPE_PNG))
		img2 = self.il.Add(wx.Bitmap(self.currentdir+"/data/connections.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)
		self.notebook.SetPageImage(2, img2)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.readToolbar1()
		self.pageImu()
		self.pageAutopilot()
		self.pageConnections()
		
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
		self.SetStatusText('')

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/pypilot/pypilot_app.html"
		webbrowser.open(url, new=2)

	def OnToolSettings(self, event): 
		subprocess.call(['pkill', '-f', 'openplotter-settings'])
		subprocess.Popen('openplotter-settings')

	def pageImu(self):
		myoptionLabel = wx.StaticText(self.imu, label=_('Sending:  '))

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(myoptionLabel, 0, wx.LEFT | wx.EXPAND, 5)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox, 0, wx.ALL | wx.EXPAND, 5)
		vbox.AddStretchSpacer(1)
		self.imu.SetSizer(vbox)

		self.readImu()

	def readImu(self):
		pass
		'''
		self.toolbar2 = wx.ToolBar(self.imu, style=wx.TB_TEXT)
		skConnections = self.toolbar3.AddTool(302, _('SK Connection'), wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.OnSkConnections, skConnections)
		self.toolbar3.AddSeparator()
		skTo0183 = self.toolbar3.AddTool(303, 'SK → NMEA 0183', wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.OnSkTo0183, skTo0183)
		skTo2000 = self.toolbar3.AddTool(304, 'SK → NMEA 2000', wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.OnSkTo2000, skTo2000)

		self.listConnections = wx.ListCtrl(self.connections, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listConnections.InsertColumn(0, _('Type'), width=80)
		self.listConnections.InsertColumn(1, _('Mode'), width=80)
		self.listConnections.InsertColumn(2, _('Data'), width=315)
		self.listConnections.InsertColumn(3, _('Direction'), width=80)
		self.listConnections.InsertColumn(4, _('Port'), width=80)
		self.listConnections.InsertColumn(5, _('Editable'), width=80)
		self.listConnections.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onlistConnectionsSelected)
		self.listConnections.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onlistConnectionsDeselected)

		self.toolbar4 = wx.ToolBar(self.connections, style=wx.TB_TEXT | wx.TB_VERTICAL)
		self.editConnButton = self.toolbar4.AddTool(402, _('Edit'), wx.Bitmap(self.currentdir+"/data/edit.png"))
		self.Bind(wx.EVT_TOOL, self.OnEditConnButton, self.editConnButton)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.listConnections, 1, wx.EXPAND, 0)
		hbox.Add(self.toolbar4, 0)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar3, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.Add(hbox, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.AddStretchSpacer(1)
		self.connections.SetSizer(vbox)
		'''

	def readToolbar1(self):
		mode = self.conf.get('PYPILOT', 'mode')
		if not mode or mode == '0': 
			self.toolbar1.ToggleTool(107,True)#disabled
			self.toolbar1.EnableTool(108,False)#calibration
		elif mode == '1': 
			self.toolbar1.ToggleTool(103,True)#imu
			self.toolbar1.EnableTool(108,True)#calibration
		elif mode == '2': 
			self.toolbar1.ToggleTool(106,True)#autopilot
			self.toolbar1.EnableTool(108,True)#calibration

	def OnToolDisabled(self,e):
		pass

	def OnToolImu(self,e):
		pass
		'''
		self.notebook.ChangeSelection(0)
		if self.toolbar1.GetToolState(103): self.myoption.SetLabel('1')
		else: self.myoption.SetLabel('0')
		'''

	def OnToolPypilot(self,e):
		pass

	def OnToolCalibration(self,e):
		pass

	def pageAutopilot(self):
		pass
		'''
		myoptionLabel = wx.StaticText(self.autopilot, label=_('Sending:  '))

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(myoptionLabel, 0, wx.LEFT | wx.EXPAND, 5)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox, 0, wx.ALL | wx.EXPAND, 5)
		vbox.AddStretchSpacer(1)
		self.autopilot.SetSizer(vbox)

		self.readAutopilot()
		'''

	def readAutopilot(self):
		pass
		'''
		value = self.conf.get('MYAPP', 'sending')
		if not value: value = '0' 
		if value == '1': self.toolbar1.ToggleTool(103,True)
		else: self.toolbar1.ToggleTool(103,False)
		'''

	def pageConnections(self):
		self.toolbar3 = wx.ToolBar(self.connections, style=wx.TB_TEXT)
		skConnections = self.toolbar3.AddTool(302, _('SK Connection'), wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.OnSkConnections, skConnections)
		self.toolbar3.AddSeparator()
		skTo0183 = self.toolbar3.AddTool(303, 'SK → NMEA 0183', wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.OnSkTo0183, skTo0183)
		skTo2000 = self.toolbar3.AddTool(304, 'SK → NMEA 2000', wx.Bitmap(self.currentdir+"/data/sk.png"))
		self.Bind(wx.EVT_TOOL, self.OnSkTo2000, skTo2000)

		self.listConnections = wx.ListCtrl(self.connections, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES, size=(-1,200))
		self.listConnections.InsertColumn(0, _('Type'), width=80)
		self.listConnections.InsertColumn(1, _('Mode'), width=80)
		self.listConnections.InsertColumn(2, _('Data'), width=315)
		self.listConnections.InsertColumn(3, _('Direction'), width=80)
		self.listConnections.InsertColumn(4, _('Port'), width=80)
		self.listConnections.InsertColumn(5, _('Editable'), width=80)
		self.listConnections.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onlistConnectionsSelected)
		self.listConnections.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onlistConnectionsDeselected)

		self.toolbar4 = wx.ToolBar(self.connections, style=wx.TB_TEXT | wx.TB_VERTICAL)
		self.editConnButton = self.toolbar4.AddTool(402, _('Edit'), wx.Bitmap(self.currentdir+"/data/edit.png"))
		self.Bind(wx.EVT_TOOL, self.OnEditConnButton, self.editConnButton)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(self.listConnections, 1, wx.EXPAND, 0)
		hbox.Add(self.toolbar4, 0)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar3, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.Add(hbox, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.AddStretchSpacer(1)
		self.connections.SetSizer(vbox)
		self.readConnections()
		self.printConnections()

	def readConnections(self):
		from .ports import Ports
		self.ports = Ports(self.conf, self.currentLanguage)

	def printConnections(self):
		if self.platform.skPort: 
			self.toolbar3.EnableTool(302,True)
			self.toolbar3.EnableTool(303,True)
			if self.platform.isSKpluginInstalled('signalk-to-nmea2000'):
				self.toolbar3.EnableTool(304,True)
			else: self.toolbar3.EnableTool(304,False)
		else:
			self.toolbar3.EnableTool(302,False)
			self.toolbar3.EnableTool(303,False)
			self.toolbar3.EnableTool(304,False)
		self.toolbar4.EnableTool(402,False)

		self.listConnections.DeleteAllItems()
		mode = self.conf.get('PYPILOT', 'mode')
		if not mode or mode == '0':
			self.listConnections.Append([self.ports.connections[0]['type'], self.ports.connections[0]['mode'], self.ports.connections[0]['data'], self.direction(self.ports.connections[0]['direction']), str(self.ports.connections[0]['port']), self.editable(self.ports.connections[0]['editable'])])
			self.listConnections.Append([self.ports.connections[1]['type'], self.ports.connections[1]['mode'], self.ports.connections[1]['data'], self.direction(self.ports.connections[1]['direction']), str(self.ports.connections[1]['port']), self.editable(self.ports.connections[1]['editable'])])
			self.listConnections.Append([self.ports.connections[2]['type'], self.ports.connections[2]['mode'], self.ports.connections[2]['data'], self.direction(self.ports.connections[2]['direction']), str(self.ports.connections[2]['port']), self.editable(self.ports.connections[2]['editable'])])
		elif mode == '1':
			self.listConnections.Append([self.ports.connections[0]['type'], self.ports.connections[0]['mode'], self.ports.connections[0]['data'], self.direction(self.ports.connections[0]['direction']), str(self.ports.connections[0]['port']), self.editable(self.ports.connections[0]['editable'])])
			self.listConnections.SetItemBackgroundColour(self.listConnections.GetItemCount()-1,(255,215,0))
			self.listConnections.Append([self.ports.connections[1]['type'], self.ports.connections[1]['mode'], self.ports.connections[1]['data'], self.direction(self.ports.connections[1]['direction']), str(self.ports.connections[1]['port']), self.editable(self.ports.connections[1]['editable'])])
			self.listConnections.SetItemBackgroundColour(self.listConnections.GetItemCount()-1,(255,215,0))
			self.listConnections.Append([self.ports.connections[2]['type'], self.ports.connections[2]['mode'], self.ports.connections[2]['data'], self.direction(self.ports.connections[2]['direction']), str(self.ports.connections[2]['port']), self.editable(self.ports.connections[2]['editable'])])
		elif mode == '2':
			self.listConnections.Append([self.ports.connections[0]['type'], self.ports.connections[0]['mode'], self.ports.connections[0]['data'], self.direction(self.ports.connections[0]['direction']), str(self.ports.connections[0]['port']), self.editable(self.ports.connections[0]['editable'])])
			self.listConnections.SetItemBackgroundColour(self.listConnections.GetItemCount()-1,(255,215,0))
			self.listConnections.Append([self.ports.connections[1]['type'], self.ports.connections[1]['mode'], self.ports.connections[1]['data'], self.direction(self.ports.connections[1]['direction']), str(self.ports.connections[1]['port']), self.editable(self.ports.connections[1]['editable'])])
			self.listConnections.SetItemBackgroundColour(self.listConnections.GetItemCount()-1,(255,215,0))
			self.listConnections.Append([self.ports.connections[2]['type'], self.ports.connections[2]['mode'], self.ports.connections[2]['data'], self.direction(self.ports.connections[2]['direction']), str(self.ports.connections[2]['port']), self.editable(self.ports.connections[2]['editable'])])
			self.listConnections.SetItemBackgroundColour(self.listConnections.GetItemCount()-1,(115,255,115))
	
	def editable(self, data):
		if data == '1': return _('yes')
		else: return _('no')

	def direction(self, data):
		if data == '1': return _('input')
		elif data == '2': return _('output')
		elif data == '3': return _('both')
		else: return ''

	def OnSkConnections(self,e):
		url = self.platform.http+'localhost:'+self.platform.skPort+'/admin/#/serverConfiguration/connections/-'
		webbrowser.open(url, new=2)

	def OnSkTo0183(self,e):
		url = self.platform.http+'localhost:'+self.platform.skPort+'/admin/#/serverConfiguration/plugins/sk-to-nmea0183'
		webbrowser.open(url, new=2)

	def OnSkTo2000(self,e):
		url = self.platform.http+'localhost:'+self.platform.skPort+'/admin/#/serverConfiguration/plugins/sk-to-nmea2000'
		webbrowser.open(url, new=2)

	def OnEditConnButton(self,e):
		selected = self.listConnections.GetFirstSelected()
		if selected == -1: return
		dlg = editPort(self.ports.connections[selected]['port'])
		res = dlg.ShowModal()
		if res == wx.ID_OK:
			self.ports.connections[selected]['port'] = dlg.port.GetValue()
			self.printConnections()
		dlg.Destroy()

	def onlistConnectionsSelected(self,e):
		i = e.GetIndex()
		valid = e and i >= 0
		if not valid: return
		if self.ports.connections[i]['editable'] == '1': self.toolbar4.EnableTool(402,True)
		else: self.toolbar4.EnableTool(402,False)

	def onlistConnectionsDeselected(self,e=0):
		self.toolbar4.EnableTool(402,False)

	def OnToolApply(self,e):
		if self.toolbar1.GetToolState(107): self.conf.set('PYPILOT', 'mode', '0')
		elif self.toolbar1.GetToolState(103): self.conf.set('PYPILOT', 'mode', '1')
		elif self.toolbar1.GetToolState(106): self.conf.set('PYPILOT', 'mode', '2')
		'''
		if self.toolbar1.GetToolState(103):
			self.conf.set('MYAPP', 'sending', '1')
			# starts service and enables it at startup. Use self.platform.admin instead of sudo
			subprocess.Popen([self.platform.admin, 'python3', self.currentdir+'/service.py', 'enable'])
			self.ShowStatusBarGREEN(_('Sending dummy data enabled'))
		else:
			self.conf.set('MYAPP', 'sending', '0')
			# stops service and disables it at startup. Use self.platform.admin instead of sudo
			subprocess.Popen([self.platform.admin, 'python3', self.currentdir+'/service.py', 'disable'])
			self.ShowStatusBarYELLOW(_('Sending dummy data disabled'))
		for i in self.ports.connections:
			self.conf.set('MYAPP', i['id'], str(i['port']))
		self.readMyapp()
		self.readConnections()
		self.printConnections()
		'''
		self.readToolbar1()

	def OnToolCancel(self,e):
		self.ShowStatusBarRED(_('Changes canceled'))
		self.readImu()
		self.readAutopilot()
		self.readConnections()
		self.printConnections()

################################################################################

class editPort(wx.Dialog):
	def __init__(self, port):
		wx.Dialog.__init__(self, None, title=_('Port'), size=(200,150))
		panel = wx.Panel(self)
		self.port = wx.SpinCtrl(panel, 101, min=4000, max=65536, initial=50000)
		self.port.SetValue(int(port))

		cancelBtn = wx.Button(panel, wx.ID_CANCEL)
		okBtn = wx.Button(panel, wx.ID_OK)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(cancelBtn, 1, wx.ALL | wx.EXPAND, 10)
		hbox.Add(okBtn, 1, wx.ALL | wx.EXPAND, 10)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.port, 1, wx.ALL | wx.EXPAND, 10)
		vbox.Add(hbox, 0, wx.EXPAND, 0)

		panel.SetSizer(vbox)
		self.Centre() 

################################################################################

def main():
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()

if __name__ == '__main__':
	main()
