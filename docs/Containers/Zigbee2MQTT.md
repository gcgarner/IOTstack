# Zigbee2MQTT

## Quick links

* New users: [start here](#basicProcess)
* Existing users: [Service definition change](#update202204) (circa April 2022)

## References

* [Web Guide](https://www.zigbee2mqtt.io)
* [Supported adapters](https://www.zigbee2mqtt.io/guide/adapters/#recommended)
* [GitHub](https://github.com/Koenkk/zigbee2mqtt)
* [DockerHub](https://hub.docker.com/r/koenkk/zigbee2mqtt/tags)

## Definitions

* *"compose file"* means the file at the path:

	```
	~/IOTstack/docker-compose.yml
	```

## Basic process for new users { #basicProcess }

1. Run the IOTstack menu and choose both "Mosquitto" and "Zigbee2MQTT". That adds the service definitions for both of those containers to your *compose file*.

2. [Prepare your Zigbee adapter](#prepareAdapter) by flashing its firmware.
3. Follow the steps in [Identify your Zigbee adapter](#identifyAdapter) to work out how your adapter "mounts" on your Raspberry Pi, and edit your *compose file* to include that information.
4. The default environment variables assume:

	- You are running Mosquitto and Zigbee2MQTT as IOTstack containers on the same computer; and
	- You want the Zigbee2MQTT web front end to be available on port 8080.

	This is a good basis for getting started. If it sounds like it will meet your needs, you will not need to make any changes. Otherwise, review the [environment variables](#envVars) and make appropriate changes to the service definition in your *compose file*.

5. Bring up your stack: { #upStack }

	```console
	$ cd ~/IOTstack
	$ docker-compose up -d
	```

6. Confirm that the Zigbee2MQTT container appears to be working correctly. You should:

	* [Check container status](#checkStatus) to confirm that the container is running and stable, and is not in a restart loop;
	* [Check the container's log](#checkLog) for any errors, warnings or other evidence of malfunction; and
	* [Check inter-container connectivity](#checkMQTT) by verifying that the Zigbee2MQTT container is publishing MQTT messages to the Mosquitto broker.

7. [Connect to the web front end](#connectGUI) and start adding your Zigbee devices.

## Prepare your Zigbee adapter { #prepareAdapter }

Zigbee adapters usually need to be "flashed" before they can be used by Zigbee2MQTT. To prepare your adatper:

1. Go to the [supported adapters](https://www.zigbee2mqtt.io/guide/adapters/#recommended) page.
2. Find your adapter in the list.
3. Follow the instructions for flashing your adapter.

Note:

* If you can't find your adapter in the list of supported devices, you may not be able to get the Zigbee2MQTT container to connect to it. This kind of problem is outside the scope of IOTstack. You will have to raise the issue with the [Zigbee2MQTT](https://www.zigbee2mqtt.io) project.

## Identify your Zigbee adapter { #identifyAdapter }

This section covers adapters that connect to your Raspberry Pi via USB.

> See [connect to a remote adapter](https://www.zigbee2mqtt.io/advanced/remote-adapter/connect_to_a_remote_adapter.html) for information on connecting to adapters via TCP.

Many USB Zigbee adapters mount as `/dev/ttyACM0` but this is not true for *all* adapters. In addition, if you have multiple devices connected to your Raspberry Pi that contend for a given device name, there are no guarantees that your Zigbee adapter will *always* be assigned the *same* name each time the device list is enumerated.

For those reasons, it is better to take the time to identify your Zigbee adapter in a manner that will be predictable, unique and reliable:

1. If your Zigbee adapter is connected to your Raspberry Pi, disconnect it.
2. Run the following command (the option is the digit "1"):

	```console
	$ ls -1 /dev/serial/by-id
	```

	The possible response patterns are:

	* An error message:

		```
		ls: cannot access '/dev/serial/by-id': No such file or directory
		```

	* A list of one or more lines where your Zigbee adapter is **not** present. Example:

		```
		usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_f068b8e7e82d4b119c0ee71fa1143ea0-if00-port0
		```

	The actual response (error, or a list of devices) does not matter. You are simply establishing a baseline.

3. Connect your prepared Zigbee adapter to a USB port on your Raspberry Pi.
4. Repeat the same `ls` command from step 2. The response pattern should be different from step 2. The list should now contain your Zigbee adapter. Example:

	```
	usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_f068b8e7e82d4b119c0ee71fa1143ea0-if00-port0
	usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00125A00183F06C5-if00
	```

	The second line indicates a CC2531 adapter is attached to the Raspberry Pi.

	If the response pattern does **not** change, it means the Raspberry Pi is unable to see your adapter. The two most common reasons are:
	
	1. Your adapter was not flashed correctly. Start over at [prepare your Zigbee adapter](#prepareAdapter).
	2. Your adapter does not mount as a serial device. Try repeating steps 2 through 4 with the command:

		```console
		$ ls -1 /dev
		```
		
		to see if you can discover how your adapter attaches to your Raspberry Pi.
		
		> One example is the Electrolama zig-a-zig-ah which attaches as `/dev/ttyUSB0`.

5. Use the output from the `ls` command in step 4 to form the absolute path to your Zigbee adapter. Example:

	```
	/dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00125A00183F06C5-if00
	```

6. Check your work like this (the option is the lower-case letter "l"):

	```console
	$ ls -l /dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00125A00183F06C5-if00
	lrwxrwxrwx 1 root root 13 Mar 31 19:49 dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00125A00183F06C5-if00 -> ../../ttyACM0
	```

	What the output is telling you is that the *by-id* path is a symbolic link to `/dev/ttyACM0`. Although this *may* always be true on your Raspberry Pi, the only part that is actually *guaranteed* to be true is the *by-id* path, which is why you should use it.

7. Once you have identified the path to your adapter, you communicate that information to docker-compose like this:

	```console
	$ echo ZIGBEE2MQTT_DEVICE_PATH=/dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00125A00183F06C5-if00 >>~/IOTstack/.env
	```

	Note:
	
	* if you forget to do this step, docker-compose will display the following error message:

		```
		parsing ~/IOTstack/docker-compose.yml: error while interpolating services.zigbee2mqtt.devices.[]: required variable ZIGBEE2MQTT_DEVICE_PATH is missing a value: eg echo ZIGBEE2MQTT_DEVICE_PATH=/dev/ttyACM0 >>~/IOTstack/.env
		```

8. Continue from [bring up your stack](#upStack).

## Configuration { #configuration }

### Environment variables { #envVars }

Any value that can be set in a Zigbee2MQTT [configuration file](#confFile) can also be set using an environment variable.

> The [Zigbee2MQTT documentation](https://www.zigbee2mqtt.io/guide/configuration/#environment-variables) explains the syntax.

Note:

* Do **not** use quote marks to enclose the values (right hand sides) of environment variables.

Whenever you change the value of an environment variable, you also need to tell `docker-compose` to apply the change:

```console
$ cd ~/IOTstack
$ docker-compose up -d zigbee2mqtt
```

The default service definition provided with IOTstack includes the following environment variables:

* `ZIGBEE2MQTT_CONFIG_MQTT_SERVER=mqtt://mosquitto:1883` { #mqttServer }

	Typical values for this are:

	- `mqtt://mosquitto:1883`

		This is default value supplied with the IOTstack template. It assumes that both Zigbee2MQTT and the Mosquitto broker are running in non-host mode containers on the same Raspberry Pi.

	- `mqtt://localhost:1883`

		This would be appropriate if you were to run Zigbee2MQTT in host mode and the Mosquitto broker was running on the same Raspberry Pi.

	- `mqtt://«host-or-ip»:1883`

		If the Mosquitto broker is running on a *different* computer, replace `«host-or-ip»` with the IP address or domain name of that other computer. You should also remove or comment-out the following lines from the service definition:

		```yaml
		depends_on:
		  - mosquitto
		```

		The `depends_on` clause ensures that the Mosquitto container starts alongside the Zigbee2MQTT container. That would not be appropriate if Mosquitto was running on a separate computer.
	
* `ZIGBEE2MQTT_CONFIG_FRONTEND=true` { #frontEndEnable }

	This variable activates the Zigbee2MQTT web interface on port 8080. If you want to change the port number where you access the Zigbee2MQTT web interface, see [connecting to the web GUI](#connectGUI).

* `ZIGBEE2MQTT_CONFIG_ADVANCED_LOG_SYMLINK_CURRENT=true` { #logSymlink }

	Defining this variable causes Zigbee2MQTT to create a symlink pointing to the current log **folder** at the path:

	```
	~/IOTstack/volumes/zigbee2mqtt/data/log/current
	```

	See [Checking the log](#checkLog) for more information about why this is useful.
	
* `- DEBUG=zigbee-herdsman*` { #enableDebug }

	Enabling this variable turns on extended debugging inside the container.

### Configuration file { #confFile }

Zigbee2MQTT creates a default configuration file at the path:

```
~/IOTstack/volumes/zigbee2mqtt/data/configuration.yaml
```

Although you *can* edit the configuration file, the approach recommended for IOTstack is to use [environment variables](#envVars).

If you decide to edit the configuration file:

1. You will need to use `sudo` to edit the file.
2. After you have finished making changes, you need to inform the running container by:

	```console
	$ cd ~/IOTstack
	$ docker-compose restart zigbee2mqtt
	```

3. [Check the log](#checkLog) for errors.

Note:

* If you start Zigbee2MQTT from a clean slate (ie where the configuration file does not exist) **and** your *compose file* does not define the [`… MQTT_SERVER`](#mqttServer) environment variable discussed above, the container will go into a restart loop. This happens because the Zigbee2MQTT container defaults to trying to reach the Mosquitto broker at `localhost:1883` instead of `mosquitto:1883`. That usually fails.

## Verifying basic operation { #verifyOperation }

### Checking status { #checkStatus }

```console
$ docker ps | grep -e mosquitto -e zigbee2mqtt
NAMES         CREATED          STATUS
zigbee2mqtt   33 seconds ago   Up 30 seconds
mosquitto     33 seconds ago   Up 31 seconds (healthy)
```

> The above output is filtered down to the relevant columns

You are looking for evidence that the container is restarting (ie the "Status" column only ever shows a low number of seconds when compared with the "Created" column).

### Checking the log { #checkLog }

You can't use `docker logs zigbee2mqtt` to inspect the Zigbee2MQTT container's logs. That's because Zigbee2MQTT writes its logging information to the path:

```
~/IOTstack/volumes/zigbee2mqtt/data/log/yyyy-mm-dd.hh-mm-ss/log.txt
```

where `yyyy-mm-dd.hh-mm-ss` is the date and time the container was last started. This means that you have to identify the folder with the latest timestamp before you can inspect the log contained within it.

Fortunately, Zigbee2MQTT offers a shortcut. If the [`… LOG_SYMLINK_CURRENT`](#logSymlink) environment variable is `true` then the path to the *current* log will be:

```
~/IOTstack/volumes/zigbee2mqtt/data/log/current/log.txt
```

You can use commands like `cat` and `tail` to examine the *current* log. Example:

```console
$ cat ~/IOTstack/volumes/zigbee2mqtt/data/log/current/log.txt
```

### Checking Mosquitto connectivity { #checkMQTT }

To perform this check, you will need to have the Mosquitto clients installed:

```console
$ sudo apt install -y mosquitto-clients
```

The Mosquitto clients package includes two command-line tools:

* `mosquitto_pub` for publishing MQTT messages to the broker; and
* `mosquitto_sub` for subscribing to MQTT messages distributed by the broker.

	> In IOTstack, the "broker" is usually the Mosquitto container.

Assuming the Mosquitto clients are installed, you can run the following command:

```console
$ mosquitto_sub -v -h "localhost" -t "zigbee2mqtt/#" -F "%I %t %p"
```

One of two things will happen:

* *silence,* indicating that the Zigbee2MQTT container is **not** able to communicate with the Mosquitto container. If this happens, you should [check the Zigbee2MQTT log](#checkLog). 
* *chatter,* proving that the Zigbee2MQTT container **can** communicate with the Mosquitto container.

Terminate the `mosquitto_sub` command with a <kbd>Control</kbd><kbd>c</kbd>.

## Connecting to the web GUI { #connectGUI }

Open a browser, and point it to port 8080 on your Raspberry Pi. For example:

```url
http://raspberrypi.local:8080
```

You should see the Zigbee2MQTT interface.

Notes:

1. The availability of the Zigbee2MQTT UI is governed by an environment variable. If you do not see the UI, check that [`… FRONTEND`](#frontEndEnable) is defined.

2. In the URL above, port 8080 is an **external** port which is exposed via the following port mapping in the Zigbee2MQTT service definition:

	```yaml
	ports:
	  - "8080:8080"
	```

	If you want to reach the Zigbee2MQTT UI via a different port, you should edit the left hand side of that mapping. For example, if you wanted to use port 10080 you would write: 

	```yaml
	ports:
	  - "10080:8080"
	```

	Do not change the *internal* port number on the right hand side of the mapping. To apply changes to the port mapping:

	```console
	$ cd ~/IOTstack
	$ docker-compose up -d zigbee2mqtt
	```

## Shell access to the container { #openShell }

To open a shell inside the Zigbee2MQTT container, run:

```console
$ docker exec -it zigbee2mqtt ash
```

> `ash` is **not** a typo!

To close the shell and leave the container, either type "exit" and press <kbd>return</kbd>, or press <kbd>Control</kbd><kbd>d</kbd>.

## Container maintenance { #pullUpgrade }

When you become aware of a new version of Zigbee2MQTT on [DockerHub](https://hub.docker.com/r/koenkk/zigbee2mqtt/tags), do the following:

```console
$ cd ~IOTstack
$ docker-compose pull zigbee2mqtt
$ docker-compose up -d zigbee2mqtt
$ docker system prune
```

In words:

1. Be in the correct directory.
2. The `pull` compares the version on your Raspberry Pi with the latest version on [DockerHub](https://hub.docker.com/r/koenkk/zigbee2mqtt/tags), and downloads any later version.
3. If a newer version is downloaded, the `up` instantiates a new container based on the new image and performs a new-for-old swap. There is barely any downtime.
4. The `prune` cleans up the older image.

You can omit the `zigbee2mqtt` arguments from the `pull` and `up` commands, in which case `docker-compose` makes an attempt to pull any available updates for all non-Dockerfile-based images, and then instantiates any new images it has downloaded.

## Service definition change { #update202204 }

This information is for existing users of the Zigbee2MQTT container.

The default IOTstack service definition for Zigbee2MQTT has changed:

* The container no longer needs to be built using a Dockerfile.
* The Zigbee2MQTT images on [DockerHub](https://hub.docker.com/r/koenkk/zigbee2mqtt/tags) can be used "as is".
* Environment variables supplied with the updated service definition exactly replicate the purpose of the old Dockerfile. 
* The Dockerfile supplied with the IOTstack template is deprecated but continues to be provided to maintain backwards compatibility and to avoid introducing a breaking change.

If you were using the Zigbee2MQTT container in IOTstack before April 2022, you should use your favourite text editor to update your *compose file* to conform with the new service definition.

> You *could* run the menu, then de-select and re-select Zigbee2MQTT. That *will* have the effect of applying the updated service definition but it also risks overwriting any other customisations you may have in place. That is why editing your *compose file* is the recommended approach.

The updated service definition is included here for ease of reference:

``` { .yaml linenums="1" }
zigbee2mqtt:
  container_name: zigbee2mqtt
  image: koenkk/zigbee2mqtt:latest
  environment:
    - TZ=${TZ:-Etc/UTC}
    - ZIGBEE2MQTT_CONFIG_MQTT_SERVER=mqtt://mosquitto:1883
    - ZIGBEE2MQTT_CONFIG_FRONTEND=true
    - ZIGBEE2MQTT_CONFIG_ADVANCED_LOG_SYMLINK_CURRENT=true
    # - DEBUG=zigbee-herdsman*
  ports:
    - "8080:8080"
  volumes:
    - ./volumes/zigbee2mqtt/data:/app/data
  devices:
    - "${ZIGBEE2MQTT_DEVICE_PATH:?eg echo ZIGBEE2MQTT_DEVICE_PATH=/dev/ttyACM0 >>~/IOTstack/.env}:/dev/ttyACM0"
  restart: unless-stopped
  depends_on:
    - mosquitto
```

The changes you should make to your existing Zigbee2MQTT service definition are:

1. Replace the `build` directive:

	```yaml
	build: ./.templates/zigbee2mqtt/.
	```

	with this `image` directive:

	```yaml
	image: koenkk/zigbee2mqtt:latest
	```

	This causes IOTstack to use Zigbee2MQTT images "as is" from [DockerHub](https://hub.docker.com/r/koenkk/zigbee2mqtt/tags).

2. Add these environment variables:

	```yaml
	  - ZIGBEE2MQTT_CONFIG_MQTT_SERVER=mqtt://mosquitto:1883
	  - ZIGBEE2MQTT_CONFIG_FRONTEND=true
	  - ZIGBEE2MQTT_CONFIG_ADVANCED_LOG_SYMLINK_CURRENT=true
	```

	The first two have the **identical** effect to the changes previously made via the Dockerfile. The last variable makes it easier for you to find and [view the current log](#checkLog).
	
	See [environment variables](#envVars) for more detail.

3. Add the dependency clause:

	```yaml
	depends_on:
	  - mosquitto
	```

	This ensures the Mosquitto container is brought up alongside Zigbee2MQTT. The Zigbee2MQTT container goes into a restart loop if Mosquitto is not reachable so this change enforces that business rule. See [`… MQTT_SERVER`](#mqttServer) for the situation where this might not be appropriate.

### pre-existing configuration file { #confExists }

Environment variables in your *compose file* override corresponding values set in the *configuration file* at:

```
~/IOTstack/volumes/zigbee2mqtt/data/configuration.yaml
```

If you have customised your existing Zigbee2MQTT [configuration file](#confFile), you should review your settings for potential conflicts with the environment variables introduced by the changes to the IOTstack service definition. You can resolve any conflicts either by:

* removing or commenting-out conflicting environment variables; or
* altering the environment variable values to match your configuration file.

The second approach is recommended because it minimises the risk that Zigbee2MQTT will go into a restart loop if the configuration file is not present when the container starts.

As the [Zigbee2MQTT documentation](https://www.zigbee2mqtt.io/guide/configuration/#environment-variables) explains, any option that can be set in a configuration file can also be set using an environment variable, so you may want to take the opportunity to implement all your settings as environment variables.
