## openplotter-pypilot

OpenPlotter app to integrate Pypilot in Raspberry Pi

### Installing

#### For production

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **production** and just install this app from *OpenPlotter Apps* tab.

#### For development

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **development**.

Install openplotter-pypilot dependencies:

`sudo apt install python-gps python-serial libpython-dev python-numpy python-scipy swig python-ujson python-pyudev python-pil python-flask python-gevent-websocket python-wxgtk3.0 python-opengl python-pyglet python-pip`

`sudo pip install pywavefront`

Install Pypilot:

`git clone https://github.com/pypilot/pypilot
git clone https://github.com/pypilot/pypilot_data
cp -rv pypilot_data/* pypilot
cd pypilot
python setup.py build
sudo python setup.py install`

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
