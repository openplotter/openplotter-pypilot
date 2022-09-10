#!/usr/bin/env python3

# This file is part of OpenPlotter.
# Copyright (C) 2022 by Sailoog <https://github.com/openplotter/openplotter-pypilot>
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

import time, ssl, json
from openplotterSettings import conf
from openplotterSettings import platform
from pypilot.client import pypilotClient
from websocket import create_connection

def main():
	conf2 = conf.Conf()
	platform2 = platform.Platform()
	if conf2.get('GENERAL', 'debug') == 'yes': debug = True
	else: debug = False
	token = conf2.get('PYPILOT', 'token')
	pypilot_boatimu = conf2.get('PYPILOT', 'pypilot_boatimu')

	if pypilot_boatimu == '1':
		if token:
			ws = False
			client = False
			while True:
				try:
					time.sleep(0.25)
					if not ws:
						uri = platform2.ws+'localhost:'+platform2.skPort+'/signalk/v1/stream?subscribe=none'
						headers = {'Authorization': 'Bearer '+token}
						ws = create_connection(uri, header=headers, sslopt={"cert_reqs": ssl.CERT_NONE})
					if not client:
						client = pypilotClient()
						client.watch('imu.heading_lowpass')
						client.watch('imu.pitch')
						client.watch('imu.roll')
					result = {}
					result = client.receive()
					headingValue = None
					rollValue = None
					pitchValue = None
					keys = []
					if result:
						if 'imu.heading_lowpass' in result: headingValue = result['imu.heading_lowpass']*0.017453293
						if 'imu.roll' in result: rollValue = result['imu.roll']*0.017453293
						if 'imu.pitch' in result: pitchValue = result['imu.pitch']*0.017453293
						keys.append({"path":"navigation.headingMagnetic","value":headingValue})
						keys.append({"path":"navigation.attitude","value":{"roll":rollValue,"pitch":pitchValue,"yaw":headingValue}})
						SignalK = {"updates":[{"$source":"pypilot","values":keys}]}
						SignalK = json.dumps(SignalK) 
						ws.send(SignalK+'\r\n')
				except Exception as e: 
					if debug: print('ERROR, pypilot-read: '+str(e))
					if ws: ws.close()
					ws = False
					client = False
					time.sleep(5)

if __name__ == '__main__':
	main()
	