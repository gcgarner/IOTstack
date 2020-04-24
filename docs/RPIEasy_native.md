# RPIEasy
RPIEasy can now be installed under the native menu

The installer will install any dependencies. If `~/rpieasy` exists it will update the project to its latest, if not it will clone the project

## Running Running RPIEasy

RPIEasy can be run by `sudo ~/rpieasy/RPIEasy.py`

To have RPIEasy start on boot in the webui under hardware look for "RPIEasy autostart at boot"

## Ports

RPIEasy will select its ports from the first available one in the list (80,8080,8008). If you run Hass.io then there will be a conflict so check the next available port