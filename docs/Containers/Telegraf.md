# Telegraf

This document discusses an IOTstack-specific version of Telegraf built on top of [influxdata/influxdata-docker/telegraf](https://github.com/influxdata/influxdata-docker/tree/master/telegraf) using a *Dockerfile*.

The purpose of the Dockerfile is to enable the container to perform self-repair if the `telegraf.conf	` configuration file disappears.
 
## <a name="references"> References </a>

- [*influxdata Telegraf* home](https://www.influxdata.com/time-series-platform/telegraf/)
- [*GitHub*: influxdata/influxdata-docker/telegraf](https://github.com/influxdata/influxdata-docker/tree/master/telegraf)
- [*DockerHub*: influxdata Telegraf](https://hub.docker.com/_/telegraf)

## <a name="significantFiles"> Significant directories and files </a>

```
~/IOTstack
├── .templates
│   └── telegraf
│       ├── Dockerfile ❶
│       ├── entrypoint.sh ❷
│       └── service.yml ❸
├── services
│   └── telegraf
│       └── service.yml ❹
├── docker-compose.yml ❺
└── volumes
    └── telegraf ❻
        └── telegraf.conf ❼
```

1. The *Dockerfile* used to customise Telegraf for IOTstack.
2. A replacement for the `telegraf` container script of the same name, extended to handle container self-repair.
3. The *template service definition*.
4. The *working service definition* (only relevant to old-menu, copied from ❸).
5. The *Compose* file (includes ❸).
6. The *persistent storage area* for the `telegraf` container.
7. The configuration file. Will be created by default if not present in ❻ when the container starts but will not be overwritten if customised by you.

## <a name="howTelegrafIOTstackGetsBuilt"> How Telegraf gets built for IOTstack </a>

### <a name="dockerHubImages"> Telegraf images ([*DockerHub*](https://hub.docker.com)) </a>

Periodically, the source code is recompiled and the resulting image is pushed to [influxdata Telegraf](https://hub.docker.com/_/telegraf?tab=tags&page=1&ordering=last_updated) on *DockerHub*.
 
### <a name="iotstackMenu"> IOTstack menu </a>

When you select Telegraf in the IOTstack menu, the *template service definition* is copied into the *Compose* file.

> Under old menu, it is also copied to the *working service definition* and then not really used.

### <a name="iotstackFirstRun"> IOTstack first run </a>

On a first install of IOTstack, you run the menu, choose your containers, and are told to do this:

```bash
$ cd ~/IOTstack
$ docker-compose up -d
```

> See also the [Migration considerations](#migration) (below).

`docker-compose` reads the *Compose* file. When it arrives at the `telegraf` fragment, it finds:

```
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

The `FROM` statement tells the build process to pull down the ***base image*** from [*DockerHub*](https://hub.docker.com).

> It is a ***base*** image in the sense that it never actually runs as a container on your Raspberry Pi.

The remaining instructions in the *Dockerfile* customise the *base image* to produce a ***local image***. The customisations are:

1. Add the `rsync` package. This helps the container perform self-repair.
2. Make a backup copy of the default `telegraf.conf`. The backup is used to re-create the working copy if that ever gets removed from the persistent storage area.
3. Replace `entrypoint.sh` with a version which:

	* calls `rsync` to perform self-repair if `telegraf.conf` goes missing; and
	* enforces root:root ownership in `~/IOTstack/volumes/telegraf`.

The *local image* is instantiated to become your running container.

When you run the `docker images` command after Telegraf has been built, you will see two rows for Telegraf:

```bash
$ docker images
REPOSITORY          TAG      IMAGE ID       CREATED       SIZE
iotstack_telegraf   latest   59861b7fe9ed   2 hours ago   292MB
telegraf            latest   a721ac170fad   3 days ago    273MB
```

* `telegraf ` is the *base image*; and
* `iotstack_telegraf ` is the *local image*.

You will see the same pattern in *Portainer*, which reports the *base image* as "unused". You should not remove the *base* image, even though it appears to be unused.

### <a name="migration"> Migration considerations </a>

Under the original IOTstack implementation of Telegraf (just "as it comes" from *DockerHub*), the service definition expected `telegraf.conf` to be at:

```
~/IOTstack/services/telegraf/telegraf.conf
```

Under this implementation of Telegraf, the configuration file has moved to:

```
~/IOTstack/volumes/telegraf/telegraf.conf
```

> The change of location is one of the things that allows self-repair to work properly. 

The default version the configuration file supplied with earlier versions of IOTstack only contained 237 lines. At the time of writing (August 2021), the default version supplied with the Telegraf image downloaded from *DockerHub* contains 8641 lines.

> That is a **significant** difference. It is not clear why the version supplied with the original [gcgarner/IOTstack](https://github.com/gcgarner/IOTstack/blob/master/.templates/telegraf/telegraf.conf) was so short. Nevertheless, that file was inherited by [SensorsIot/IOTstack](https://github.com/SensorsIot/IOTstack/blob/master/.templates/telegraf/telegraf.conf) and has never been changed.

If you did not need to alter the 237-line file when you were running the original IOTstack implementation of Telegraf, it is *readonably* likely that the 8641-line default will also work, and that there will be no change in Telegraf's behaviour when it is built from a *Dockerfile*.

However, if you experience problems then you have two choices:

1. Use your old `telegraf.conf`:

	```bash
	$ cd ~/IOTstack
	$ docker-compose rm --force --stop -v telegraf
	$ sudo cp ./services/telegraf/telegraf.conf ./volumes/telegraf/telegraf.conf
	$ docker-compose up -d telegraf
	```
	
2. Work out which options you need to change in the 8641-line version. You can use your favourite Unix text editor. To cause Telegraf to notice your changes:

	```
	$ cd ~/IOTstack
	$ docker-compose restart telegraf
	```

## <a name="logging"> Logging </a>

You can inspect Telegraf's log by:

```
$ docker logs telegraf
```

These logs are ephemeral and will disappear when your Telegraf container is rebuilt.

## <a name="upgradingTelegraf"> Upgrading Telegraf </a>

You can update most containers like this:

```bash
$ cd ~/IOTstack
$ docker-compose pull
$ docker-compose up -d
$ docker system prune
```

In words:

* `docker-compose pull` downloads any newer images;
* `docker-compose up -d` causes any newly-downloaded images to be instantiated as containers (replacing the old containers); and
* the `prune` gets rid of the outdated images.

This strategy doesn't work when a *Dockerfile* is used to build a *local image* on top of a *base image* downloaded from [*DockerHub*](https://hub.docker.com). The *local image* is what is running so there is no way for the `pull` to sense when a newer version becomes available.

The only way to know when an update to Telegraf is available is to check the [Telegraf tags page](https://hub.docker.com/_/telegraf?tab=tags&page=1&ordering=last_updated) on *DockerHub*.

Once a new version appears on *DockerHub*, you can upgrade Telegraf like this:

```bash
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull telegraf
$ docker-compose up -d telegraf
$ docker system prune
$ docker system prune
```

Breaking it down into parts:

* `build` causes the named container to be rebuilt;
* `--no-cache` tells the *Dockerfile* process that it must not take any shortcuts. It really **must** rebuild the *local image*;
* `--pull` tells the *Dockerfile* process to actually check with [*DockerHub*](https://hub.docker.com) to see if there is a later version of the *base image* and, if so, to download it before starting the build;
* `telegraf` is the named container argument required by the `build` command.

Your existing Telegraf container continues to run while the rebuild proceeds. Once the freshly-built *local image* is ready, the `up` tells `docker-compose` to do a new-for-old swap. There is barely any downtime for your service.

The `prune` is the simplest way of cleaning up. The first call removes the old *local image*. The second call cleans up the old *base image*.

### <a name="versionPinning"> Telegraf version pinning </a>

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

4. Save the file and tell `docker-compose` to rebuild the local image:

	```bash
	$ cd ~/IOTstack
	$ docker-compose up -d --build telegraf
	$ docker system prune
	``` 

	The new *local image* is built, then the new container is instantiated based on that image. The `prune` deletes the old *local image*.
	
Note:

* As well as preventing Docker from updating the *base image*, pinning will also block incoming updates to the *Dockerfile* from a `git pull`. Nothing will change until you decide to remove the pin.
