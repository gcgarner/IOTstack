# Zigbee2MQTT

* [Web Guide](https://www.zigbee2mqtt.io)
* [Flashing the CC2531](https://www.zigbee2mqtt.io/information/flashing_the_cc2531.html)
* [Figuring-out your device identifier](https://www.zigbee2mqtt.io/getting_started/running_zigbee2mqtt.html)

## Service definition change - April 2021

The IOTstack service definition for Zigbee2MQTT is at the following path:

```
~/IOTstack/.templates/zigbee2mqtt/service.yml
```

As of April 2021, the service definition changed:

1. The Zigbee2MQTT container no longer runs in host mode.
2. Adds timezone support.
3. Builds the container from a Dockerfile providing appropriate defaults for IOTstack.
4. Re-adds a port mapping for port 8080 (the Zigbee2MQTT web UI).

If you were running the Zigbee2MQTT service before this change, you may wish to compare and contrast your active service definition (in `docker-compose.yml`) with the revised template.

Note:

* You may need to `git pull` to update your local copy of the IOTstack repository against GitHub.

## First startup with CC2531 adapter

The service definition includes:

```
  devices:
    - /dev/ttyAMA0:/dev/ttyACM0 # should work even if no adapter
   #- /dev/ttyACM0:/dev/ttyACM0 # should work if CC2531 connected
   #- /dev/ttyUSB0:/dev/ttyACM0 # Electrolama zig-a-zig-ah! (zzh!) maybe other as well
```

The default device (`/dev/ttyAMA0`) probably will **not** work for any Zigbee adapter. It is only there because `/dev/ttyAMA0` exists on Raspberry Pis. Its presence permits the container to come up even though it will not actually be able to connect to an adapter.

If you have a CC2531, properly flashed and connected to a USB port, you should be able to see it:

```
$ ls -l /dev/ttyACM0
crw-rw---- 1 root dialout 166, 0 Apr  7 09:38 /dev/ttyACM0
``` 

> If you see the error "No such file or directory", you will need to first figure out why your device is not visible.

Assuming your CC2531 is visible:

1. Change the device mapping in `docker-compose.yml` to deactivate `ttyAMA0` in favour of activating `ttyACM0`:

	```
	  devices:
	   #- /dev/ttyAMA0:/dev/ttyACM0 # should work even if no adapter
	    - /dev/ttyACM0:/dev/ttyACM0 # should work if CC2531 connected
	   #- /dev/ttyUSB0:/dev/ttyACM0 # Electrolama zig-a-zig-ah! (zzh!) maybe other as well
	```

2. Bring up the container:

	```
	$ cd ~/IOTstack
	$ docker-compose up -d zigbee2mqtt
	```

You can also follow the instructions in the Zigbee2MQTT documentation to [work out the identifier of your device](https://www.zigbee2mqtt.io/getting_started/running_zigbee2mqtt.html) and use that instead of `/dev/ttyACM0`. Then, your `docker-compose.yml` might look something like this:

```
  devices:
   #- /dev/ttyAMA0:/dev/ttyACM0 # should work even if no adapter
   #- /dev/ttyACM0:/dev/ttyACM0 # should work if CC2531 connected
   #- /dev/ttyUSB0:/dev/ttyACM0 # Electrolama zig-a-zig-ah! (zzh!) maybe other as well
    - "/dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___xxx:/dev/ttyACM0"
```

## First startup with other adapters

Similar principles apply if you use other adapters. You must work out how the adapter presents itself on your Raspberry Pi and then map it to `/dev/ttyACM0` **inside** the container (ie the common right hand side of every device definition).

## Configuration file

### Active configuration file

Under IOTstack, the **active** configuration file for Zigbee2MQTT appears at the following path:

```
~/IOTstack/volumes/zigbee2mqtt/data/configuration.yaml
```

After you make any changes to the configuration file (using `sudo`), you need to inform the running container by:

```
$ cd ~/IOTstack
$ docker-compose restart zigbee2mqtt
```

### Default configuration file

The IOTstack version of Zigbee2MQTT is built using a Dockerfile located at:

```
~/IOTstack/.templates/zigbee2mqtt/Dockerfile
```

The Dockerfile downloads the **base** `koenkk/zigbee2mqtt` image from DockerHub and then alters the **default** configuration file as it builds a **local** image to:

* change the default MQTT server URL from "mqtt://localhost" to "mqtt://mosquitto"; and
* activate the Zigbee2MQTT web interface on port 8080.

Those changes are intended to help new IOTstack installations get started with a minimum of fuss.

However, the **default** configuration file will only become the **active** configuration file in two situations:

* On a first install of Zigbee2MQTT; or
* If you erase the container's persistent storage area. For example:

	```
	$ cd ~/IOTstack
	$ docker-compose stop zigbee2mqtt
	$ docker-compose rm -f zigbee2mqtt
	$ sudo rm -rf ./volumes/zigbee2mqtt
	$ docker-compose up -d zigbee2mqtt
	```
	
In either of those situations, the **active** configuration file will be initialised by copying the **default** configuration file into place as the container comes up.

### If you have an existing configuration file

If you have an existing **active** Zigbee2MQTT configuration file, you may need to make two changes:

1. Alter the Mosquitto URL:

	- *before:*
	
		```
		server: 'mqtt://localhost'
		```
	- *after:*
	
		```
		server: 'mqtt://mosquitto'
		```
		
2. Enable the web interface (if necessary):

	- *append:*
	
		```
		frontend:
		  port: 8080
		```

## Checking that the container is working

### Checking status

```
$ docker ps --format "table {{.Names}}\t{{.RunningFor}}\t{{.Status}}" --filter name="zigbee2mqtt"
NAMES         CREATED       STATUS
zigbee2mqtt   2 hours ago   Up 2 hours
```

You are looking for signs that the container is restarting (ie the "Status" column only ever shows a low number of seconds).

### Checking the log

```
$ docker logs zigbee2mqtt
```

You are looking for evidence of malfunction.

### Checking that Zigbee2MQTT is able to communicate with Mosquitto

If you have the Mosquitto clients installed (`sudo apt install -y mosquitto-clients`), you can run the following command:

```
$ mosquitto_sub -v -h "localhost" -t "zigbee2mqtt/#" -F "%I %t %p"
```

One of two things will happen:

* *silence,* indicating that Zigbee2MQTT is **not** able to communicate with Mosquitto.
* *chatter,* proving that Zigbee2MQTT **can** communicate with Mosquitto.

Terminate the `mosquitto_sub` command with a Control-C.

### Checking that the Zigbee2MQTT web GUI is working

Open a browser, and point it to port 8080 on your Raspberry Pi. You should see the Zigbee2MQTT interface.

### terminal access inside the container

To access the terminal run:

```
$ docker exec -it zigbee2mqtt ash
```

> `ash` is **not** a typo!

When you want to leave the container, either type `exit` and press return, or press Control-D.

## Setting a password for the web interface

By default, the web interface is unprotected. If you want to set a password:

1. Use `sudo` to edit the active configuration file at the path:

	```
	~/IOTstack/volumes/zigbee2mqtt/data/configuration.yaml
	```

2. Find the following text:

	```
	frontend:
	  port: 8080
	# auth_token: PASSWORD
	```
	
3. Uncomment the `auth_token` line and replace "PASSWORD" with the password of your choice. For example, to set the password to "mypassword":

	```
	  auth_token: mypassword
	```
	
	Note:
	
	* although the name `auth_token` suggests something more complex, it really is no more than a simple *en-clear* password. If this concerns you, consider disabling the web front-end entirely, like this:
	
		```
		#frontend:
		# port: 8080
		# auth_token: PASSWORD
		```

4. Save the file and restart the container:

	```
	$ cd ~/IOTstack
	$ docker-compose restart zigbee2mqtt
	```

## Container maintenance

Because the Zigbee2MQTT container is built from a Dockerfile, a normal `pull` command will not automatically download any updates released on DockerHub.

When you become aware of a new version of Zigbee2MQTT being released on DockerHub, do the following:

```
$ cd ~IOTstack
$ docker-compose build --no-cache --pull zigbee2mqtt
$ docker-compose up -d zigbee2mqtt
$ docker system prune
```

Note:

* Sometimes it is necessary to repeat the `docker system prune` command.
