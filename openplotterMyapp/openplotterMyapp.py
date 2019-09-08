#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by xxxx <https://github.com/xxxx/openplotter-myapp>
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
# use the class "platform" to get info about the host system. See: https://github.com/openplotter/openplotter-settings/blob/master/openplotterSettings/platform.py
from openplotterSettings import platform

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = conf.Conf()
		self.conf_folder = self.conf.conf_folder
		self.platform = platform.Platform()
		self.currentdir = os.path.dirname(__file__)
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = language.Language(self.currentdir,'openplotter-myapp',self.currentLanguage)

		wx.Frame.__init__(self, None, title=_('OpenPlotter My App'), size=(800,444))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/openplotter-myapp.png", wx.BITMAP_TYPE_PNG)
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
		toolSend = self.toolbar1.AddCheckTool(103, _('Dummy Data'), wx.Bitmap(self.currentdir+"/data/send.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSend, toolSend)
		self.toolbar1.AddSeparator()
		toolOutput = self.toolbar1.AddTool(106, _('Dummy Output'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolOutput, toolOutput)
		self.toolbar1.AddSeparator()
		toolApply = self.toolbar1.AddTool(104, _('Apply Changes'), wx.Bitmap(self.currentdir+"/data/apply.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolApply, toolApply)
		toolCancel = self.toolbar1.AddTool(105, _('Cancel Changes'), wx.Bitmap(self.currentdir+"/data/cancel.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCancel, toolCancel)

		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.myapp = wx.Panel(self.notebook)
		self.connections = wx.Panel(self.notebook)
		self.output = wx.Panel(self.notebook)
		self.notebook.AddPage(self.myapp, _('My App'))
		self.notebook.AddPage(self.connections, _('Data output'))
		self.notebook.AddPage(self.output, _('Output'))
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/openplotter-24.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/connections.png", wx.BITMAP_TYPE_PNG))
		img2 = self.il.Add(wx.Bitmap(self.currentdir+"/data/output.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)
		self.notebook.SetPageImage(2, img2)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.pageMyapp()
		self.pageConnections()
		self.pageOutput()
		
		self.Centre() 

	def ShowStatusBar(self, w_msg, colour):
		self.GetStatusBar().SetForegroundColour(colour)
		self.SetStatusText(w_msg)

	# red for error or cancellation messages
	def ShowStatusBarRED(self, w_msg):
		self.ShowStatusBar(w_msg, (130,0,0))

	# green for succesful messages
	def ShowStatusBarGREEN(self, w_msg):
		self.ShowStatusBar(w_msg, (0,130,0))

	# black for informative messages
	def ShowStatusBarBLACK(self, w_msg):
		self.ShowStatusBar(w_msg, wx.BLACK) 

	# yellow for attention messages
	def ShowStatusBarYELLOW(self, w_msg):
		self.ShowStatusBar(w_msg,(255,140,0)) 

	def onTabChange(self, event):
		self.SetStatusText('')

	# create your page in the manuals and add the link here
	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/template/myapp_app.html"
		webbrowser.open(url, new=2)

	def OnToolSettings(self, event): 
		subprocess.call(['pkill', '-f', 'openplotter-settings'])
		subprocess.Popen('openplotter-settings')

	def pageOutput(self):
		self.logger = rt.RichTextCtrl(self.output, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.logger, 1, wx.EXPAND, 0)
		self.output.SetSizer(sizer)

	def pageMyapp(self):
		myoptionLabel = wx.StaticText(self.myapp, label=_('Sending:  '))
		self.myoption = wx.StaticText(self.myapp, label='')

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(myoptionLabel, 0, wx.LEFT | wx.EXPAND, 5)
		hbox.Add(self.myoption, 0, wx.LEFT | wx.EXPAND, 5)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox, 0, wx.ALL | wx.EXPAND, 5)
		vbox.AddStretchSpacer(1)
		self.myapp.SetSizer(vbox)

		self.readMyapp()

	def readMyapp(self):
		# here get data from conf file to load the surrent settings
		value = self.conf.get('MYAPP', 'sending')
		if not value: value = '0' 
		self.myoption.SetLabel(value)
		if value == '1': self.toolbar1.ToggleTool(103,True)
		else: self.toolbar1.ToggleTool(103,False)

	def OnToolSend(self,e):
		self.notebook.ChangeSelection(0)
		if self.toolbar1.GetToolState(103): self.myoption.SetLabel('1')
		else: self.myoption.SetLabel('0')

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
		print ()

	def printConnections(self):
		# Check if Signal K and some plugins are installed
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
		enabled = self.conf.get('MYAPP', 'sending')
		for i in self.ports.connections:
			if i['editable'] == '1': editable = _('yes')
			else: editable = _('no')
			direction = ''
			if i['direction'] == '1': direction = _('input')
			elif i['direction'] == '2': direction = _('output')
			elif i['direction'] == '3': direction = _('both')
			self.listConnections.Append([i['type'], i['mode'], i['data'], direction, str(i['port']), editable])
			# if the connection is enabled we will set the item background to:
			# yellow for Signal K data: (255,215,0)
			# blue for NMEA 2000 data: (0,215,255)
			# green for NMEA 0183 data: (115,255,115)
			if enabled == '1': self.listConnections.SetItemBackgroundColour(self.listConnections.GetItemCount()-1,(255,215,0))

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
		
	def OnToolCancel(self,e):
		self.ShowStatusBarRED(_('Changes canceled'))
		self.readMyapp()
		self.readConnections()
		self.printConnections()

	def OnToolOutput(self,e):
		self.logger.Clear()
		self.notebook.ChangeSelection(2)
		# You can write formated text
		self.logger.BeginTextColour((0, 130, 0))
		self.logger.BeginBold()
		self.logger.WriteText(_('Hello World!'))
		self.logger.EndBold()
		self.logger.EndTextColour()
		self.logger.Newline()
		# or print any program output
		self.logger.BeginTextColour((55, 55, 55))
		command = self.platform.admin+' apt update'
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
		for line in popen.stdout:
			if not 'Warning' in line and not 'WARNING' in line:
				self.logger.WriteText(line)
				self.ShowStatusBarYELLOW(_('Updating packages data, please wait... ')+line)
				self.logger.ShowPosition(self.logger.GetLastPosition())
		self.logger.EndTextColour()

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
