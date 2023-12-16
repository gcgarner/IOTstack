# Telegraf

This document discusses an IOTstack-specific version of Telegraf built on top of [influxdata/influxdata-docker/telegraf](https://github.com/influxdata/influxdata-docker/tree/master/telegraf) using a *Dockerfile*.

The purpose of the Dockerfile is to:

* tailor the default configuration to be IOTstack-ready; and
* enable the container to perform self-repair if essential elements of the persistent storage area disappear.
 
## References { #references }

- [*influxdata Telegraf* home](https://www.influxdata.com/time-series-platform/telegraf/)
- [*GitHub*: influxdata/influxdata-docker/telegraf](https://github.com/influxdata/influxdata-docker/tree/master/telegraf)
- [*DockerHub*: influxdata Telegraf](https://hub.docker.com/_/telegraf)

## Significant directories and files { #significantFiles }

```
~/IOTstack
├── .templates
│   └── telegraf
│       ├── Dockerfile ❶
│       ├── entrypoint.sh ❷
│       ├── iotstack_defaults
│       │   ├── additions ❸
│       │   └── auto_include ❹
│       └── service.yml ❺
├── services
│   └── telegraf
│       └── service.yml ❻
├── docker-compose.yml
└── volumes
    └── telegraf ❼
        ├── additions ❽
        ├── telegraf-reference.conf ➒
        └── telegraf.conf ➓
```

1. The *Dockerfile* used to customise Telegraf for IOTstack.
2. A replacement for the `telegraf` container script of the same name, extended to handle container self-repair.
3. The *additions folder*. See [Applying optional additions](#optionalAdditions).
4. The *auto_include folder*. Additions automatically applied to
   `telegraf.conf`. See [Automatic includes to telegraf.conf](#autoInclude).
5. The *template service definition*.
6. The *working service definition* (only relevant to old-menu, copied from ❹).
7. The *persistent storage area* for the `telegraf` container.
8. A working copy of the *additions folder* (copied from ❸). See [Applying optional additions](#optionalAdditions).
9. The *reference configuration file*. See [Changing Telegraf's configuration](#editConfiguration).
10. The *active configuration file*. A subset of ➒ altered to support communication with InfluxDB running in a container in the same IOTstack instance.

Everything in the persistent storage area ❼:

* will be replaced if it is not present when the container starts; but
* will never be overwritten if altered by you.

## How Telegraf gets built for IOTstack { #howTelegrafIOTstackGetsBuilt }

### IOTstack menu { #iotstackMenu }

When you select Telegraf in the IOTstack menu, the *template service definition* is copied into the *Compose* file.

> Under old menu, it is also copied to the *working service definition* and then not really used.

### IOTstack first run { #iotstackFirstRun }

On a first install of IOTstack, you run the menu, choose your containers, and are told to do this:

``` console
$ cd ~/IOTstack
$ docker-compose up -d
```

> See also the [Migration considerations](#migration) (below).

`docker-compose` reads the *Compose* file. When it arrives at the `telegraf` fragment, it finds:

``` yaml
  telegraf:
    container_name: telegraf
    build: ./.templates/telegraf/.
    …
```

The `build` statement tells `docker-compose` to look for:

```
~/IOTstack/.templates/telegraf/Dockerfile
```

> The *Dockerfile* is in the `.templates` directory because it is intended to be a common build for **all** IOTstack users. This is different to the arrangement for Node-RED where the *Dockerfile* is in the `services` directory because it is how each individual IOTstack user's version of Node-RED is customised.

The *Dockerfile* begins with:

```
FROM telegraf:latest
```

> If you need to pin to a particular version of Telegraf, the *Dockerfile* is the place to do it. See [Telegraf version pinning](#versionPinning).

The `FROM` statement tells the build process to pull down the ***base image*** from [*DockerHub*](https://hub.docker.com/_/telegraf?tab=tags&page=1&ordering=last_updated&name=latest).

> It is a ***base*** image in the sense that it never actually runs as a container on your Raspberry Pi.

The remaining instructions in the *Dockerfile* customise the ***base image*** to produce a ***local image***. The customisations are:

1. Add the `rsync` package. This helps the container perform self-repair.
2. Copy the *default configuration file* that comes with the DockerHub image (so it will be available as a fully-commented reference for the user) and make it read-only.
3. Make a *working version* of the *default configuration file* from which comment lines and blank lines have been removed.
4. Patch the *working version* to support communications with InfluxDB running in another container in the same IOTstack instance.
5. Replace `entrypoint.sh` with a version which:

	* calls `rsync` to perform self-repair if `telegraf.conf` goes missing; and
	* enforces root:root ownership in `~/IOTstack/volumes/telegraf`.

The ***local image*** is instantiated to become your running container.

When you run the `docker images` command after Telegraf has been built, you *may* see two rows for Telegraf:

``` console
$ docker images
REPOSITORY          TAG      IMAGE ID       CREATED       SIZE
iotstack_telegraf   latest   59861b7fe9ed   2 hours ago   292MB
telegraf            latest   a721ac170fad   3 days ago    273MB
```

* `telegraf ` is the ***base image***; and
* `iotstack_telegraf ` is the ***local image***.

You *may* see the same pattern in *Portainer*, which reports the ***base image*** as "unused". You should not remove the ***base*** image, even though it appears to be unused.

> Whether you see one or two rows depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

### Migration considerations { #migration }

Under the original IOTstack implementation of Telegraf (just "as it comes" from *DockerHub*), the service definition expected `telegraf.conf` to be at:

```
~/IOTstack/services/telegraf/telegraf.conf
```

Under this implementation of Telegraf, the configuration file has moved to:

```
~/IOTstack/volumes/telegraf/telegraf.conf
```

> The change of location is one of the things that allows self-repair to work properly. 

With one exception, all prior and current versions of the default configuration file are identical in terms of their semantics.

> In other words, once you strip away comments and blank lines, and remove any "active" configuration options that simply repeat their default setting, you get the same subset of "active" configuration options. The default configuration file supplied with gcgarner/IOTstack is available [here](https://github.com/gcgarner/IOTstack/blob/master/.templates/telegraf/telegraf.conf) if you wish to refer to it.

The exception is `[[inputs.mqtt_consumer]]` which is now provided as an optional addition. If your existing Telegraf configuration depends on that input, you will need to apply it. See [applying optional additions](#optionalAdditions).

## Logging { #logging }

You can inspect Telegraf's log by:

``` console
$ docker logs telegraf
```

These logs are ephemeral and will disappear when your Telegraf container is rebuilt.

### log message: *database "telegraf" creation failed* { #logTelegrafDB }

The following log message can be misleading:

```
W! [outputs.influxdb] When writing to [http://influxdb:8086]: database "telegraf" creation failed: Post "http://influxdb:8086/query": dial tcp 172.30.0.9:8086: connect: connection refused
```

If InfluxDB is not running when Telegraf starts, the `depends_on:` clause in Telegraf's service definition tells Docker to start InfluxDB (and Mosquitto) before starting Telegraf. Although it can launch the InfluxDB *container* first, Docker has no way of knowing when the `influxd` *process* running inside the InfluxDB container will start listening to port 8086.

What this error message *usually* means is that Telegraf has tried to communicate with InfluxDB before the latter is ready to accept connections. Telegraf typically retries after a short delay and is then able to communicate with InfluxDB.

## Changing Telegraf's configuration { #editConfiguration }

The first time you launch the Telegraf container, the following structure will be created in the persistent storage area:

```
~/IOTstack/volumes/telegraf
├── [drwxr-xr-x root    ]  additions
│   └── [-rw-r--r-- root    ]  inputs.mqtt_consumer.conf
├── [-rw-r--r-- root    ]  telegraf.conf
└── [-r--r--r-- root    ]  telegraf-reference.conf
```

The file:

* `telegraf-reference.conf`:

	- is a *reference* copy of the default configuration file that ships with the ***base image*** for Telegraf when it is downloaded from DockerHub. It is nearly 9000 lines long and is mostly comments.
	- is **not** used by Telegraf but will be replaced if you delete it.
	- is marked "read-only" (even for root) as a reminder that it is only for your reference. Any changes you make will be ignored.

* `telegraf.conf`:

	- is created by removing all comment lines and blank lines from `telegraf-reference.conf`, leaving only the "active" configuration options, and then adding options necessary for IOTstack.
	- is less than 30 lines and is significantly easier to understand than `telegraf-reference.conf`.

* `inputs.mqtt_consumer.conf` – see [Applying optional additions](#optionalAdditions) below.

The intention of this structure is that you:

1. search `telegraf-reference.conf` to find the configuration option you need;
2. read the comments to understand what the option does and how to use it; and then
3. import the option into the correct section of `telegraf.conf`.

When you make a change to `telegraf.conf`, you activate it by restarting the container:

``` console
$ cd ~/IOTstack
$ docker-compose restart telegraf
```

### Automatic includes to telegraf.conf { #autoInclude }

* `inputs.docker.conf` instructs Telegraf to collect metrics from Docker. Requires kernel control
  groups to be enabled to collect memory usage data. If not done during initial installation,
  enable by running (reboot required):
  ``` console
  $ echo $(cat /boot/cmdline.txt) cgroup_memory=1 cgroup_enable=memory | sudo tee /boot/cmdline.txt
  ```
* `inputs.cpu_temp.conf` collects cpu temperature.
 
### Applying optional additions { #optionalAdditions }

The *additions folder* (see [Significant directories and files](#significantFiles)) is a mechanism for additional *IOTstack-ready* configuration options to be provided for Telegraf.

Currently there is one addition:

1. `inputs.mqtt_consumer.conf` which formed part of the [gcgarner/IOTstack telegraf configuration](https://github.com/gcgarner/IOTstack/blob/master/.templates/telegraf/telegraf.conf) and instructs Telegraf to subscribe to a metric feed from the Mosquitto broker. This assumes, of course, that something is publishing those metrics.

Using `inputs.mqtt_consumer.conf` as the example, applying that addition to
your Telegraf configuration file involves:

``` console
$ cd ~/IOTstack/volumes/telegraf
$ grep -v "^#" additions/inputs.mqtt_consumer.conf | sudo tee -a telegraf.conf >/dev/null
$ cd ~/IOTstack
$ docker-compose restart telegraf
```

The `grep` strips comment lines and the `sudo tee` is a safe way of appending the result to `telegraf.conf`. The `restart` causes Telegraf to notice the change.

## Getting a clean slate { #cleanSlate }

### Erasing the persistent storage area { #zapStore }

Erasing Telegraf's persistent storage area triggers self-healing and restores known defaults:

``` console
$ cd ~/IOTstack
$ docker-compose down telegraf
$ sudo rm -rf ./volumes/telegraf
$ docker-compose up -d telegraf
```

Notes:

* You can also remove individual files within the persistent storage area and then trigger self-healing. For example, if you decide to edit `telegraf-reference.conf` and make a mess, you can restore the original version like this:

	``` console
	$ cd ~/IOTstack
	$ sudo rm ./volumes/telegraf/telegraf-reference.conf
	$ docker-compose restart telegraf
	```

* See also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)

### Resetting the InfluxDB database { #resetDB }

To reset the InfluxDB database that Telegraf writes into, proceed like this:

``` console
$ cd ~/IOTstack
$ docker-compose down telegraf
$ docker exec -it influxdb influx -precision=rfc3339
> drop database telegraf
> exit
$ docker-compose up -d telegraf
```

In words:

* Be in the right directory.
* Stop the Telegraf container (while leaving the InfluxDB container running). See also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer).
* Launch the Influx CLI inside the InfluxDB container.
* Delete the `telegraf` database, and then exit the CLI.
* Start the Telegraf container. This re-creates the database automatically. 

## Upgrading Telegraf { #upgradingTelegraf }

You can update most containers like this:

``` console
$ cd ~/IOTstack
$ docker-compose pull
$ docker-compose up -d
$ docker system prune
```

In words:

* `docker-compose pull` downloads any newer images;
* `docker-compose up -d` causes any newly-downloaded images to be instantiated as containers (replacing the old containers); and
* the `prune` gets rid of the outdated images.

This strategy doesn't work when a *Dockerfile* is used to build a ***local image*** on top of a ***base image*** downloaded from [*DockerHub*](https://hub.docker.com). The ***local image*** is what is running so there is no way for the `pull` to sense when a newer version becomes available.

The only way to know when an update to Telegraf is available is to check the [Telegraf tags page](https://hub.docker.com/_/telegraf?tab=tags&page=1&ordering=last_updated) on *DockerHub*.

Once a new version appears on *DockerHub*, you can upgrade Telegraf like this:

``` console
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull telegraf
$ docker-compose up -d telegraf
$ docker system prune
$ docker system prune
```

Breaking it down into parts:

* `build` causes the named container to be rebuilt;
* `--no-cache` tells the *Dockerfile* process that it must not take any shortcuts. It really **must** rebuild the ***local image***;
* `--pull` tells the *Dockerfile* process to actually check with [*DockerHub*](https://hub.docker.com) to see if there is a later version of the ***base image*** and, if so, to download it before starting the build;
* `telegraf` is the named container argument required by the `build` command.

Your existing Telegraf container continues to run while the rebuild proceeds. Once the freshly-built ***local image*** is ready, the `up` tells `docker-compose` to do a new-for-old swap. There is barely any downtime for your service.

The `prune` is the simplest way of cleaning up. The first call removes the old ***local image***. The second call cleans up the old ***base image***. Whether an old ***base image*** exists depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

### Telegraf version pinning { #versionPinning }

If you need to pin Telegraf to a particular version:

1. Use your favourite text editor to open the following file:

	```
	~/IOTstack/.templates/telegraf/Dockerfile
	```

2. Find the line:

	```
	FROM telegraf:latest
	```

3. Replace `latest` with the version you wish to pin to. For example, to pin to version 1.19.3:

	```
	FROM telegraf:1.19.3
	```

4. Save the file and tell `docker-compose` to rebuild the ***local image***:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d --build telegraf
	$ docker system prune
	``` 

	The new ***local image*** is built, then the new container is instantiated based on that image. The `prune` deletes the old ***local image***.
	
Note:

* As well as preventing Docker from updating the ***base image***, pinning will also block incoming updates to the *Dockerfile* from a `git pull`. Nothing will change until you decide to remove the pin.
