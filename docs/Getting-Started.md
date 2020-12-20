# Getting started

## Introduction to IOTstack - videos

Andreas Spiess Video #295: Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc: IOTstack
[![#295 Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc: IOTstack](http://img.youtube.com/vi/a6mjt8tWUws/0.jpg)](https://www.youtube.com/watch?v=a6mjt8tWUws)

Andreas Spiess Video #352: Raspberry Pi4 Home Automation Server (incl. Docker, OpenHAB, HASSIO, NextCloud)
[![#352 Raspberry Pi4 Home Automation Server (incl. Docker, OpenHAB, HASSIO, NextCloud)](http://img.youtube.com/vi/KJRMjUzlHI8/0.jpg)](https://www.youtube.com/watch?v=KJRMjUzlHI8)

## A word about the `sudo` command

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

The answer is different. It is different because `sudo` means "become root, and then run the command". The process of becoming root changes the home directory, and that changes the definition of `~`.

Any script designed for working with IOTstack assumes `~` (or the equivalent `$HOME` variable) expands to `/home/pi`. That assumption is invalidated if the script is run by `sudo`.

Of necessity, any script designed for working with IOTstack will have to invoke `sudo` **inside** the script **when it is required**. You do not need to second-guess the script's designer.

Please try to minimise your use of `sudo` when you are working with IOTstack. Here are some rules of thumb:

1. Is what you are about to run a script? If yes, check whether the script already contains `sudo` commands. Using `menu.sh` as the example:

	```
	$ grep -c 'sudo' ~/IOTstack/menu.sh
	28
	```
	
	There are 28 separate uses of `sudo` within `menu.sh`. That means the designer thought about when `sudo` was needed.
	
2. Did the command you **just executed** work without `sudo`? Note the emphasis on the past tense. If yes, then your work is done. If no, and the error suggests elevated privileges are necessary, then re-execute the last command like this:

	```
	$ sudo !!
	```

It takes time, patience and practice to learn when `sudo` is **actually** needed. Over-using `sudo` out of habit, or because you were following a bad example you found on the web, is a very good way to find that you have created so many problems for yourself that will need to reinstall your IOTstack. *Please* err on the side of caution!

## Download the project

You may need to install these support tools first:
 
```
$ sudo apt install -y git curl
```

> It does no harm to re-install a package that is already installed. The command either behaves as an update or does nothing, as appropriate.

IOTstack makes the following assumptions (the first three are Raspberry Pi defaults on a clean installation):

1. You are logged-in as the user "pi"
2. User "pi" has the user ID 1000
3. The home directory for user "pi" is `/home/pi/`
4. IOTstack is installed at `/home/pi/IOTstack` (with that exact spelling)

Download IOTstack manually like this:

```
$ cd
$ git clone https://github.com/SensorsIot/IOTstack.git IOTstack
```

## The Menu

The menu is used to install Docker and then build the `docker-compose.yml` file which is necessary for starting the stack.

> The menu is only an aid. It is a good idea to learn the `docker` and `docker-compose` commands if you plan on using Docker in the long run.

### Menu item: Install Docker

Please do **not** try to install `docker` and `docker-compose` via `sudo apt install`. There's more to it than that. Docker needs to be installed by `menu.sh`, like this:

```
$ cd ~/IOTstack
$ ./menu.sh
Select "Install Docker"
```

Follow the prompts. The process finishes by asking you to reboot. Do that!

### Menu item: Build Stack

`docker-compose` uses a `docker-compose.yml` file to configure all your services. The `docker-compose.yml` file is created by the menu:

```
$ cd ~/IOTstack
$ ./menu.sh
Select "Build Stack"
```

Follow the on-screen prompts and select the containers you need.

> The best advice we can give is "start small". Limit yourself to the core containers you actually need (eg Mosquitto, Node-Red, InfluxDB, Grafana, Portainer). You can always add more containers later. Some users have gone overboard with their initial selections and have run into what seem to be Raspberry Pi OS limitations.

The process finishes by asking you to bring up the stack:

```
$ cd ~/IOTstack
$ docker-compose up -d
```

The first time you run `up` the stack docker will download all the images from Dockerhub. How long this takes will depend on how many containers you selected and the speed of your internet connection.

Some containers also need to be built locally. Node-Red is an example. Depending on the Node-Red nodes you select, building the image can also take a very long time. This is especially true if you select the SQLite node.

Be patient (and ignore the huge number of warnings).

### Menu item: Docker commands

The commands in this menu execute shell scripts in the root of the project.

### Menu item: Miscellaneous commands

Some helpful commands have been added like disabling swap, or installing SSH keys from github.

## Useful commands: docker \& docker-compose

Handy rules:

* `docker` commands can be executed from anywhere, but
* `docker-compose` commands need to be executed from within `~/IOTstack`

### Starting your IOTstack

To start the stack:

```
$ cd ~/IOTstack
$ docker-compose up -d
```

Once the stack has been brought up, it will stay up until you take it down. This includes shutdowns and reboots of your Raspberry Pi. If you do not want the stack to start automatically after a reboot, you need to stop the stack before you issue the reboot command.

### Stopping your IOTstack

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

`stop` can also be used to stop individual containers, like this:

```
$ cd ~/IOTstack
$ docker-compose stop nodered
```

> there is no equivalent of `down` for a single container.

### Checking container status

You can check the status of containers with:

```
$ docker ps
```

or

```
$ cd ~/IOTstack
$ docker-compose ps
```

### Viewing container logs

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

### Restarting a container

You can restart a container in several ways:

```
$ cd ~/IOTstack
$ docker-compose restart «container»
```

where «container» is the name of the container you want to restart, like this:

```
$ docker-compose restart nodered
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

## Persistent data

Docker allows a container's designer to map folders inside a container to a folder on your disk (SD, SSD, HD). This is done with the "volumes" key in `docker-compose.yml`. Consider the following snippet for Node-Red:

```
    volumes:
      - ./volumes/nodered/data:/data
```

You read this as two paths, separated by a colon. The:

* external path is `./volumes/nodered/data`
* internal path is `/data`

In this context, the leading "." means "the folder containing `docker-compose.yml`, so the external path is actually:

* `~/IOTstack/volumes/nodered/data`

If a process running **inside** the container modifies any file or folder within `/data`, the change is mirrored **outside** the container at the same relative path within `./volumes/nodered/data` 

The same is true in reverse. Any change made to any file or folder within `./volumes/nodered/data` **outside** the container is is mirrored in the same file or folder at `/data` **inside** the container.

### Deleting persistent data

If you need a "clean slate" for a container, you can delete its volumes. Using InfluxDB as an example:

```
$ cd ~/IOTstack
$ docker-compose stop influxdb
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

This is how **most** containers behave. But there are exceptions. A good example of an exception is Mosquitto.
### Sharing files between the Pi and containers

Have a look a the [Wiki](https://sensorsiot.github.io/IOTstack/Containers/Node-RED/#sharing-files-between-node-red-and-the-host) on how to share files between Node-RED and the Pi.

## Updating Docker images

If a new version of a container image becomes available on Dockerhub, your local IOTstack can be updated by a pull command:

```
$ cd ~/IOTstack
$ docker-compose pull
$ docker-compose up -d
```

The `pull` downloads any new images. It does this without disrupting the running stack.

The `up -d` notices any newly-downloaded images, builds new containers, and swaps old-for-new. There is barely any downtime for affected containers.

### Updating images built from Dockerfiles

Some containers are built by downloading a *base* image from DockerHub, and then applying a Dockerfile to build a *local* image. Node-Red is a good example of this.

You can check if a container uses a Dockerfile by looking in its services directory:

```
$ ls ~/IOTstack/services/«container»
```

The directory will either contain a Dockerfile or it won't.

> You can also find out if a container is built using a Dockerfile by inspecting `docker-compose.yml` to see if the `build` key is present in the container's definition. 

To update a container that is built from a *local* image using a Dockerfile, proceed like this.

First, figure out the name of the *base* image. Using Node-Red as the example, there are two candidates:

```
$ docker images
REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
iotstack_nodered         latest              a38d38605ed4        22 hours ago        531MB
nodered/node-red         latest              fa3bc6f20464        2 months ago        376MB
```

It's practically guaranteed that the older image (the one created "2 months ago") is the *base* but you can confirm it by examining the first part of the Dockerfile:

```
$ head -1 ~/IOTstack/services/nodered/Dockerfile 
FROM nodered/node-red:latest
```

The image mentioned in the Dockerfile ("nodered/node-red") is the *base* image, while the other candidate ("iotstack_nodered") is the *local* image.

To rebuild a *local* image, you usually need to remove the *base* image and then use a special form of the `up` command. Using Node-Red as the example:

```
$ cd ~/IOTstack
$ docker rmi "nodered/node-red"
$ docker-compose up --build -d
```

This pulls down the updated *base* image, builds a new *local* image by running the Dockerfile, creates the new container and swaps old-for-new. There is barely any downtime for the Node-Red service.

#### Node-RED error after modifications to setup files

If you get an error after you modify Node-Red's environment, it is because of how it is built (via Dockerfile). You can usually resolve the problem with:

```
$ cd ~/IOTstack
$ docker-compose up --build -d
```

## Deleting unused images

As your system evolves and new images come down from Dockerhub, you may find that more disk space is being occupied than you expected. Try running:

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

In general, you can use the repository name to remove an image but the Image ID is sometimes needed. The most common situation where you are likely to need the Image ID is after an image has been updated on Dockerhub and pulled down to your Raspberry Pi. You will find two containers with the same name. One will be tagged "latest" (the running version) while the other will be tagged "<none>" (the prior version). You use the Image ID to resolve the ambiguity.

## The nuclear option - use with caution

You can use Git to delete all files and folders to return your folder to the freshly cloned state.

Warning: **YOU WILL LOSE ALL YOUR DATA**.

```
$ cd ~/IOTstack
$ sudo git clean -d -x -f
```

This is probably the **only** time you should ever need to use `sudo` in conjunction with `git` for IOTstack. This is not recoverable!
