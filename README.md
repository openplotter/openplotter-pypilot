## openplotter-pypilot

OpenPlotter app to integrate Pypilot.

### Installing

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **production**.

#### For production

Install Pypilot from openplotter-settings app.

#### For development

Clone the repository:

`git clone https://github.com/openplotter/openplotter-pypilot`

Make your changes and create the package:

```
cd openplotter-pypilot
dpkg-buildpackage -b
```

Install the package:

```
cd ..
sudo dpkg -i openplotter-pypilot_x.x.x-xxx_all.deb
```

Run post-installation script:

`sudo pypilotPostInstall`

Run openplotter-pypilot:

```
openplotter-pypilot
```

Pull request your changes to github and we will check and add them to the next version of the [Debian package](https://cloudsmith.io/~openplotter/repos/openplotter/packages/).

### Documentation

https://openplotter.readthedocs.io

### Support

http://forum.openmarine.net/forumdisplay.php?fid=1