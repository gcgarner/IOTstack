# Getting Started

## <a name="introAndVideos"> introduction to IOTstack - videos </a>

Andreas Spiess Video #295: Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc: IOTstack

[![#295 Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc: IOTstack](http://img.youtube.com/vi/a6mjt8tWUws/0.jpg)](https://www.youtube.com/watch?v=a6mjt8tWUws)

Andreas Spiess Video #352: Raspberry Pi4 Home Automation Server (incl. Docker, OpenHAB, HASSIO, NextCloud)

[![#352 Raspberry Pi4 Home Automation Server (incl. Docker, OpenHAB, HASSIO, NextCloud)](http://img.youtube.com/vi/KJRMjUzlHI8/0.jpg)](https://www.youtube.com/watch?v=KJRMjUzlHI8)

## <a name="assumptions"> assumptions </a>

IOTstack makes the following assumptions:

1. Your hardware is a Raspberry Pi (typically a 3B+ or 4B)
2. It has a reasonably-recent version of Raspberry Pi OS (aka "Raspbian") installed which has been kept up-to-date with:

	```
	$ sudo apt update
	$ sudo apt upgrade -y
	```

3. You are logged-in as the user "pi"
4. User "pi" has the user ID 1000
5. The home directory for user "pi" is `/home/pi/`
6. IOTstack is installed at `/home/pi/IOTstack` (with that exact spelling).

The first five assumptions are Raspberry Pi defaults on a clean installation. The sixth is what you get if you follow these instructions faithfully.

> Please don't read these assumptions as saying that IOTstack will not run on other hardware, other operating systems, or as a different user. It is just that IOTstack gets most of its testing under these conditions. The further you get from these implicit assumptions, the more your mileage may vary.

## <a name="newInstallation"> new installation </a>

### <a name="autoInstall"> automatic (recommended) </a>

1. Install `curl`:

	```
	$ sudo apt install -y curl
	```

2. Run the following command:

	```
	$ curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | bash
	```

3. Run the menu and choose your containers:

	```
	$ cd ~/IOTstack
	$ ./menu.sh
	```

4. Bring up your stack:

	```
	$ cd ~/IOTstack
	$ docker-compose up -d
	```

### <a name="manualInstall"> manual </a>

1. Install `git`:

	```
	$ sudo apt install -y git
	```

2. Clone IOTstack:

	* If you want "new menu":

		```
		$ git clone https://github.com/SensorsIot/IOTstack.git ~/IOTstack
		```

	* If you prefer "old menu":

		```
		$ git clone -b old-menu https://github.com/SensorsIot/IOTstack.git ~/IOTstack
		```

3. Run the menu and choose your containers:

	```
	$ cd ~/IOTstack
	$ ./menu.sh
	```

	Note:

	* If you are running "old menu" for the first time, you will be guided to "Install Docker". That will end in a reboot, after which you should re-enter the menu and choose your containers.

4. Bring up your stack:

	```
	$ cd ~/IOTstack
	$ docker-compose up -d
	```

### <a name="scriptedInstall"> scripted </a>

If you prefer to automate your installations using scripts, see:

* [Installing Docker for IOTstack](https://gist.github.com/Paraphraser/d119ae81f9e60a94e1209986d8c9e42f#scripting-iotstack-installations).

## <a name="gcgarnerMigrate"> migrating from the old repo (gcgarner)? </a>

If you are still running on gcgarner/IOTstack and need to migrate to SensorsIot/IOTstack, see:

* [Migrating IOTstack from gcgarner to SensorsIot](./gcgarner-migration.md).

## <a name="recommendedPatches"> recommended system patches </a>

### <a name="patch1DHCP"> patch 1 – restrict DHCP </a>

Run the following commands:

```
$ sudo bash -c '[ $(egrep -c "^allowinterfaces eth0,wlan0" /etc/dhcpcd.conf) -eq 0 ] && echo "allowinterfaces eth0,wlan0" >> /etc/dhcpcd.conf'
$ sudo reboot
```

See [Issue 219](https://github.com/SensorsIot/IOTstack/issues/219) and [Issue 253](https://github.com/SensorsIot/IOTstack/issues/253) for more information.

### <a name="patch2DHCP"> patch 2 – update libseccomp2</a>

If you don't have this patch in place, Docker images that are based on Alpine will fail if an image's maintainer updates to [Alpine 3.13](https://wiki.alpinelinux.org/wiki/Release_Notes_for_Alpine_3.13.0#time64_requirement).

```
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138
$ echo "deb http://httpredir.debian.org/debian buster-backports main contrib non-free" | sudo tee -a "/etc/apt/sources.list.d/debian-backports.list"
$ sudo apt update
$ sudo apt install libseccomp2 -t buster-backports
```

## <a name="aboutSudo"> a word about the `sudo` command </a>

Many first-time users of IOTstack get into difficulty by misusing the `sudo` command. The problem is best understood by example. In the following, you would expect `~` (tilde) to expand to `/home/pi`. It does:

```
$ echo ~/IOTstack
/home/pi/IOTstack
```

The command below sends the same `echo` command to `bash` for execution. This is what happens when you type the name of a shell script. You get a new instance of `bash` to run the script:

```
$ bash -c 'echo ~/IOTstack'
/home/pi/IOTstack
```

Same answer. Again, this is what you expect. But now try it with `sudo` on the front:

```
$ sudo bash -c 'echo ~/IOTstack'
/root/IOTstack
```

Different answer. It is different because `sudo` means "become root, and then run the command". The process of becoming root changes the home directory, and that changes the definition of `~`.

Any script designed for working with IOTstack assumes `~` (or the equivalent `$HOME` variable) expands to `/home/pi`. That assumption is invalidated if the script is run by `sudo`.

Of necessity, any script designed for working with IOTstack will have to invoke `sudo` **inside** the script **when it is required**. You do not need to second-guess the script's designer.

Please try to minimise your use of `sudo` when you are working with IOTstack. Here are some rules of thumb:

1. Is what you are about to run a script? If yes, check whether the script already contains `sudo` commands. Using `menu.sh` as the example:

	```
	$ grep -c 'sudo' ~/IOTstack/menu.sh
	28
	```

	There are numerous uses of `sudo` within `menu.sh`. That means the designer thought about when `sudo` was needed.

2. Did the command you **just executed** work without `sudo`? Note the emphasis on the past tense. If yes, then your work is done. If no, and the error suggests elevated privileges are necessary, then re-execute the last command like this:

	```
	$ sudo !!
	```

It takes time, patience and practice to learn when `sudo` is **actually** needed. Over-using `sudo` out of habit, or because you were following a bad example you found on the web, is a very good way to find that you have created so many problems for yourself that will need to reinstall your IOTstack. *Please* err on the side of caution!

## <a name="theMenu"> the IOTstack menu </a>

The menu is used to install Docker and then build the `docker-compose.yml` file which is necessary for starting the stack.

> The menu is only an aid. It is a good idea to learn the `docker` and `docker-compose` commands if you plan on using Docker in the long run.

### <a name="menuInstallDocker"> menu item: Install Docker </a> (old menu only)

Please do **not** try to install `docker` and `docker-compose` via `sudo apt install`. There's more to it than that. Docker needs to be installed by `menu.sh`. The menu will prompt you to install docker if it detects that docker is not already installed. You can manually install it from within the `Native Installs` menu:

```
$ cd ~/IOTstack
$ ./menu.sh
Select "Native Installs"
Select "Install Docker and Docker-Compose"
```

Follow the prompts. The process finishes by asking you to reboot. Do that!

Note:

* New menu (master branch) automates this step.

### <a name="menuBuildStack"> menu item: Build Stack </a>

`docker-compose` uses a `docker-compose.yml` file to configure all your services. The `docker-compose.yml` file is created by the menu:

```
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

```
$ cd ~/IOTstack
$ docker-compose up -d
```

The first time you run `up` the stack docker will download all the images from DockerHub. How long this takes will depend on how many containers you selected and the speed of your internet connection.

Some containers also need to be built locally. Node-RED is an example. Depending on the Node-RED nodes you select, building the image can also take a very long time. This is especially true if you select the SQLite node.

Be patient (and ignore the huge number of warnings).

### <a name="menuDockerCommands"> menu item: Docker commands </a>

The commands in this menu execute shell scripts in the root of the project.

### <a name="otherMenuItems"> other menu items </a>

The old and new menus differ in the options they offer. You should come back and explore them once your stack is built and running.

## <a name="switchingMenus"> switching menus </a>

At the time of writing, IOTstack supports three menus:

* "Old Menu" on the `old-menu` branch. This was inherited from [gcgarner/IOTstack](https://github.com/gcgarner/IOTstack).
* "New Menu" on the `master` branch. This is the current menu.
* "New New Menu" on the `experimental` branch. This is under development.

With a few precautions, you can switch between git branches as much as you like without breaking anything. The basic check you should perform is:

```
$ cd ~/IOTstack
$ git status
```

Check the results to see if any files are marked as "modified". For example:

```
modified:   .templates/mosquitto/Dockerfile
```

Key point:

* Files marked "untracked" do not matter. You only need to check for "modified" files because those have the potential to stop you from switching branches cleanly.

The way to avoid potential problems is to move any modified files to one side and restore the unmodified original. For example:

```
$ mv .templates/mosquitto/Dockerfile .templates/mosquitto/Dockerfile.save
$ git checkout -- .templates/mosquitto/Dockerfile
```

When `git status` reports no more "modified" files, it is safe to switch your branch.

### <a name="menuMasterBranch"> current menu (master branch) </a>

```
$ cd ~/IOTstack/
$ git pull
$ git checkout master
$ ./menu.sh
```

### <a name="menuOldMenuBranch"> old menu (old-menu branch)</a>

```
$ cd ~/IOTstack/
$ git pull
$ git checkout old-menu
$ ./menu.sh
```

### <a name="menuExperimentalBranch"> experimental branch </a>

Switch to the experimental branch to try the latest and greatest features.

```
$ cd ~/IOTstack/
$ git pull
$ git checkout experimental
$ ./menu.sh
```

Notes:

* Please make sure you have a good backup before you start.
* The experimental branch may be broken, or may break your setup.
* Please report any issues.
* Remember:

	* you can switch git branches as much as you like without breaking anything.
	* simply launching the menu (any version) won't change anything providing you exit before letting the menu complete.
	* running the menu *to completion* **will** change your docker-compose.yml and supporting structures in `~/IOTstack/services`.
	* running `docker-compose up -d` will change your running containers.

* The way back is to take down your stack, restore a backup, and bring up your stack again.

## <a name="dockerAndCompose"> useful commands: docker & docker-compose </a>

Handy rules:

* `docker` commands can be executed from anywhere, but
* `docker-compose` commands need to be executed from within `~/IOTstack`

### <a name="upIOTstack"> starting your IOTstack </a>

To start the stack:

```
$ cd ~/IOTstack
$ docker-compose up -d
```

Once the stack has been brought up, it will stay up until you take it down. This includes shutdowns and reboots of your Raspberry Pi. If you do not want the stack to start automatically after a reboot, you need to stop the stack before you issue the reboot command.

#### <a name="journaldErrors"> logging journald errors </a>

If you get docker logging error like:

```
Cannot create container for service [service name here]: unknown log opt 'max-file' for journald log driver
```

1. Run the command:

	```
	sudo nano /etc/docker/daemon.json
	```

2. change:

	```
	"log-driver": "journald",
	```

	to:

	```
	"log-driver": "json-file",
	```

Logging limits were added to prevent Docker using up lots of RAM if log2ram is enabled, or SD cards being filled with log data and degraded from unnecessary IO. See [Docker Logging configurations](https://docs.docker.com/config/containers/logging/configure/)

You can also turn logging off or set it to use another option for any service by using the IOTstack `docker-compose-override.yml` file mentioned at [IOTstack/Custom](https://sensorsiot.github.io/IOTstack/Custom/).

### <a name="upContainer"> starting an individual container </a>

To start the stack:

```
$ cd ~/IOTstack
$ docker-compose up -d «container»
```

### <a name="downIOTstack"> stopping your IOTstack </a>

Stopping aka "downing" the stack stops and deletes all containers, and removes the internal network:

```
$ cd ~/IOTstack
$ docker-compose down
```

To stop the stack without removing containers, run:

```
$ cd ~/IOTstack
$ docker-compose stop
```

### <a name="downContainer"> stopping an individual container </a>

`stop` can also be used to stop individual containers, like this:

```
$ cd ~/IOTstack
$ docker-compose stop «container»
```

This puts the container in a kind of suspended animation. You can resume the container with

```
$ cd ~/IOTstack
$ docker-compose start «container»
```

There is no equivalent of `down` for a single container. It needs two commands:

```
$ cd ~/IOTstack
$ docker-compose stop «container»
$ docker-compose rm -f «container»
```

To reactivate a container which has been stopped and removed:

```
$ cd ~/IOTstack
$ docker-compose up -d «container»
```

### <a name="dockerPS"> checking container status </a>

You can check the status of containers with:

```
$ docker ps
```

or

```
$ cd ~/IOTstack
$ docker-compose ps
```

### <a name="dockerLogs"> viewing container logs </a>

You can inspect the logs of most containers like this:

```
$ docker logs «container»
```

for example:

```
$ docker logs nodered
```

You can also follow a container's log as new entries are added by using the `-f` flag:

```
$ docker logs -f nodered
```

Terminate with a Control+C. Note that restarting a container will also terminate a followed log.

### <a name="restartContainer"> restarting a container </a>

You can restart a container in several ways:

```
$ cd ~/IOTstack
$ docker-compose restart «container»
```

This kind of restart is the least-powerful form of restart. A good way to think of it is "the container is only restarted, it is not rebuilt".

If you change a `docker-compose.yml` setting for a container and/or an environment variable file referenced by `docker-compose.yml` then a `restart` is usually not enough to bring the change into effect. You need to make `docker-compose` notice the change:

```
$ cd ~/IOTstack
$ docker-compose up -d «container»
```

This type of "restart" rebuilds the container.

Alternatively, to force a container to rebuild (without changing either `docker-compose.yml` or an environment variable file):

```
$ cd ~/IOTstack
$ docker-compose stop «container»
$ docker-compose rm -f «container»
$ docker-compose up -d «container»
```

See also [updating images built from Dockerfiles](#updateDockerfile) if you need to force `docker-compose` to notice a change to a Dockerfile.

## <a name="persistentStore"> persistent data </a>

Docker allows a container's designer to map folders inside a container to a folder on your disk (SD, SSD, HD). This is done with the "volumes" key in `docker-compose.yml`. Consider the following snippet for Node-RED:

```
volumes:
  - ./volumes/nodered/data:/data
```

You read this as two paths, separated by a colon. The:

* external path is `./volumes/nodered/data`
* internal path is `/data`

In this context, the leading "." means "the folder containing `docker-compose.yml`", so the external path is actually:

* `~/IOTstack/volumes/nodered/data`

If a process running **inside** the container modifies any file or folder within:

```
/data
```

the change is mirrored **outside** the container at the same relative path within:

```
~/IOTstack/volumes/nodered/data
```

The same is true in reverse. Any change made to any file or folder **outside** the container within:

```
~/IOTstack/volumes/nodered/data
```

is mirrored at the same relative path **inside** the container at:

```
/data
```

### <a name="deletePersistentStore"> deleting persistent data </a>

If you need a "clean slate" for a container, you can delete its volumes. Using InfluxDB as an example:

```
$ cd ~/IOTstack
$ docker-compose stop influxdb
$ docker-compose rm -f influxdb
$ sudo rm -rf ./volumes/influxdb
$ docker-compose up -d influxdb
```

When `docker-compose` tries to bring up InfluxDB, it will notice this volume mapping in `docker-compose.yml`:

```
    volumes:
      - ./volumes/influxdb/data:/var/lib/influxdb
```

and check to see whether `./volumes/influxdb/data` is present. Finding it not there, it does the equivalent of:

```
$ sudo mkdir -p ./volumes/influxdb/data
```

When InfluxDB starts, it sees that the folder on right-hand-side of the volumes mapping (`/var/lib/influxdb`) is empty and initialises new databases.

This is how **most** containers behave. But there are exceptions. A good example of an exception is Mosquitto which does not re-initialise correctly so you should avoid removing its persistent store.

## <a name="stackMaintenance"> stack maintenance </a>

### <a name="raspbianUpdates"> update Raspberry Pi OS </a>

You should keep your Raspberry Pi up-to-date. Despite the word "container" suggesting that *containers* are fully self-contained, they sometimes depend on operating system components ("WireGuard" is an example).

```
$ sudo apt update
$ sudo apt upgrade -y
```

### <a name="gitUpdates"> git pull </a>

Although the menu will generally do this for you, it does not hurt to keep your local copy of the IOTstack repository in sync with the master version on GitHub.

```
$ cd ~/IOTstack
$ git pull
```

### <a name="imageUpdates"> container image updates </a>

There are two kinds of images used in IOTstack:

* Those not built using Dockerfiles (the majority)
* Those built using Dockerfiles (special cases)

	> A Dockerfile is a set of instructions designed to customise an image before it is instantiated to become a running container.

The easiest way to work out which type of image you are looking at is to inspect the container's service definition in your `docker-compose.yml` file. If the service definition contains the:

* `image:` keyword then the image is **not** built using a Dockerfile.
* `build:` keyword then the image **is** built using a Dockerfile.

#### <a name="updateNonDockerfile"> updating images not built from Dockerfiles </a>

If new versions of this type of image become available on DockerHub, your local IOTstack copies can be updated by a `pull` command:

```
$ cd ~/IOTstack
$ docker-compose pull
$ docker-compose up -d
$ docker system prune
```

The `pull` downloads any new images. It does this without disrupting the running stack.

The `up -d` notices any newly-downloaded images, builds new containers, and swaps old-for-new. There is barely any downtime for affected containers.

#### <a name="updateDockerfile"> updating images built from Dockerfiles </a>

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

##### <a name="buildDockerfile"> when Dockerfile changes (*local* image only) </a>

When your Dockerfile changes, you need to rebuild like this:

```
$ cd ~/IOTstack
$ docker-compose up --build -d «container»
$ docker system prune
```

This only rebuilds the *local* image and, even then, only if `docker-compose` senses a *material* change to the Dockerfile.

If you are trying to force the inclusion of a later version of an add-on node, you need to treat it like a [DockerHub update](#rebuildDockerfile).

Key point:

* The *base* image is not affected by this type of update.

Note:

* You can also use this type of build if you get an error after modifying Node-RED's environment:

	```
	$ cd ~/IOTstack
	$ docker-compose up --build -d nodered
	```

##### <a name="rebuildDockerfile"> when DockerHub updates (*base* and *local* images) </a>

When a newer version of the *base* image appears on DockerHub, you need to rebuild like this:

```
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull «container»
$ docker-compose up -d «container»
$ docker system prune
```

This causes DockerHub to be checked for the later version of the *base* image, downloading it as needed.

Then, the Dockerfile is run to produce a new *local* image. The Dockerfile run happens even if a new *base* image was not downloaded in the previous step.

### <a name="dockerPrune"> deleting unused images </a>

As your system evolves and new images come down from DockerHub, you may find that more disk space is being occupied than you expected. Try running:

```
$ docker system prune
```

This recovers anything no longer in use.

If you add a container via `menu.sh` and later remove it (either manually or via `menu.sh`), the associated images(s) will probably persist. You can check which images are installed via:

```
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

```
$ docker rmi portainer/portainer
$ docker rmi dbf28ba50432
```

In general, you can use the repository name to remove an image but the Image ID is sometimes needed. The most common situation where you are likely to need the Image ID is after an image has been updated on DockerHub and pulled down to your Raspberry Pi. You will find two containers with the same name. One will be tagged "latest" (the running version) while the other will be tagged "\<none\>" (the prior version). You use the Image ID to resolve the ambiguity.

## <a name="nuclearOption"> the nuclear option - use with caution </a>

You can use Git to delete all files and folders to return your folder to the freshly cloned state.

Warning: **YOU WILL LOSE ALL YOUR DATA**.

```
$ cd ~/IOTstack
$ sudo git clean -d -x -f
```

This is probably the **only** time you should ever need to use `sudo` in conjunction with `git` for IOTstack. This is not recoverable!
