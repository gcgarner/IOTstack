# deCONZ
## References
- [Docker](https://hub.docker.com/r/marthoc/deconz)
- [Website](https://github.com/dresden-elektronik/deconz-rest-plugin/blob/master/README.md)

## Pre-installation
Before running the command that creates the deconz Docker container (`docker-compose up -d`), you may need to add your Linux user to the dialout group, which allows the user access to serial devices (i.e. Conbee/Conbee II/RaspBee):

`sudo usermod -a -G dialout pi` (pi user being used as an example)

## Accessing the Phoscon UI
The Phoscon UI is available using port 8090 (http://your.local.ip.address:8090/)

## Viewing the deCONZ Zigbee mesh
The Zigbee mesh can be viewed using VNC (port 5901). The default VNC password is "changeme".

## Connecting deCONZ and Node-RED
Install [node-red-contrib-deconz](https://flows.nodered.org/node/node-red-contrib-deconz) via the "Manage palette" menu in Node-RED (if it is not already pre-installed) and follow the 2 simple steps in the video below:

![installing deCONZ](https://github.com/DIYtechie/resources/blob/master/images/Setup%20deCONZ%20in%20Node-RED.gif?raw=true)
