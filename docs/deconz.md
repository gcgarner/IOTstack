# deCONZ
## References
- [Docker](https://hub.docker.com/r/marthoc/deconz)
- [Website](https://github.com/dresden-elektronik/deconz-rest-plugin/blob/master/README.md)

## Installing Phoscon (the part of deCONZ that lets you add devices and setup the gateway)
All devices are commented out of the docker-compose template by default to avoid errors. After adding deCONZ to the stack, comment in your device and physically plug in the relevant device (e.g. ConBee II) BEFORE running `docker-compose up -d` again.



## Viewing the Zigbee mesh
The Zigbee mesh can be seen using VNC (port 8090). The default password is "changeme".

By default, VNC container has no password. You can leave it that way if you like but its always a good idea to secure your services.

## Connecting deCONZ and Node-RED
(port 8090)

Step 2
Edit the file called services/mosquitto/mosquitto.conf and remove the comment in front of password_file. Restart the container with `docker-compose restart mosquitto`. Type those credentials into Node-red etc.
