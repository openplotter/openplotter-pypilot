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
import socket, time, subprocess, sys
from signalk.client import SignalKClient

def main():

	def on_con(client):
		print('conected to pypilot Signal K server')
		client.watch('imu.heading_lowpass')
		client.watch('imu.pitch')
		client.watch('imu.roll')

	try:
		subprocess.check_output(['systemctl', 'is-enabled', 'pypilot_boatimu']).decode(sys.stdin.encoding)
		pypilot_boatimu = True
	except: pypilot_boatimu = False

	try:
		subprocess.check_output(['systemctl', 'is-enabled', 'pypilot']).decode(sys.stdin.encoding)
		pypilot = True
	except: pypilot = False

	if pypilot_boatimu or pypilot:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client = False
		while True:
			time.sleep(0.5)
			try:
				if not client:
					client = SignalKClient(on_con, 'localhost')
			except:
				time.sleep(3)
				continue
			try:
				result = client.receive()
			except:
				print('disconnected from pypilot Signal K server')
				client = False
				continue

			headingValue = ''
			rollValue = ''
			pitchValue = ''
			values = ''
			for i in result:
				if 'imu.heading_lowpass' in i: headingValue = result[i]['value']*0.017453293
				if 'imu.roll' in i: rollValue = result[i]['value']*0.017453293
				if 'imu.pitch' in i: pitchValue = result[i]['value']*0.017453293
				
			if headingValue and rollValue and pitchValue:
				if pypilot_boatimu: 
					values += '{"path": "navigation.headingMagnetic","value":'+str(headingValue)+'}'
					values += ','
				values += '{"path": "navigation.attitude","value":{"roll":'+str(rollValue)+',"pitch":'+str(pitchValue)+',"yaw":null}}'

				SignalK = '{"updates":[{"$source":"OpenPlotter.I2C.pypilot","values":['+values+']}]}\n'
				sock.sendto(SignalK.encode('utf-8'), ('127.0.0.1', 20220))

if __name__ == '__main__':
	main()

'''
import socketserver, time, sys, subprocess
from signalk.client import SignalKClient

class MyTCPHandler(socketserver.BaseRequestHandler):

	def handle(self):

		def nmea_cksum(msg):
			value = 0
			for c in msg:
				value ^= ord(c)
			return value & 255
	
		def send_nmea(msg):
			line = '$' + msg + ('*%02X' % nmea_cksum(msg)) + '\r\n'
			self.request.sendall(line.encode())

		def on_con(client):
			print('conected to pypilot Signal K server')
			client.watch('imu.heading')
			client.watch('imu.pitch')
			client.watch('imu.roll')

		client = False
		while True:
			time.sleep(0.5)
			try:
				if not client:
					client = SignalKClient(on_con, 'localhost')
			except:
				time.sleep(3)
				continue
			try:
				result = client.receive()
			except:
				print('disconnected from pypilot Signal K server')
				client = False
				continue
			headingValue = ''
			rollValue = ''
			pitchValue = ''
			for i in result:
				if 'imu.heading' in i: headingValue = result[i]['value']
				if 'imu.roll' in i: rollValue = result[i]['value']
				if 'imu.pitch' in i: pitchValue = result[i]['value']

			if pitchValue: send_nmea('APXDR,A,%.3f,D,PTCH' % pitchValue)
			if rollValue: send_nmea('APXDR,A,%.3f,D,ROLL' % rollValue)
			if headingValue: send_nmea('APHDM,%.3f,M' % headingValue)

def main():
	HOST, PORT = "localhost", 20220
	with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
		server.serve_forever()

if __name__ == "__main__":
	main()
'''