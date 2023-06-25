# deCONZ

## References
- [Docker](https://hub.docker.com/r/marthoc/deconz)
- [Website](https://github.com/dresden-elektronik/deconz-rest-plugin/blob/master/README.md)

## Setup

### Old menu (old menu branch)

If you use "old menu", you may get an error message similar to the following on first launch:

```
parsing ~/IOTstack/docker-compose.yml: error while interpolating services.deconz.devices.[]: required variable DECONZ_DEVICE_PATH is missing a value: eg echo DECONZ_DEVICE_PATH=/dev/serial0 >>~/IOTstack/.env
```

The message is telling you that you need to define the path to your deCONZ device. Common examples are:

- Raspbee at `/dev/serial0`
- Conbee at `/dev/ttyUSB0`
- Conbee II at `/dev/ttyACM0`

Once you have identified the appropriate device path, you can define it like this:

```console
$ echo DECONZ_DEVICE_PATH=/dev/serial0 >>~/IOTstack/.env
```

This example uses `/dev/serial0`. Substitute your actual device path if it is different. 

### New menu (master branch)

New menu offers a sub-menu (place the cursor on `deconz` and press the right arrow) where you can select the appropriate device path.

## Dialout group

Before running `docker-compose up -d`, make sure your Linux user is part of the dialout group, which allows the user access to serial devices (i.e. Conbee/Conbee II/RaspBee). If you are not certain, simply add your user to the dialout group by running the following command (username "pi" being used as an example):

```console
$ sudo usermod -a -G dialout pi
```

## Troubleshooting

Your Conbee/Conbee II/RaspBee gateway must be plugged in when the deCONZ Docker container is being brought up. If your gateway is not detected, or no lights can be paired, try moving the device to another usb port. A reboot may help too.

Use a 0.5-1m usb extension cable with ConBee (II) to avoid wifi and bluetooth noise/interference from your Raspberry Pi (recommended by the manufacturer and often the solution to poor performance).

## Accessing the Phoscon UI
The Phoscon UI is available using port 8090 (http://your.local.ip.address:8090/)

## Viewing the deCONZ Zigbee mesh
The Zigbee mesh can be viewed using VNC on port 5901. The default VNC password is "changeme".

## Connecting deCONZ and Node-RED
Install [node-red-contrib-deconz](https://flows.nodered.org/node/node-red-contrib-deconz) via the "Manage palette" menu in Node-RED (if not already installed) and follow these 2 simple steps (also shown in the video below):

Step 1: In the Phoscon UI, Go to Settings > Gateway > Advanced and click "Authenticate app".

Step 2: In Node-RED, open a deCONZ node, select "Add new deonz-server", insert your ip adress and port 8090 and click "Get settings".  Click "Add", "Done" and "Deploy". Your device list will not be updated before deploying.


![installing deCONZ](https://github.com/DIYtechie/resources/blob/master/images/Setup%20deCONZ%20in%20Node-RED.gif?raw=true)
