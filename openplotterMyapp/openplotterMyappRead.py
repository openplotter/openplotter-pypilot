#!/usr/bin/env python

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
import socket, time, random
from openplotterSettings import conf

# this file runs as a service in the background
def main():
	try:
		conf2 = conf.Conf()
		value = conf2.get('MYAPP', 'sending')
		port = conf2.get('MYAPP', 'myappConn1')
		if value == '1':
			# this script sends data to Signal K servers by an UDP connection in client mode
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			while True:
				random1 = random.randint(1,101)
				random2 = random.randint(1,101)
				values = '{"path": "Random.Number1","value":'+str(random1)+'},'
				values += '{"path": "Random.Number2","value":'+str(random2)+'}'	
				SignalK = '{"updates":[{"$source":"OpenPlotter.Dummy","values":['+values+']}]}\n'		
				sock.sendto(SignalK.encode('utf-8'), ('127.0.0.1', int(port)))
				time.sleep(1)
	except Exception as e: print (str(e))

if __name__ == '__main__':
	main()