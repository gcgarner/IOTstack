# deCONZ
## References
- [Docker](https://hub.docker.com/r/marthoc/deconz)
- [Website](https://github.com/dresden-elektronik/deconz-rest-plugin/blob/master/README.md)

## Accessing Phoscon ui
deCONZ should now be available at http://ip.address.of.your.IOTstack.pc.here:8090/

## Viewing the deCONZ Zigbee mesh
The Zigbee mesh can be viewed using VNC (port 5901). The default VNC password is "changeme".

## Connecting deCONZ and Node-RED
1) Install [node-red-contrib-deconz](https://flows.nodered.org/node/node-red-contrib-deconz) via the manage palette menu (if not already pre-installed with Node-RED)
2) Open a deCONZ in node, select "Add new deconz-server" and type in the IP-address of your IOTstack pc (Rpi) and type in port 8090 (not websocket port)
3) Open deCONZ (http://ip.address.of.your.IOTstack.pc.here:8090/) and open settings>gateway>advanced. Click "Authenticate app".
4) Go back to your Node-RED instance and click the magick:get setting button in the server node. The API and websocket port will be automatically inserted. Click "Add" and you are good to go.

![installing deCONZ](https://github.com/DIYtechie/resources/blob/master/images/deconz%20authenticate.png?raw=true)
![installing deCONZ](https://github.com/DIYtechie/resources/blob/master/images/deconz%20node%20red%20config.png?raw=true)
