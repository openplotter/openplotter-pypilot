## openplotter-pypilot

OpenPlotter app to integrate Pypilot in Raspberry Pi

### Installing

#### For production

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **production** and just install this app from *OpenPlotter Apps* tab.

#### For development

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **development**.

Install openplotter-pypilot dependencies:

`sudo apt install swig python3-opengl python3-serial libpython3-dev python3-numpy python3-scipy python3-ujson python3-pyudev python3-pil python3-flask python3-pip`

`sudo pip3 install pywavefront pyglet gps gevent-websocket`

Install Pypilot:

`git clone https://github.com/pypilot/pypilot
git clone https://github.com/pypilot/pypilot_data
cp -rv pypilot_data/* pypilot
cd pypilot
python3 setup.py build
sudo python3 setup.py install`

Clone the repository:

`git clone https://github.com/openplotter/openplotter-pypilot`

Make your changes and install:

`sudo python3 setup.py install`

Run:

`openplotter-pypilot`

Pull request your changes to github and we will check and add them to the next version of the [Debian package](https://launchpad.net/~openplotter/+archive/ubuntu/openplotter/).

### Documentation

https://openplotter.readthedocs.io

### Support

http://forum.openmarine.net/forumdisplay.php?fid=1
