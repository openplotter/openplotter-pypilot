## openplotter-pypilot

OpenPlotter app to integrate Pypilot in Raspberry Pi

### Installing

#### For production

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **production** and just install this app from *OpenPlotter Apps* tab.

#### For development

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **development**.

```
git clone https://github.com/openplotter/openplotter-pypilot
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

Run openplotter-pypilot

```
openplotter-pypilot
```

Make your changes and repeat package, installation and post-installation steps to test. Pull request your changes to github and we will check and add them to the next version of the [Debian package](https://launchpad.net/~openplotter/+archive/ubuntu/openplotter).

### Documentation

https://openplotter.readthedocs.io

### Support

http://forum.openmarine.net/forumdisplay.php?fid=1
