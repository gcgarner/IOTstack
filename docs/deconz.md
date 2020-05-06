# deCONZ
## References
- [Docker](https://hub.docker.com/r/marthoc/deconz)
- [Website](https://github.com/dresden-elektronik/deconz-rest-plugin/blob/master/README.md)

## Installing deCONZ
1) Plug in you ConBee II, ConBee or Raspbee (if no device is plugged in, deCONZ will not be properly installed)
2) Add deCONZ to your stack using `cd ~/IOTstack && bash ./menu.sh`and select deCONZ
3) Edit the deconz service.yml using `sudo nano ~/IOTstack/services/deconz/service.yml` - activate your device by removing the "#" in front of "devices" and the "#" in front of your specific device. Save the changes using "ctrl+x", "y" and "enter".
4) Build the stack again using `cd ~/IOTstack && bash ./menu.sh` to apply the changes and select "Do not overwrite".
5) Run `docker-compose up -d` to build the deCONZ container.

These steps are also shown in the gif below:

![installing deCONZ](https://github.com/DIYtechie/resources/blob/master/images/installing%20deconz%20-%20short%20version.gif?raw=true)

deCONZ should now be available at http://<ip-address-of-your-IOTstack-pc-here>:8090/

## Viewing the deCONZ Zigbee mesh
The Zigbee mesh can be viewed using VNC (port 5901). The default VNC password is "changeme".

## Connecting deCONZ and Node-RED
1) Install [node-red-contrib-deconz](https://flows.nodered.org/node/node-red-contrib-deconz) via the manage palette menu (if not already pre-installed with Node-RED)
2) Open a deCONZ in node, select "Add new deconz-server" and type in the IP-address of your IOTstack pc (Rpi) and type in port 8090 (not websocket port)
3) Open deCONZ (http://<ip-address-of-your-IOTstack-pc-here>:8090/) and open settings>gateway>advanced. Click "Authenticate app".
4) Go back to your Node-RED instance and click the magick:get setting button in the server node. The API and websocket port will be automatically inserted. Click "Add" and you are good to go.

![installing deCONZ](https://github.com/DIYtechie/resources/blob/master/images/deconz%20authenticate.png?raw=true)
![installing deCONZ](https://github.com/DIYtechie/resources/blob/master/images/deconz%20node%20red%20config.png?raw=true)
