# Motion JPEG Streamer

The `mjpg-streamer` container lets you pass a video stream from a local camera to a `motioneye` container. The `mjpg-streamer` and `motioneye` containers can be running on the *same* or *different* hosts.

Each `mjpg-streamer` container can process a stream from an official Raspberry Pi "ribbon cable" camera, or from a third-party USB-connected camera, such as those from [Logitech](https://www.logitech.com/en-au/products/webcams.html).

Using `mjpg-streamer` to handle your video streams gives you a consistent approach to supporting multiple cameras and camera types. You do not need to care about distinctions between "ribbon" or USB cameras, nor which hosts are involved.

## Raspberry Pi Ribbon Camera

> This section is only relevant if you are trying to use a camera that connects to your Raspberry Pi via a ribbon cable.

Beginning with Raspberry Pi OS Bullseye, the Raspberry Pi Foundation introduced the [LibCamera](https://www.raspberrypi.com/documentation/computers/camera_software.html) subsystem and withdrew support for the earlier `raspistill` and `raspivid` mechanisms which then became known as the *legacy* camera system.

The introduction of the *LibCamera* subsystem triggered quite a few articles (and videos) on the topic, of which this is one example:

* [How to use Raspberry Pi Cameras with Bullseye OS Update](https://core-electronics.com.au/guides/raspberry-pi-bullseye-camera-commands/)

Although the *LibCamera* subsystem works quite well with "native" applications, it has never been clear whether it supports passing camera streams to Docker containers. At the time of writing (2023-10-23), this author has never been able to find any examples which demonstrate that such support exists.
 
It is important to understand that:

1. This **only** applies to the Raspberry Pi Ribbon Camera;
2. In order to access a Raspberry Pi Ribbon Camera, the `mjpg-streamer` container depends on the *legacy* camera system; and
3. The *LibCamera* subsystem and the *legacy* camera system are mutually exclusive.

In other words, if you want to use the `mjpg-streamer` container to process a stream from a Raspberry Pi Ribbon Camera, you have to forgo using the *LibCamera* subsystem.

### preparing your Raspberry Pi

If you have a Raspberry Pi Ribbon Camera, prepare your system like this:

1. Check the version of your system by running:

	``` console
	$ grep "VERSION_CODENAME" /etc/os-release
	```

	The answer should be one of "buster", "bullseye" or "bookworm".

2. Configure camera support:

	* if your system is running Buster, run this command:

		``` console
		$ sudo raspi-config nonint do_camera 0
		```

		Buster pre-dates *LibCamera* so this is the same as enabling the *legacy* camera system. In this context, `0` means "enable" and `1` means "disable".

	* if your system is running Bullseye or Bookworm, run these commands:

		``` console
		$ sudo raspi-config nonint do_camera 1
		$ sudo raspi-config nonint do_legacy 0
		```

		The first command is protective and turns off the *LibCamera* subsystem, while the second command enables the *legacy* camera system.

		> When executed from the command line, both the `do_camera` and `do_legacy` commands are supported in the Bookworm version of `raspi-config`. However, neither command is available when `raspi-config` is invoked as a GUI in a Bookworm system. This likely implies that the commands have been deprecated and will be removed, in which case this documentation will break.

3. Reboot your system:

	``` console
	$ sudo reboot
	```

4. Make a note that your ribbon camera will be accessible on `/dev/video0`.

## Third-party cameras

The simplest approach is:

1. Connect your camera to a USB port.
2. Run: 

	``` console
	$ ls -l /dev/v4l/by-id
	```

	This is an example of the response with a LogiTech "C920 PRO FHD Webcam 1080P" camera connected:

	```
	lrwxrwxrwx 1 root root 12 Oct 23 15:42 usb-046d_HD_Pro_Webcam_C920-video-index0 -> ../../video1
	lrwxrwxrwx 1 root root 12 Oct 23 15:42 usb-046d_HD_Pro_Webcam_C920-video-index1 -> ../../video2
	```

	In general, the device at `index0` is where your camera will be accessible, as in:

	```
	/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920-video-index0
	```

If you don't get a sensible response to the `ls` command then try disconnecting and reconnecting your camera, and rebooting your system.

## Container variables

### environment variables

variable                         | default       | remark
---------------------------------|:-------------:|------------------------------    
`MJPG_STREAMER_USERNAME`         | container ID  | *changes each time the container is recreated*
`MJPG_STREAMER_PASSWORD`         | random UUID   | *changes each time the container restarts*
`MJPG_STREAMER_SIZE`             | `640x480`     | should be one of your camera's natural resolutions
`MJPG_STREAMER_FPS`              | `5`           | frames per second

### device variable

variable                         | default       | remark
---------------------------------|:-------------:|------------------------------    
`MJPG_STREAMER_EXTERNAL_DEVICE`  | `/dev/video0` | must be set to your video device

## Setting your variables

To initialise your environment, begin by using a text editor (eg `vim`, `nano`) to edit `~/IOTstack/.env` (which may or may not already exist):

1. If your `.env` file does not already define your time-zone, take the opportunity to set it. For example:

	```
	TZ=Australia/Sydney
	```

2. The access credentials default to random values which change each time the container starts. This is reasonably secure but is unlikely to be useful in practice, so you need to invent some credentials of your own. Example:

	```
	MJPG_STREAMER_USERNAME=streamer
	MJPG_STREAMER_PASSWORD=oNfDG-d1kgzC
	```

3. Define the **external** device path to your camera. Two examples have been given above:

	* a ribbon camera:

		```
		MJPG_STREAMER_EXTERNAL_DEVICE=/dev/video0
		```

	* a Logitech C920 USB camera:

		```
		MJPG_STREAMER_EXTERNAL_DEVICE=/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920-video-index
		```

4. If you know your camera supports higher resolutions, you can also set the size. Examples:

	* the ribbon camera can support:

		```
		MJPG_STREAMER_SIZE=1152x648
		```

	* the Logitech C920 can support:

		```
		MJPG_STREAMER_SIZE=1920x1080
		```

5. If the `mjpg-streamer` and `motioneye` containers are going to be running on:

	* the **same** host, you can consider increasing the frame rate:

		```
		MJPG_STREAMER_FPS=30
		```

		Even though we are setting up a *web* camera, the traffic will never leave the host and will not traverse your Ethernet or WiFi networks.

	* **different** hosts, you should probably leave the rate at 5 frames per second until you understand the impact on network traffic.

6. Save your work.

Tip:

* Do **not** use quote marks (either single or double quotes) to surround the values of your environment variables. This is because docker-compose treats the quotes as part of the string. If you used quotes, please go back and remove them.

### alternative approach

It is still a good idea to define `TZ` in your `.env` file. Most IOTstack containers now use the `TZ=${TZ:-Etc/UTC}` syntax so a single entry in your `.env` sets the timezone for all of your containers.

However, if you prefer to keep most of your environment variables inline in your `docker-compose.yml` rather than in `.env`, you can do that. Example:

``` yaml
environment:
  - TZ=${TZ:-Etc/UTC}
  - MJPG_STREAMER_USERNAME=streamer
  - MJPG_STREAMER_PASSWORD=oNfDG-d1kgzC
  - MJPG_STREAMER_SIZE=1152x648
  - MJPG_STREAMER_FPS=5
```

Similarly for the camera device mapping:

``` yaml
devices:
  - "/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920-video-index:/dev/video0"
```

### about variable substitution syntax

If you're wondering about the syntax used for environment variables:

``` yaml
  - MJPG_STREAMER_USERNAME=${MJPG_STREAMER_USERNAME:-}
```

it means that `.env` will be checked for the presence of `MJPG_STREAMER_USERNAME=value`. If the key is found, its value will be used. If the key is not found, the value will be set to a null string. Then, inside the container, a null string is used as the trigger to apply the defaults listed in the table above.

In the case of the camera device mapping, this syntax:

``` yaml
  - "${MJPG_STREAMER_EXTERNAL_DEVICE:-/dev/video0}:/dev/video0"
```

means that `.env` will be checked for the presence of `MJPG_STREAMER_EXTERNAL_DEVICE=path`. If the key is found, the path will be used. If the key is not found, the path will be set to `/dev/video0` on the assumption that a camera is present and the device exists.

Regardless of whether a device path comes from `.env`, or is defined inline, or defaults to `/dev/video0`, if the device does not actually exist then `docker-compose` will refuse to start the container with the following error:

```
Error response from daemon: error gathering device information while adding custom device "«path»": no such file or directory
```

## Starting the container

1. Start the container like this:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d mjpg-streamer
	```

	The first time you do this triggers a fairly long process. First, a basic operating system image is downloaded from DockerHub, then a Dockerfile is run to add the streamer software and construct a local image, after which the local image is instantiated as your running container. Subsequent launches use the local image so the container starts immediately. See also [container maintenance](#maintenance).

2. Once the container is running, make sure it is behaving normally and has not gone into a restart loop:

	``` console
	$ docker ps -a --format "table {{.Names}}\t{{.RunningFor}}\t{{.Status}}"
	```

	> The `docker ps` command produces a lot of output which generally results in line-wrapping and can be hard to read. The `--format` argument reduces this clutter by focusing on the interesting columns. If you have [IOTstackAliases](https://github.com/Paraphraser/IOTstackAliases) installed, you can use `DPS` instead of copy/pasting the above command.

	If the container is restarting, you will see evidence of that in the STATUS column. If that happens, re-check the values set in the `.env` file and "up" the container again. The container's log (see below) may also be helpful.

3. Check the container's log:

	``` console
	$ docker logs mjpg-streamer
	 i: Using V4L2 device.: /dev/video0
	 i: Desired Resolution: 1152 x 648
	 i: Frames Per Second.: 5
	 i: Format............: JPEG
	 i: TV-Norm...........: DEFAULT
	 o: www-folder-path......: /usr/local/share/mjpg-streamer/www/
	 o: HTTP TCP port........: 80
	 o: HTTP Listen Address..: (null)
	 o: username:password....: streamer:oNfDG-d1kgzC
	 o: commands.............: enabled
	```

	Many of the values you set earlier using environment variables show up here so viewing the log is a good way of making sure everything is being passed to the container.

	Note:

	* The `/dev/video0` in the first line of output is the **internal** device path (inside the container). This is **not** the same as the **external** device path associated with `MJPG_STREAMER_EXTERNAL_DEVICE`. The container doesn't know about the **external** device path so it has no way to display it.

## Connecting the camera to MotionEye

1. Use a browser to connect with MotionEye on port 8765.
2. Authenticate as an administrator (the default is "admin" with no password).
3. Click the &#x2630; icon at the top, left of the screen so that it rotates 90° and exposes the "Camera" popup menu.
3. In the "Camera" popup menu field, click the &#x25BE; and choose "Add&nbsp;Camera…".
4. Change the "Camera Type" field to "Network Camera".
5. If the `motioneye` and `mjpg-streamer` containers are running on:

	* the **same** host, the URL should be:

		```
		http://mjpg-streamer:80/?action=stream
		```

		Here:

		- `mjpg-streamer` is the name of the **container**. Technically, it is a **host** name (rather than a domain name); and
		- port 80 is the **internal** port that the streamer process running inside the container is listening to. It comes from the *right* hand side of the port mapping in the service definition:

			``` yaml
			ports:
			- "8980:80"
			```

	* **different** hosts, the URL should be in this form:

		```
		http://«name-or-ip»:8980/?action=stream
		```

		Here:

		- `«name-or-ip»` is the domain name or IP address of the host on which the `mjpg-streamer` container is running. Examples:

			```
			http://raspberrypi.local:8980/?action=stream
			http://my-spy.domain.com:8980/?action=stream
			http://192.168.200.200:8980/?action=stream
			```

		- port 8980 is the **external** port that the host where the `mjpg-streamer` container is running is listening on behalf of the container. It comes from the *left* hand side of the port mapping in the service definition:

			``` yaml
			ports:
			- "8980:80"
			```

6. Enter the Username ("streamer" in this example).
7. Enter the Password ("oNfDG-d1kgzC" in this example).
8. Click in the Username field again. This causes MotionEye to retry the connection, after which the camera should appear in the Camera field.
9. Click OK. The camera feed should start working.

## Container maintenance { #maintenance }

Because it is built from a local Dockerfile, the `mjpg-streamer` does not get updated in response to a normal "pull". If you want to rebuild the container, proceed like this:

``` console
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull mjpg-streamer
$ docker-compose up -d mjpg-streamer
$ docker system prune -f
```

If you have [IOTstackAliases](https://github.com/Paraphraser/IOTstackAliases) installed, the above is:

``` console
$ REBUILD mjpg-streamer
$ UP mjpg-streamer
$ PRUNE
```
