# Announcements 
The bulk of the README has moved to the Wiki. Please check it out [here](https://github.com/gcgarner/IOTstack/wiki)
* Added Pi-Hole
* Added zigbee2mqtt (needs wiki)
* Added rclone for Google Drive Backups
* Fixed Hass.io (now has a seperate menu installation) 
* Added Telegraf (needs wiki)
* Plex added
* Tasmoadmin (needs wiki)
* Fixed Tasmoadmin not starting after reboot

***
## Highlighted topics
* [Bluetooth and Node-RED](https://github.com/gcgarner/IOTstack/wiki/Node-RED#using-bluetooth)
* [Saving files to disk inside containers](https://github.com/gcgarner/IOTstack/wiki/Node-RED#sharing-files-between-node-red-and-the-host)
* [Updating the Project](https://github.com/gcgarner/IOTstack/wiki/Updating-the-Project)

 ***
# Coming soon
- [EspurinoHub](https://hub.docker.com/r/humbertosales/espruinohub-docker-rpi)
***

# IOTstack
Docker stack for getting started on IoT on the Raspberry Pi.

This Docker stack consists of:
  * Node-RED
  * Grafana
  * InfluxDB
  * Postgres
  * Mosquitto mqtt
  * Portainer
  * Adminer
  * openHAB
  * Home Assistant (HASSIO)
  * zigbee2mqtt
  * Pi-Hole
  * TasmoAdmin (parial wiki)
  * Plex media server
  * Telegraf (wiki coming soon)

In addition, there is a write-up and some scripts to get a dynamic DNS via duckdns and VPN up and running.

Firstly what is docker? The correct question is "what are containers?". Docker is just one of the utilities to run container.

Container can be thought of as ultra-minimal virtual machines, they are a collection of binaries that run in a sandbox environment. You download a preconfigured base image and create a new container and only the differences between the base and your "VM" are stored.
Containers don't have [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)s so generally the way you interact with them is via web services or you can launch into a terminal.
One of the major advantages is that the image comes mostly preconfigured.  

There are pro's and cons for using native installs vs containers. For me, one of the best parts of containers is that it doesn't "clutter" your device, and if you don't need Postgres anymore then just stop the container and delete it and it's like it was never there.

It's not advised to try to run the native version of an app and the docker version, the container will fail. It would be best to install this on a fresh system.

For those looking for a script that installs native applications check out [Peter Scargill's script](https://tech.scargill.net/the-script/)
  
# Tested platform
Raspberry Pi 3B and 4B Raspbian (Buster)

## Older Pi's
Docker will not run on a PiZero or A model 1 because of the CPU. It has not been tested on a Model 2. You can still use Peter Scargill's [script](https://tech.scargill.net/the-script/)

## Running under a virtual machine
For those wanting to test out the script in a Virtual Machine before installing on their Pi there are some limitations. The script is designed to work with Debian based distos. Not all the container have x86_64 images. For example Portainer does not and will give an error when you try and start the stack. Please see the pinned issue [#29](https://github.com/gcgarner/IOTstack/issues/29), there is more info there.

# Feature Requests
Please direct all feature requests to [Discord](https://discord.gg/W45tD83)
  
# Youtube reference
This repo was originally inspired by Andreas Spiess's video on using some of these tools. Some containers have been added to extend its functionality.

[YouTube video](https://www.youtube.com/watch?v=JdV4x925au0): This is an alternative approach to the setup. Be sure to watch the video for the instructions. Just note that the network addresses are different, see note below

# Download the project

On the lite image you will need to install git first 
```
sudo apt-get install git
```
Then download with
```
git clone https://github.com/gcgarner/IOTstack.git ~/IOTstack
```
Due to some script restraints, this project needs to be stored in ~/IOTstack

To enter the directory run:
```
cd ~/IOTstack
```
# The Menu
I've added a menu to make things easier. It is good however to familiarise yourself with how things are installed.
The menu can be used to install docker and then build the docker-compose.yml file necessary for starting the stack and it runs a few common commands. I do recommend you start to learn the docker and docker-compose commands if you plan using docker in the long run. I've added several helper scripts, have a look inside.

Navigate to the project folder and run `./menu.sh`

## Installing from the menu
Select the first option and follow the prompts

## Build the docker-compose file
docker-compose uses the `docker-compose.yml` file to configure all the services. Run through the menu to select the options you want to install.

## Docker commands
This menu executes shell scripts in the root of the project. It is not necessary to run them from the menu. Open up the shell script files to see what is inside and what they do

## Miscellaneous commands
Some helpful commands have been added like disabling swap

# Running Docker commands
From this point on make sure you are executing the commands from inside the project folder. Docker-compose commands need to be run from the folder where the docker-compose.yml is located. If you want to move the folder make sure you move the whole project folder.

## Starting and Stopping containers
to start the stack navigate to the project folder containing the docker-compose.yml file

To start the stack run:
`docker-compose up -d` or `./scripts/start.sh`

To stop:
`docker-compose down` or `./scripts/stop.sh`

The first time you run 'start' the stack docker will download all the images for the web. Depending on how many containers you selected and your internet speed this can take a long while.

The 'docker-compose down' command stops the containers then deletes them. The alternative is to run 'docker-compose stop' which does not delete the containers.

## Persistent data
Docker allows you to map folders inside your containers to folders on the disk. This is done with the "volume" key. There are two types of volumes. Any modification to the container reflects in the volume.

# See Wiki for further info
[Wiki](https://github.com/gcgarner/IOTstack/wiki)


# Add to the project
Feel free to add your comments on features or images that you think should be added.
