## openplotter-pypilot

OpenPlotter app to integrate Pypilot in Raspberry Pi

### Installing

#### For production

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **production** and just install this app from *OpenPlotter Apps* tab.

#### For development

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **development**.

Install openplotter-pypilot dependencies:

`sudo apt install swig python3-opengl python3-serial libpython3-dev python3-numpy python3-scipy python3-ujson python3-pyudev python3-pil python3-flask python3-flask-socketio python3-pip`

Clone the repository:

`git clone https://github.com/openplotter/openplotter-pypilot`

Install:

`cd openplotter-pypilot
sudo python3 setup.py install`

Run post-installation script:

`sudo pypilotPostInstall`

Run:

`openplotter-pypilot`

Make your changes and repeat installation and post-installation steps to test. Pull request your changes to github and we will check and add them to the next version of the [Debian package](https://launchpad.net/~openplotter/+archive/ubuntu/openplotter/).

### Documentation

https://openplotter.readthedocs.io

### Support

http://forum.openmarine.net/forumdisplay.php?fid=1
