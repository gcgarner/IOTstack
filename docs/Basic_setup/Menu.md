The `menu.sh`-script is used to create or modify the `docker-compose.yml`-file.
This file defines how all containers added to the stack are configured.

## Miscellaneous

### log2ram

One of the drawbacks of an sd card is that it has a limited lifespan. One way
to reduce the load on the sd card is to move your log files to RAM. [log2ram](
https://github.com/azlux/log2ram) is a convenient tool to simply set this up.
It can be installed from the miscellaneous menu.

This only affects logs written to /var/log, and won't have any effect on Docker
logs or logs stored inside containers.

### Dropbox-Uploader
This a great utility to easily upload data from your PI to the cloud. The
[MagPi](https://magpi.raspberrypi.org/articles/dropbox-raspberry-pi) has an
excellent explanation of the process of setting up the Dropbox API.
Dropbox-Uploader is used in the backup script.

## Backup and Restore

See [Backing up and restoring IOTstack](Backup-and-Restore.md)

## Native Installs

### RTL_433
RTL_433 can be installed from the "Native install sections"

[This video](https://www.youtube.com/watch?v=L0fSEbGEY-Q&t=386s) demonstrates
how to use RTL_433

### RPIEasy

The installer will install any dependencies. If `~/rpieasy` exists it will
update the project to its latest, if not it will clone the project

RPIEasy can be run by `sudo ~/rpieasy/RPIEasy.py`

To have RPIEasy start on boot in the webui under hardware look for "RPIEasy
autostart at boot"

RPIEasy will select its ports from the first available one in the list
(80,8080,8008). If you run Hass.io then there will be a conflict so check the
next available port

## Old-menu branch details
The build script creates the ./services directory and populates it from the
template file in .templates . The script then appends the text withing each
service.yml file to the docker-compose.yml . When the stack is rebuilt the menu
does not overwrite the service folder if it already exists. Make sure to sync
any alterations you have made to the docker-compose.yml file with the
respective service.yml so that on your next build your changes pull through.

The .gitignore file is setup such that if you do a `git pull origin master` it
does not overwrite the files you have already created. Because the build script
does not overwrite your service directory any changes in the .templates
directory will have no affect on the services you have already made. You will
need to move your service folder out to get the latest version of the template.
