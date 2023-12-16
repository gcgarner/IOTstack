# Getting Started

## About IOTstack { #conventions }

IOTstack is not a *system.* It is a set of *conventions* for assembling arbitrary collections of containers into something that has a reasonable chance of working out-of-the-box. The three most important conventions are:

1. If a container needs information to persist across restarts (and most containers do) then the container's *persistent store* will be found at:

	```
	~/IOTstack/volumes/«container»
	```
	
	Most *service definitions* examples found on the web have a scattergun approach to this problem. IOTstack imposes order on this chaos.
	
2. To the maximum extent possible, network port conflicts have been sorted out in advance.

	Sometimes this is not possible. For example, Pi-hole and AdGuardHome both offer Domain Name System services. The DNS relies on port 53. You can't have two containers claiming port 53 so the only way to avoid this is to pick *either* Pi-hole *or* AdGuardHome.
3. Where multiple containers are needed to implement a single user-facing service, the IOTstack service definition will include everything needed. A good example is NextCloud which relies on MariaDB. IOTstack implements MariaDB as a private instance which is only available to NextCloud. This strategy ensures that you are able to run your own separate MariaDB container without any risk of interference with your NextCloud service. 

## Requirements

IOTstack makes the following assumptions:

1. Your hardware is capable of running Debian or one of its derivatives. Examples that are known to work include:

	- a Raspberry Pi (typically a 3B+ or 4B)

		> The Raspberry Pi Zero W2 has been tested with IOTstack. It works but the 512MB RAM means you should not try to run too many containers concurrently.

	- Orange Pi Win/Plus [see also issue 375](https://github.com/SensorsIot/IOTstack/issues/375)
	- an Intel-based Mac running macOS plus Parallels with a Debian guest.
	- an Intel-based platform running Proxmox with a Debian guest.

2. Your host or guest system is running a reasonably-recent version of Debian or an operating system which is downstream of Debian in the Linux family tree, such as Raspberry Pi OS (aka "Raspbian") or Ubuntu.

	IOTstack is known to work in 32-bit mode but not all containers have images on DockerHub that support 320bit mode. If you are setting up a new system from scratch, you should choose a 64-bit option.

	IOTstack was known to work with Buster but it has not been tested recently. Bullseye is known to work but if you are setting up a new system from scratch, you should choose Bookworm.
	
	Please don't waste your own time trying Linux distributions from outside the Debian family tree. They are unlikely to work.

3. You are logged-in as the default user (ie not root). In most cases, this is the user with ID=1000 and is what you get by default on either a Raspberry Pi OS or Debian installation.

	This assumption is not really an IOTstack requirement as such. However, many containers assume UID=1000 exists and you are less likely to encounter issues if this assumption holds.

Please don't read these assumptions as saying that IOTstack will not run on other hardware, other operating systems, or as a different user. It is just that IOTstack gets most of its testing under these conditions. The further you get from these implicit assumptions, the more your mileage may vary.

## New installation

You have two choices:

1. If you have an **existing** system and you want to add IOTstack to it, then the [add-on](#addonInstall) method is your best choice.
2. If you are setting up a **new** system from scratch, then [PiBuilder](#pibuilderInstall) is probably your best choice. You can, however, also use the [add-on](#addonInstall) method in a green-fields installation.

### add-on method { #addonInstall }

This method assumes an **existing** system rather than a green-fields installation. The script uses the principle of least interference. It only installs the bare minimum of prerequisites and, with the exception of adding some boot time options to your Raspberry Pi (but not any other kind of hardware), makes no attempt to tailor your system.

To use this method:

1. Install `curl`:

	``` console
	$ sudo apt install -y curl
	```

2. Run the following command:

	``` console
	$ curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | bash
	```

The `install.sh` script is *designed* to be run multiple times. If the script discovers a problem, it will explain how to fix that problem and, assuming you follow the instructions, you can safely re-run the script. You can repeat this process until the script completes normally.

### PiBuilder method { #pibuilderInstall }

Compared with the [add-on method](#addonInstall), PiBuilder is far more comprehensive. PiBuilder:

1. Does everything the [add-on method](#addonInstall) does.
2. Adds support packages and debugging tools that have proven useful in the IOTstack context.
3. Installs all required system patches (see next section).
4. In addition to cloning IOTstack (this repository), PiBuilder also clones:

	* [IOTstackBackup](https://github.com/Paraphraser/IOTstackBackup) which is an alternative to the backup script supplied with IOTstack but does not require your stack to be taken down to perform backups; and
	* [IOTstackAliases](https://github.com/Paraphraser/IOTstackAliases) which provides shortcuts for common IOTstack operations.

5. Performs extra tailoring intended to deliver a rock-solid platform for IOTstack.

PiBuilder does, however, assume a **green fields** system rather than an existing installation. Although the PiBuilder scripts will *probably* work on an existing system, that scenario has never been tested so it's entirely at your own risk. 

PiBuilder actually has two specific use-cases:

1. A first-time build of a system to run IOTstack; and
2. The ability to create your own customised version of PiBuilder so that you can quickly rebuild your Raspberry Pi or Proxmox guest after a disaster. Combined with IOTstackBackup, you can go from bare metal to a running system with data restored in about half an hour.

## Required system patches

You can skip this section if you used [PiBuilder](https://github.com/Paraphraser/PiBuilder) to construct your system. That's because PiBuilder installs all necessary patches automatically.

If you used the [add-on method](#addonInstall), you should consider applying these patches by hand. Unless you know that a patch is **not** required, assume that it is needed.

### patch 1 – restrict DHCP

Run the following commands:

``` console
$ sudo bash -c '[ $(egrep -c "^allowinterfaces eth\*,wlan\*" /etc/dhcpcd.conf) -eq 0 ] && echo "allowinterfaces eth*,wlan*" >> /etc/dhcpcd.conf'
```

This patch prevents the `dhcpcd` daemon from trying to allocate IP addresses to Docker's `docker0` and `veth` interfaces. Docker assigns the IP addresses itself and `dhcpcd` trying to get in on the act can lead to a deadlock condition which can freeze your Pi.

See [Issue 219](https://github.com/SensorsIot/IOTstack/issues/219) and [Issue 253](https://github.com/SensorsIot/IOTstack/issues/253) for more information.

### patch 2 – update libseccomp2

This patch is **ONLY** for Raspbian Buster. Do **NOT** install this patch if you are running Raspbian Bullseye or Bookworm.

1.  check your OS release

    Run the following command:

    ``` console
    $ grep "PRETTY_NAME" /etc/os-release
    PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
    ```

    If you see the word "buster", proceed to step 2. Otherwise, skip this patch.

2.  if you are indeed running "buster"

    Without this patch on Buster, Docker images will fail if:

    * the image is based on Alpine and the image's maintainer updates to [Alpine 3.13](https://wiki.alpinelinux.org/wiki/Release_Notes_for_Alpine_3.13.0#time64_requirement); and/or
    * an image's maintainer updates to a library that depends on 64-bit values for *Unix epoch time* (the so-called Y2038 problem).

    To install the patch:

    ``` console
    $ sudo apt-key adv --keyserver hkps://keyserver.ubuntu.com:443 --recv-keys 04EE7237B7D453EC 648ACFD622F3D138
    $ echo "deb http://httpredir.debian.org/debian buster-backports main contrib non-free" | sudo tee -a "/etc/apt/sources.list.d/debian-backports.list"
    $ sudo apt update
    $ sudo apt install libseccomp2 -t buster-backports
    ```

### patch 3 - kernel control groups

Kernel control groups need to be enabled in order to monitor container specific
usage. This makes commands like `docker stats` fully work. Also needed for full
monitoring of docker resource usage by the telegraf container.

Enable by running (takes effect after reboot):

``` console
$ echo $(cat /boot/cmdline.txt) cgroup_memory=1 cgroup_enable=memory | sudo tee /boot/cmdline.txt
$ sudo reboot
```

## the IOTstack menu { #iotstackMenu}

The menu is used to construct your `docker-compose.yml` file. That file is read by `docker-compose` which issues the instructions necessary for starting your stack.

The menu is a great way to get started quickly but it is only an aid. It is a good idea to learn the various `docker` and `docker-compose` commands so you can use them outside the menu. It is also a good idea to study the `docker-compose.yml` generated by the menu to see how everything is put together. You will gain a lot of flexibility if you learn how to add containers by hand.

In essence, the menu is a concatenation tool which appends *service definitions* that exist inside the hidden `~/IOTstack/.templates` folder to your `docker-compose.yml`.

Once you understand what the menu does (and, more importantly, what it doesn't do), you will realise that the real power of IOTstack lies not in its menu system but resides in its [conventions](#conventions).

### menu item: Build Stack { #buildStack}

To create your first `docker-compose.yml`:

``` console
$ cd ~/IOTstack
$ ./menu.sh
Select "Build Stack"
```

Follow the on-screen prompts and select the containers you need.

> The best advice we can give is "start small". Limit yourself to the core containers you actually need (eg Mosquitto, Node-RED, InfluxDB, Grafana, Portainer). You can always add more containers later. Some users have gone overboard with their initial selections and have run into what seem to be Raspberry Pi OS limitations.

Key point:

* If you are running "new menu" (master branch) and you select Node-RED, you **must** press the right-arrow and choose at least one add-on node. If you skip this step, Node-RED will not build properly.
* Old menu forces you to choose add-on nodes for Node-RED.

The process finishes by asking you to bring up the stack:

``` console
$ cd ~/IOTstack
$ docker-compose up -d
```

The first time you run `up` the stack docker will download all the images from DockerHub. How long this takes will depend on how many containers you selected and the speed of your internet connection.

Some containers also need to be built locally. Node-RED is an example. Depending on the Node-RED nodes you select, building the image can also take a very long time. This is especially true if you select the SQLite node.

Be patient (and, if you selected the SQLite node, ignore the huge number of warnings).

### menu item: Docker commands

The commands in this menu execute shell scripts in the root of the project.

### other menu items

The old and new menus differ in the options they offer. You should come back and explore them once your stack is built and running.

## useful commands: docker & docker-compose

Handy rules:

* `docker` commands can be executed from anywhere, but
* `docker-compose` commands need to be executed from within `~/IOTstack`

### starting your IOTstack

To start the stack:

``` console
$ cd ~/IOTstack
$ docker-compose up -d
```

Once the stack has been brought up, it will stay up until you take it down. This includes shutdowns and reboots of your Raspberry Pi. If you do not want the stack to start automatically after a reboot, you need to stop the stack before you issue the reboot command.

#### logging journald errors

If you get docker logging error like:

```
Cannot create container for service [service name here]: unknown log opt 'max-file' for journald log driver
```

1. Run the command:

	``` console
	$ sudo nano /etc/docker/daemon.json
	```

2. change:

	``` json
	"log-driver": "journald",
	```

	to:

	``` json
	"log-driver": "json-file",
	```

Logging limits were added to prevent Docker using up lots of RAM if log2ram is enabled, or SD cards being filled with log data and degraded from unnecessary IO. See [Docker Logging configurations](https://docs.docker.com/config/containers/logging/configure/)

You can also turn logging off or set it to use another option for any service by using the IOTstack `docker-compose-override.yml` file mentioned at [IOTstack/Custom](Custom.md).

Another approach is to change `daemon.json` to be like this:

``` json
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "1m"
  }
}
```

The `local` driver is specifically designed to prevent disk exhaustion. Limiting log size to one megabyte also helps, particularly if you only have a limited amount of storage.

If you are familiar with system logging where it is best practice to retain logs spanning days or weeks, you may feel that one megabyte is unreasonably small. However, before you rush to increase the limit, consider that each container is the equivalent of a small computer dedicated to a single task. By their very nature, containers tend to either work as expected or fail outright. That, in turn, means that it is usually only recent container logs showing failures as they happen that are actually useful for diagnosing problems.

### starting an individual container

To start a particular container:

``` console
$ cd ~/IOTstack
$ docker-compose up -d «container»
```

### stopping your IOTstack

Stopping aka "downing" the stack stops and deletes all containers, and removes the internal network:

``` console
$ cd ~/IOTstack
$ docker-compose down
```

To stop the stack without removing containers, run:

``` console
$ cd ~/IOTstack
$ docker-compose stop
```

### stopping an individual container

`stop` can also be used to stop individual containers, like this:

``` console
$ cd ~/IOTstack
$ docker-compose stop «container»
```

This puts the container in a kind of suspended animation. You can resume the container with

``` console
$ cd ~/IOTstack
$ docker-compose start «container»
```

You can also `down` a container:

``` console
$ cd ~/IOTstack
$ docker-compose down «container»
```

<a name="downContainer"></a>Note:

* If the `down` command returns an error suggesting that you can't use it to down a container, it actually means that you have an obsolete version of `docker-compose`. You should upgrade your system. The workaround is to you the old syntax:

	``` console
	$ cd ~/IOTstack
	$ docker-compose rm --force --stop -v «container»
	```

To reactivate a container which has been stopped and removed:

``` console
$ cd ~/IOTstack
$ docker-compose up -d «container»
```

### checking container status

You can check the status of containers with:

``` console
$ docker ps
```

or

``` console
$ cd ~/IOTstack
$ docker-compose ps
```

### viewing container logs

You can inspect the logs of most containers like this:

``` console
$ docker logs «container»
```

for example:

``` console
$ docker logs nodered
```

You can also follow a container's log as new entries are added by using the `-f` flag:

``` console
$ docker logs -f nodered
```

Terminate with a Control+C. Note that restarting a container will also terminate a followed log.

### restarting a container

You can restart a container in several ways:

``` console
$ cd ~/IOTstack
$ docker-compose restart «container»
```

This kind of restart is the least-powerful form of restart. A good way to think of it is "the container is only restarted, it is not rebuilt".

If you change a `docker-compose.yml` setting for a container and/or an environment variable file referenced by `docker-compose.yml` then a `restart` is usually not enough to bring the change into effect. You need to make `docker-compose` notice the change:

``` console
$ cd ~/IOTstack
$ docker-compose up -d «container»
```

This type of "restart" rebuilds the container.

Alternatively, to force a container to rebuild (without changing either `docker-compose.yml` or an environment variable file):

``` console
$ cd ~/IOTstack
$ docker-compose up -d --force-recreate «container»
```

See also [updating images built from Dockerfiles](#updating-images-not-built-from-dockerfiles) if you need to force `docker-compose` to notice a change to a Dockerfile.

## persistent data

Docker allows a container's designer to map folders inside a container to a folder on your disk (SD, SSD, HD). This is done with the "volumes" key in `docker-compose.yml`. Consider the following snippet for Node-RED:

```yaml
volumes:
  - ./volumes/nodered/data:/data
```

You read this as two paths, separated by a colon. The:

* external path is `./volumes/nodered/data`
* internal path is `/data`

In this context, the leading "." means "the folder containing`docker-compose.yml`", so the external path is actually:

* `~/IOTstack/volumes/nodered/data`

This type of volume is a
[bind-mount](https://docs.docker.com/storage/bind-mounts/), where the
container's internal path is directly linked to the external path. All
file-system operations, reads and writes, are mapped to directly to the files
and folders at the external path.

### deleting persistent data

If you need a "clean slate" for a container, you can delete its volumes. Using InfluxDB as an example:

``` console
$ cd ~/IOTstack
$ docker-compose rm --force --stop -v influxdb
$ sudo rm -rf ./volumes/influxdb
$ docker-compose up -d influxdb
```

When `docker-compose` tries to bring up InfluxDB, it will notice this volume mapping in `docker-compose.yml`:

```yaml
    volumes:
      - ./volumes/influxdb/data:/var/lib/influxdb
```

and check to see whether `./volumes/influxdb/data` is present. Finding it not there, it does the equivalent of:

``` console
$ sudo mkdir -p ./volumes/influxdb/data
```

When InfluxDB starts, it sees that the folder on right-hand-side of the volumes mapping (`/var/lib/influxdb`) is empty and initialises new databases.

This is how **most** containers behave. There are exceptions so it's always a good idea to keep a backup.

## stack maintenance

!!! danger "Breaking update"
    Recent changes will require [manual steps](
    ../Updates/migration-network-change.md)
    or you may get an error like:  
    `ERROR: Service "influxdb" uses an undefined network "iotstack_nw"`

### update Raspberry Pi OS

You should keep your Raspberry Pi up-to-date. Despite the word "container" suggesting that *containers* are fully self-contained, they sometimes depend on operating system components ("WireGuard" is an example).

``` console
$ sudo apt update
$ sudo apt upgrade -y
```

### git pull

Although the menu will generally do this for you, it does not hurt to keep your local copy of the IOTstack repository in sync with the master version on GitHub.

``` console
$ cd ~/IOTstack
$ git pull
```

### container image updates

There are two kinds of images used in IOTstack:

* Those not built using Dockerfiles (the majority)
* Those built using Dockerfiles (special cases)

	> A Dockerfile is a set of instructions designed to customise an image before it is instantiated to become a running container.

The easiest way to work out which type of image you are looking at is to inspect the container's service definition in your `docker-compose.yml` file. If the service definition contains the:

* `image:` keyword then the image is **not** built using a Dockerfile.
* `build:` keyword then the image **is** built using a Dockerfile.

#### updating images not built from Dockerfiles

If new versions of this type of image become available on DockerHub, your local IOTstack copies can be updated by a `pull` command:

``` console
$ cd ~/IOTstack
$ docker-compose pull
$ docker-compose up -d
$ docker system prune
```

The `pull` downloads any new images. It does this without disrupting the running stack.

The `up -d` notices any newly-downloaded images, builds new containers, and swaps old-for-new. There is barely any downtime for affected containers.

#### updating images built from Dockerfiles

Containers built using Dockerfiles have a two-step process:

1. A *base* image is downloaded from from DockerHub; and then
2. The Dockerfile "runs" to build a *local* image.

Node-RED is a good example of a container built from a Dockerfile. The Dockerfile defines some (or possibly all) of your add-on nodes, such as those needed for InfluxDB or Tasmota.

There are two separate update situations that you need to consider:

* If your Dockerfile changes; or
* If a newer base image appears on DockerHub

Node-RED also provides a good example of why your Dockerfile might change: if you decide to add or remove add-on nodes.

Note:

* You can also add nodes to Node-RED using Manage Palette.

##### when Dockerfile changes (*local* image only)

When your Dockerfile changes, you need to rebuild like this:

``` console
$ cd ~/IOTstack
$ docker-compose up --build -d «container»
$ docker system prune
```

This only rebuilds the *local* image and, even then, only if `docker-compose` senses a *material* change to the Dockerfile.

If you are trying to force the inclusion of a later version of an add-on node, you need to treat it like a [DockerHub update](#updating-images-built-from-dockerfiles).

Key point:

* The *base* image is not affected by this type of update.

Note:

* You can also use this type of build if you get an error after modifying Node-RED's environment:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up --build -d nodered
	```

##### when DockerHub updates (*base* and *local* images)

When a newer version of the *base* image appears on DockerHub, you need to rebuild like this:

``` console
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull «container»
$ docker-compose up -d «container»
$ docker system prune
$ docker system prune
```

This causes DockerHub to be checked for the later version of the *base* image, downloading it as needed.

Then, the Dockerfile is run to produce a new *local* image. The Dockerfile run happens even if a new *base* image was not downloaded in the previous step.

### deleting unused images

As your system evolves and new images come down from DockerHub, you may find that more disk space is being occupied than you expected. Try running:

``` console
$ docker system prune
```

This recovers anything no longer in use. Sometimes multiple `prune` commands are needed (eg the first removes an old *local* image, the second removes the old *base* image).

If you add a container via `menu.sh` and later remove it (either manually or via `menu.sh`), the associated images(s) will probably persist. You can check which images are installed via:

``` console
$ docker images

REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
influxdb                 latest              1361b14bf545        5 days ago          264MB
grafana/grafana          latest              b9dfd6bb8484        13 days ago         149MB
iotstack_nodered         latest              21d5a6b7b57b        2 weeks ago         540MB
portainer/portainer-ce   latest              5526251cc61f        5 weeks ago         163MB
eclipse-mosquitto        latest              4af162db6b4c        6 weeks ago         8.65MB
nodered/node-red         latest              fa3bc6f20464        2 months ago        376MB
portainer/portainer      latest              dbf28ba50432        2 months ago        62.5MB
```

Both "Portainer CE" and "Portainer" are in that list. Assuming "Portainer" is no longer in use, it can be removed by using either its repository name or its Image ID. In other words, the following two commands are synonyms:

``` console
$ docker rmi portainer/portainer
$ docker rmi dbf28ba50432
```

In general, you can use the repository name to remove an image but the Image ID is sometimes needed. The most common situation where you are likely to need the Image ID is after an image has been updated on DockerHub and pulled down to your Raspberry Pi. You will find two containers with the same name. One will be tagged "latest" (the running version) while the other will be tagged "\<none\>" (the prior version). You use the Image ID to resolve the ambiguity.

### pinning to specific versions

See [container image updates](#container-image-updates) to understand how to tell the difference between images that are used "as is" from DockerHub versus those that are built from local Dockerfiles.

Note:

* You should **always** visit an image's DockerHub page before pinning to a specific version. This is the only way to be certain that you are choosing the appropriate version suffix.

To pin an image to a specific version:

* If the image comes straight from DockerHub, you apply the pin in `docker-compose.yml`. For example, to pin Grafana to version 7.5.7, you change:

	```yaml
	  grafana:
	    container_name: grafana
	    image: grafana/grafana:latest
	    …
	```

	to:

	```yaml
	  grafana:
	    container_name: grafana
	    image: grafana/grafana:7.5.7
	    …
	```

	To apply the change, "up" the container:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d grafana
	```

* If the image is built using a local Dockerfile, you apply the pin in the Dockerfile. For example, to pin Mosquitto to version 1.6.15, edit `~/IOTstack/.templates/mosquitto/Dockerfile` to change:

	```dockerfile
	# Download base image
	FROM eclipse-mosquitto:latest
	…
	```

	to:

	```dockerfile
	# Download base image
	FROM eclipse-mosquitto:1.6.15
	…
	```

	To apply the change, "up" the container and pass the `--build` flag:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d --build mosquitto
	```

