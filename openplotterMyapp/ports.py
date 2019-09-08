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
import os
from openplotterSettings import language

# Here you have to define all the TCP/UDP connections on localhost managed by your app so that the main app can wtch for conflicts. Use this format:
#
# {'id':'uniqueId', description':_('My App'), 'data':_('Signal K keys:')+'Random.Number1, Random.Number2', 'direction':'1/2/3', 'type':'UDP/TCP', 'mode':'client/server', 'address':'localhost', 'port':000000, 'editable':'1'}
#
# id (text, required): any unique id 
# description (text, required): use translatable text
# data (text, optional): details about the data like signal k key, NMEA sentences or PGN...
# direction (text, optional): 1= in, 2=out, 3=both
# type (text, required): TCP or UDP
# mode (text, required): client or server. Normally you can only set one TCP/UDP server for the same port. You can define multiple TCP/UDP clients for the same port. 
# Clients and servers can send and receive data. A UDP connection listenning on any port will be a server. A UDP connection just sending data to any port will be a client. 
# A TCP connection listenning on any port can be client or server
# address (text, required): this should always be localhost
# port (number, required): the port where the connections is set
# editable (text, optional): if your app provide a way of changing the port, set this value to '1'
class Ports:
	def __init__(self,conf,currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-myapp',currentLanguage)
		# here you have to define what connections will be always present in your app
		self.connections = []
		connectionId = 'myappConn1'
		try: port = int(self.conf.get('MYAPP', connectionId))
		except: port = 50000 #default port
		self.connections.append({'id':connectionId, 'description':_('My App'), 'data':_('Signal K keys: ')+'Random.Number1, Random.Number2', 'direction':'2', 'type':'UDP', 'mode':'client', 'address':'localhost', 'port':port, 'editable':'1'})

	def usedPorts(self):
		# here you have to define what connections are enabled when this function is called to check servers conflicts or provide a list of the enabled connections in your system.
		state = self.conf.get('MYAPP', 'sending')
		if state == '1': return self.connections
