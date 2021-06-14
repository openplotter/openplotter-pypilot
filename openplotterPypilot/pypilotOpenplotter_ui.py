# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jun 12 2021)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class pypilotPanelBase
###########################################################################

class pypilotPanelBase ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.pypilotVersion = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"pypilot version"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pypilotVersion.Wrap( -1 )

		fgSizer1.Add( self.pypilotVersion, 0, wx.ALL, 5 )

		self.version = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"N/A"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.version.Wrap( -1 )

		fgSizer1.Add( self.version, 0, wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Detected IMU:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.imuDetected = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"N/A"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.imuDetected.Wrap( -1 )

		fgSizer1.Add( self.imuDetected, 0, wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText12 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Detected Hardware"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		fgSizer1.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.hardware = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"None"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.hardware.Wrap( -1 )

		fgSizer1.Add( self.hardware, 0, wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Services"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		fgSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )

		servicesChoices = [ _(u"Disabled"), _(u"IMU Only"), _(u"Autopilot") ]
		self.services = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, servicesChoices, 0 )
		self.services.SetSelection( 0 )
		fgSizer1.Add( self.services, 0, wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Web Control"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		fgSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.WebControl = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"Enable"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.WebControl, 0, wx.ALL, 5 )

		self.m_button3 = wx.Button( self.m_panel1, wx.ID_ANY, _(u"Open Browser"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_button3, 0, wx.ALL, 5 )

		self.m_staticText8 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Hat Control"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		fgSizer1.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.HatControl = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"Enable"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.HatControl, 0, wx.ALL, 5 )

		self.m_button4 = wx.Button( self.m_panel1, wx.ID_ANY, _(u"Configure"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_button4, 0, wx.ALL, 5 )


		self.m_panel1.SetSizer( fgSizer1 )
		self.m_panel1.Layout()
		fgSizer1.Fit( self.m_panel1 )
		self.m_notebook1.AddPage( self.m_panel1, _(u"Services"), True )
		self.m_panel7 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer12 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText14 = wx.StaticText( self.m_panel7, wx.ID_ANY, _(u"If the pypilot hat service is enabled,\n pypilot uses gpio pins\n17, 23, 27, 22, 18, 5, 6, 26\n\nIf the pypilot hat contains an arduino additonal pins can be used for keys.\n\n\nEventually more control and configuration for these keys is intended"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		fgSizer12.Add( self.m_staticText14, 0, wx.ALL, 5 )


		self.m_panel7.SetSizer( fgSizer12 )
		self.m_panel7.Layout()
		fgSizer12.Fit( self.m_panel7 )
		self.m_notebook1.AddPage( self.m_panel7, _(u"Keys"), False )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer5 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer5.AddGrowableCol( 0 )
		fgSizer5.AddGrowableRow( 1 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer10 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer10.AddGrowableCol( 1 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"Hardware Serial"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer10.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.hardwareSerial = wx.StaticText( self.m_panel2, wx.ID_ANY, _(u"N/A"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.hardwareSerial.Wrap( -1 )

		fgSizer10.Add( self.hardwareSerial, 0, wx.ALL, 5 )

		self.bHardwareSerial = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Enable"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.bHardwareSerial, 0, wx.ALL, 5 )


		fgSizer5.Add( fgSizer10, 1, wx.EXPAND, 5 )

		listSerialChoices = []
		self.listSerial = wx.ListBox( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, listSerialChoices, 0 )
		fgSizer5.Add( self.listSerial, 0, wx.ALL|wx.EXPAND, 5 )

		fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_button6 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Add"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.m_button6, 0, wx.ALL, 5 )

		self.m_button7 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Remove"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.m_button7, 0, wx.ALL, 5 )


		fgSizer5.Add( fgSizer6, 1, wx.EXPAND, 5 )


		self.m_panel2.SetSizer( fgSizer5 )
		self.m_panel2.Layout()
		fgSizer5.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, _(u"Serial"), False )
		self.m_panel3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer4 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableRow( 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.installConsole = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		fgSizer4.Add( self.installConsole, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button5 = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Update"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_button5, 0, wx.ALL, 5 )


		self.m_panel3.SetSizer( fgSizer4 )
		self.m_panel3.Layout()
		fgSizer4.Fit( self.m_panel3 )
		self.m_notebook1.AddPage( self.m_panel3, _(u"Reinstall"), False )

		fgSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( fgSizer2 )
		self.Layout()
		fgSizer2.Fit( self )

		# Connect Events
		self.services.Bind( wx.EVT_CHOICE, self.onServices )
		self.WebControl.Bind( wx.EVT_CHECKBOX, self.onWebControl )
		self.m_button3.Bind( wx.EVT_BUTTON, self.onOpenBrowser )
		self.HatControl.Bind( wx.EVT_CHECKBOX, self.onHatControl )
		self.m_button4.Bind( wx.EVT_BUTTON, self.onConfigureHat )
		self.bHardwareSerial.Bind( wx.EVT_BUTTON, self.OnHardwareSerial )
		self.m_button6.Bind( wx.EVT_BUTTON, self.onAddSerial )
		self.m_button7.Bind( wx.EVT_BUTTON, self.onRemoveSerial )
		self.m_button5.Bind( wx.EVT_BUTTON, self.onReinstall )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onServices( self, event ):
		event.Skip()

	def onWebControl( self, event ):
		event.Skip()

	def onOpenBrowser( self, event ):
		event.Skip()

	def onHatControl( self, event ):
		event.Skip()

	def onConfigureHat( self, event ):
		event.Skip()

	def OnHardwareSerial( self, event ):
		event.Skip()

	def onAddSerial( self, event ):
		event.Skip()

	def onRemoveSerial( self, event ):
		event.Skip()

	def onReinstall( self, event ):
		event.Skip()


