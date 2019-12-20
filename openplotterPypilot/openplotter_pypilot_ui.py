# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Nov  2 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx, os
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class openplotter_pypilotBase
###########################################################################

class openplotter_pypilotBase ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 700,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.currentdir = os.path.dirname(os.path.abspath(__file__))

		fgSizer1 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_toolBar1 = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL|wx.TB_TEXT )
		self.m_tool1 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Help"), wx.Bitmap( self.currentdir+"/data/help.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_tool4 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Client"), wx.Bitmap( self.currentdir+"/data/edit.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_tool5 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Scope"), wx.Bitmap( self.currentdir+"/data/connections.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_tool6 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Calibration"), wx.Bitmap( self.currentdir+"/data/settings.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_tool8 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Control"), wx.Bitmap( self.currentdir+"/data/heading.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_toolBar1.AddSeparator()

		self.m_tool3 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, _(u"Ok"), wx.Bitmap( self.currentdir+"/data/apply.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.m_toolBar1.Realize()

		fgSizer1.Add( self.m_toolBar1, 0, wx.EXPAND, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Detected IMU"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer3.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.stDetected = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"none"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stDetected.Wrap( -1 )

		fgSizer3.Add( self.stDetected, 0, wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Mode"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )

		cModeChoices = [ _(u"disable"), _(u"imu"), _(u"autopilot") ]
		self.cMode = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cModeChoices, 0 )
		self.cMode.SetSelection( 0 )
		fgSizer3.Add( self.cMode, 0, wx.ALL, 5 )

		self.cbOutputSignalKNode = wx.CheckBox( self.m_panel3, wx.ID_ANY, _(u"output to signalk node"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.cbOutputSignalKNode, 0, wx.ALL, 5 )

		fgSizer5 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		fgSizer3.Add( fgSizer5, 1, wx.EXPAND, 5 )

		self.cbWebApp = wx.CheckBox( self.m_panel3, wx.ID_ANY, _(u"Browser Control"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.cbWebApp, 0, wx.ALL, 5 )

		fgSizer6 = wx.FlexGridSizer( 1, 0, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText10 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"port"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		fgSizer6.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.m_staticText71 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"8000"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		fgSizer6.Add( self.m_staticText71, 0, wx.ALL, 5 )

		self.m_button2 = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Open"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.m_button2, 0, wx.ALL, 5 )


		fgSizer3.Add( fgSizer6, 1, wx.EXPAND, 5 )

		self.cbLCDControl = wx.CheckBox( self.m_panel3, wx.ID_ANY, _(u"LCD keypad/remote control"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.cbLCDControl, 0, wx.ALL, 5 )

		self.m_button1 = wx.Button( self.m_panel3, wx.ID_ANY, _(u"?"), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button1, 0, wx.ALL, 5 )


		self.m_panel3.SetSizer( fgSizer3 )
		self.m_panel3.Layout()
		fgSizer3.Fit( self.m_panel3 )
		self.m_notebook1.AddPage( self.m_panel3, _(u"Settings"), True )
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook1.AddPage( self.m_panel4, _(u"Console"), False )

		fgSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


		fgSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( fgSizer1 )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.OnToolHelp, id = self.m_tool1.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnToolClient, id = self.m_tool4.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnToolScope, id = self.m_tool5.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnToolCalibration, id = self.m_tool6.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnToolControl, id = self.m_tool8.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnToolOK, id = self.m_tool3.GetId() )
		self.cMode.Bind( wx.EVT_CHOICE, self.OnMode )
		self.cbOutputSignalKNode.Bind( wx.EVT_CHECKBOX, self.OnOutputSignalKNode )
		self.cbWebApp.Bind( wx.EVT_CHECKBOX, self.OnWebApp )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnOpenWebControl )
		self.cbLCDControl.Bind( wx.EVT_CHECKBOX, self.OnLCDKeypad )
		self.m_button1.Bind( wx.EVT_BUTTON, self.OnAboutLCDKeypad )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnToolHelp( self, event ):
		event.Skip()

	def OnToolClient( self, event ):
		event.Skip()

	def OnToolScope( self, event ):
		event.Skip()

	def OnToolCalibration( self, event ):
		event.Skip()

	def OnToolControl( self, event ):
		event.Skip()

	def OnToolOK( self, event ):
		event.Skip()

	def OnMode( self, event ):
		event.Skip()

	def OnOutputSignalKNode( self, event ):
		event.Skip()

	def OnWebApp( self, event ):
		event.Skip()

	def OnOpenWebControl( self, event ):
		event.Skip()

	def OnLCDKeypad( self, event ):
		event.Skip()

	def OnAboutLCDKeypad( self, event ):
		event.Skip()


