# Blynk server

This document discusses an IOTstack-specific version of Blynk-Server. It is built on top of an [Ubuntu](https://hub.docker.com/_/ubuntu) base image using a *Dockerfile*.

## References { #references }

- [Ubuntu base image](https://hub.docker.com/_/ubuntu) at DockerHub
- [Peter Knight Blynk-Server fork](https://github.com/Peterkn2001/blynk-server) at GitHub (includes documentation)
- [Peter Knight Blynk-Server releases](https://github.com/Peterkn2001/blynk-server/releases/) at GitHub
- [Blynk home page](https://blynk.io) at blynk.io
- [Blynk documentation](https://docs.blynk.io/en/) at blynk.io
- [Blynk community forum](https://community.blynk.cc/) at community.blynk.cc
- [Interesting post by Peter Knight on MQTT/Node Red flows](
https://community.blynk.cc/t/my-home-automation-projects-built-with-mqtt-and-node-red/29045)  at community.blynk.cc
- [Blynk flow examples](https://github.com/877dev/Node-Red-flow-examples) at GitHub

Acknowledgement:

- Original writeup from @877dev

## Significant directories and files { #significantFiles }

```
~/IOTstack
├── .templates
│   └── blynk_server
│       ├── Dockerfile ❶
│       ├── docker-entrypoint.sh ❷
│       ├── iotstack_defaults ❸
│       │   ├── mail.properties
│       │   └── server.properties
│       └── service.yml ❹
├── services
│   └── blynk_server
│       └── service.yml ❺
├── docker-compose.yml ❻
└── volumes
    └── blynk_server ❼
        ├── config ❽
        │   ├── mail.properties
        │   └── server.properties
        └── data
```

1. The *Dockerfile* used to construct Blynk Server on top of Ubuntu.
2. A start-up script designed to handle container self-repair.
3. A folder holding the default versions of the configuration files.
4. The *template service definition*.
5. The *working service definition* (only relevant to old-menu, copied from ❹).
6. The *Compose* file (includes ❹).
7. The *persistent storage area* for the `blynk_server` container.
8. Working copies of the configuration files (copied from ❸).

Everything in ❽:

* will be replaced if it is not present when the container starts; but
* will never be overwritten if altered by you.

## How Blynk Server gets built for IOTstack { #howBlynkServerIOTstackGetsBuilt }

### GitHub Updates  { #dockerHubImages }

Periodically, the source code is updated and a new version is released. You can check for the latest version at the [releases page](https://github.com/Peterkn2001/blynk-server/releases/).
 
### IOTstack menu { #iotstackMenu }

When you select Blynk Server in the IOTstack menu, the *template service definition* is copied into the *Compose* file.

> Under old menu, it is also copied to the *working service definition* and then not really used.

### IOTstack first run  { #iotstackFirstRun }

On a first install of IOTstack, you run the menu, choose your containers, and are told to do this:

```console
$ cd ~/IOTstack
$ docker-compose up -d
```

`docker-compose` reads the *Compose* file. When it arrives at the `blynk_server` fragment, it finds:

```yaml
  blynk_server:
    build:
      context: ./.templates/blynk_server/.
      args:
        - BLYNK_SERVER_VERSION=0.41.16
```

The `build` statement tells `docker-compose` to look for:

```
~/IOTstack/.templates/blynk_server/Dockerfile
```

The `BLYNK_SERVER_VERSION` argument is passed into the build process. This implicitly pins each build to the version number in the *Compose* file (eg 0.41.16). If you need to update to a  

> The *Dockerfile* is in the `.templates` directory because it is intended to be a common build for **all** IOTstack users. This is different to the arrangement for Node-RED where the *Dockerfile* is in the `services` directory because it is how each individual IOTstack user's version of Node-RED is customised.

The *Dockerfile* begins with:

```Dockerfile
FROM ubuntu
```

The `FROM` statement tells the build process to pull down the ***base image*** from [*DockerHub*](https://hub.docker.com).

> It is a ***base*** image in the sense that it never actually runs as a container on your Raspberry Pi.

The remaining instructions in the *Dockerfile* customise the ***base image*** to produce a ***local image***. The customisations are:

1. Add packages to satisfy dependencies.
2. Add the default versions of the configuration files so that the container can perform self-repair each time it is launched.
3. Download an install the Java package that implements the Blynk Server. 

The ***local image*** is instantiated to become your running container.

When you run the `docker images` command after Blynk Server has been built, you *may* see two rows that are relevant:

```console
$ docker images
REPOSITORY              TAG      IMAGE ID       CREATED         SIZE
iotstack_blynk_server   latest   3cd6445f8a7e   3 hours ago     652MB
ubuntu                  latest   897590a6c564   7 days ago      49.8MB
```

* `ubuntu ` is the ***base image***; and
* `iotstack_blynk_server ` is the ***local image***.

You *may* see the same pattern in *Portainer*, which reports the ***base image*** as "unused". You should not remove the ***base*** image, even though it appears to be unused.

> Whether you see one or two rows depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

## Logging { #logging }

You can inspect Blynk Server's log by:

```console
$ docker logs blynk_server
```

## Changing Blynk Server's configuration { #editConfiguration }

The first time you launch the `blynk_server` container, the following structure will be created in the persistent storage area:

```
~/IOTstack/volumes/blynk_server
├── [drwxr-xr-x pi      ]  config
│   ├── [-rw-r--r-- pi      ]  mail.properties
│   └── [-rw-r--r-- pi      ]  server.properties
└── [drwxr-xr-x root    ]  data
```

The two `.properties` files can be used to alter Blynk Server's configuration. When you make change to these files, you activate then by restarting the container:

```console
$ cd ~/IOTstack
$ docker-compose restart blynk_server
```

## Getting a clean slate { #cleanSlate }

Erasing Blynk Server's persistent storage area triggers self-healing and restores known defaults:

```console
$ cd ~/IOTstack
$ docker-compose down blynk_server
$ sudo rm -rf ./volumes/blynk_server
$ docker-compose up -d blynk_server
```
Notes:

* You can also remove individual configuration files and then trigger self-healing. For example, if you decide to edit `server.properties` and make a mess, you can restore the original default version like this:

	```console
	$ cd ~/IOTstack
	$ rm volumes/blynk_server/config/server.properties
	$ docker-compose restart blynk_server
	```
	
* See also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)

## Upgrading Blynk Server { #upgradingBlynkServer }

To find out when a new version has been released, you need to visit the [Blynk-Server releases](https://github.com/Peterkn2001/blynk-server/releases/) page at GitHub.

At the time of writing, version 0.41.16 was the most up-to-date. Suppose that version 0.41.17 has been released and that you decide to upgrade:

1. Edit your *Compose* file to change the version nuumber:

	```yaml
	  blynk_server:
	    build:
	      context: ./.templates/blynk_server/.
	      args:
	        - BLYNK_SERVER_VERSION=0.41.17
	```

	Note:

	- You can use this method to pin Blynk Server to any available version.

2. You then have two options:

	- If you only want to reconstruct the **local** image:

		```console
		$ cd ~/IOTstack
		$ docker-compose up --build -d blynk_server
		$ docker system prune -f
		```

	- If you want to update the Ubuntu **base** image at the same time:

		```console
		$ cd ~/IOTstack
		$ docker-compose build --no-cache --pull blynk_server
		$ docker-compose up -d blynk_server
		$ docker system prune -f
		$ docker system prune -f
		```

		The second `prune` will only be needed if there is an old *base image* and that, in turn, depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

## Using Blynk Server { #usingBlynkServer }

See the [References](#references) for documentation links.

### Connecting to the administrative UI { #blynkAdmin }

To connect to the administrative interface, navigate to:

```
https://<your pis IP>:9444/admin
```

You may encounter browser security warnings which you will have to acknowledge in order to be able to connect to the page. The default credentials are:

- username = `admin@blynk.cc`
- password = `admin`

### Change username and password { #changePassword }

1. Click on Users > "email address" and edit email, name and password. 
2. Save changes.
3. Restart the container using either Portainer or the command line:

	```console
	$ cd ~/IOTstack
	$ docker-compose restart blynk_server
	```

### Setup gmail { #gmailSetup }

Optional step, useful for getting the auth token emailed to you.
(To be added once confirmed working....)

### iOS/Android app setup { #mobileSetup }

1. When setting up the application on your mobile be sure to select "custom" setup [see](https://github.com/Peterkn2001/blynk-server#app-and-sketch-changes).
2. Press "New Project"
3. Give it a name, choose device "Raspberry Pi 3 B" so you have plenty of [virtual pins](http://help.blynk.cc/en/articles/512061-what-is-virtual-pins) available, and lastly select WiFi.
4. Create project and the [auth token](https://docs.blynk.cc/#getting-started-getting-started-with-the-blynk-app-4-auth-token) will be emailed to you (if emails configured). You can also find the token in app under the phone app settings, or in the admin web interface by clicking Users>"email address" and scroll down to token.

### Quick usage guide for app { #quickAppGuide }

1. Press on the empty page, the widgets will appear from the right.
2. Select your widget, let's say a button.
3. It appears on the page, press on it to configure.
4. Give it a name and colour if you want. 
5. Press on PIN, and select virtual. Choose any pin i.e. V0
6. Press ok.
7. To start the project running, press top right Play button.
8. You will get an offline message, because no devices are connected to your project via the token.

Enter Node-Red.....

### Node-RED { #enterNodeRed }

1. Install `node-red-contrib-blynk-ws` from Manage Palette.
2. Drag a "write event" node into your flow, and connect to a debug node
3. Configure the Blynk node for the first time:

	```
	URL: wss://youripaddress:9444/websockets
	```

	There is more information [here](https://github.com/gablau/node-red-contrib-blynk-ws/blob/master/README.md#how-to-use).
4. Enter your [auth token](https://docs.blynk.cc/#getting-started-getting-started-with-the-blynk-app-4-auth-token) from before and save/exit.
5. When you deploy the flow, notice the app shows connected message, as does the Blynk node.
6. Press the button on the app, you will notice the payload is sent to the debug node.
