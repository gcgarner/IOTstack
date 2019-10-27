# IOTstack
Docker stack for getting started on IOT on the Raspberry PI

This Docker stack consists of:
  * nodered
  * grafana
  * influxDB
  * postgres
  * mosquitto mqtt
  * portainer
  * adminer

In addition there is a write-up and some scripts to get a dynamic DNS via duckdns and VPN up and running.

Firstly what is docker? The corrent question is "what are containers?". Docker is just one of the utilities to run container.

Container can be thought of as ultra minimal virtual machines. You download a preconfigured base image and create a new container and only the differences between the base and your "VM" are stored.
Containers dont have GUIs so generally the way you interact with them are via web services or you can launch into a terminal.
One of the major advantages is that the image comes mostly preconfigured.  
  
# Tested platform
Raspberry Pi 3B and 4B Raspbian (Buster)
  
# Youtube reference
This repo was originally inspired by Andreas Spiess's video on using some of these tools. Some containers have been added to extend its functionality

https://www.youtube.com/watch?v=JdV4x925au0 
This is an alternative approach to the setup. Be sure to watch the video for the instructions. Just note that the network addresses are different, see note below

For those looking for a script that installs native applications check out Peter Scargill's script
https://tech.scargill.net/the-script/

There are pro's and con's for using native installs vs containers. For me one of the best part of containers is that it doesnt "clutter" your device, and if you don't need Postgres anymore then just stop the container and delete it and its like it was never there.

It's not advided to try run the native version of an app and the docker version, the contianer will fail. It would be best to install this on a fresh system. 

## Download the project

```
git clone https://github.com/gcgarner/IOTstack.git ~/IOTstack
```
Due to some script restraints this project needs to ve stored in ~/IOTstack

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
`docker-compose up -d` or `./start.sh`

To stop:
`docker-compose down` or `./stop.sh`

The first time you run start the stack docker will download all the images for the web. Depending on how many containers you selected and your internet speed this can take a long while.

The "docker-compose down" command stops the containers then deletes them. The alternative is to run "docker-compose stop" which does not delete the containers.

## Persistent data
Docker allowes you to map folders inside your containers to folders on the disk. This is done with "volume" key. There are two types of volumes. Any modification to the container reflects in the volume.

## Updating the images
If a new version of a container image is available on docker hub it can be updated by a pull command.

Use the `docker-compose down` command to stop the stack

Pull the latest version from docker hub with one of the following command

`docker-compose pull` or the script `./scritps/update.sh`

## Node-RED error after modifications to setup files
The Node-RED image differs from the rest of the images in this project. It uses the "build" key. It uses a dockerfile for the setup to inject the nodes for preinstallation. If you get an error for Node-RED run `docker-compose build` then `docker-compose up -d`

## Deleting containers, volumes and images

`./prune-images.sh` will remove all images not assosiated with a container. IF you run it while the stack is up it will ignore any in use image. If you run this while you stack is down it will delete all images and you will have to redownload all images from scratch. This command can be helful to reclaim diskspace after updating your images, just make sure to run it while your stack is running as not to delete the images in use. (your data will still be safe in your volume mapping)

## Deleting folder volumes
If you want to delete the influxdb data folder run the following command `sudo rm -r volumes/influxdb/`. Only the data folder is deleted leaving the env file intact. review the docker-compose.yml file to see where the file volumes are stored.

You can use git to delete all files and folders to return your folder to the freshly cloned state, AS IN YOU WILL LOSE ALL YOUR DATA.
`sudo git clean -d -x -f` will return the working tree to its clean state. USE WITH CAUTION!

## Networking

The docker-compose instruction creates a internal network for the containers to communicate in, the ports get exposed to the PI's IP address when you want to connect from outside. It also creates a "DNS" the name being the container name. So it is important to note that when one container talks to another they talk by name. All the containers names are lowercase like nodered,influxdb...

An easy way to find out your IP is by typing `ifconfig` in the terminal and look next to eth0 or wlan0 for your IP. It is hightly recommended that you set a static IP for your PI or at least reserve a IP on your router so that you know it

Check the docker-compose.yml to see which ports have been used

![net](https://user-images.githubusercontent.com/46672225/66702353-0bcc4080-ed07-11e9-994b-62219f50b096.png)

### Examples
You want to connect your nodered to your mqtt server.
In nodered drop an mqtt node, when you need to specify the address type `mosquitto`

You want to connect to your influxdb from grafana. 
You are in the Docker network and you need to use the name of the Container.
The address you specify in the grafana is http://influx:8086

You want to connect to the web interface of grafana from you laptop.
Now you are outside the container environmnet you type PI's IP eg 192.168.n.m:3000

# Portainer
https://hub.docker.com/r/portainer/portainer/

Portainer is a great application for managing Docker. In your web browser navigate to `#yourip:9000`. You will be asked to choose a password. In the next window select 'Local' and connect, it shouldn't ask you this again. From here you can play around, click local, and take a look around. This can help you find unused images/containers. On the Containers section there are 'Quick actions' to view logs and other stats. Note: This can all be done from the CLI but portainer just makes it much much easier. 

If you have forgotten the password you created for the container, stop the stack remove portainers volume with `sudo rm -r ./volumes/portainer` and start the stack. Your browser may get a little confused when it restarts. Just navigate to "yourip:9000" (may require more than one attempt) and create your new login details. If it doesn't ask you to connect to the 'Local' docker or shows and empty endpoint just logout and log back in and it will give you the option. From now on it should just work fine.

# Postgres
https://hub.docker.com/_/postgres

I added a SQL server, for those that need an SQL database. The database credentials can be found in the file postgres/postgres.env. It is highly recommended to change the user, password and default database

# Adminer
https://hub.docker.com/_/adminer

This is a nice tool for managing databases. Web interface on port 8080

# Grafana
https://hub.docker.com/r/grafana/grafana

Grafana's default credentials are username "admin" password "admin" it will ask you to choose a new password on boot. Go to yourIP:3000 in you web browser.

# Influxdb
https://hub.docker.com/_/influxdb

The credentials and default database name for influxdb are stored in the file called influxdb/influx.env . The default username and password is set to "nodered" for both it is HIGHLY recommended that you change that, the default db is "measurements".
To access the terminal for influxdb execute `./services/influxdb/terminal.sh`. Here you can set additional parameters or create other databases.

# Mosquitto
https://hub.docker.com/_/eclipse-mosquitto

Extra reference https://www.youtube.com/watch?v=1msiFQT_flo


By default the Mosquitto container has no password. You can leave it that way if you like but its always a good idea to secure your services.

Step 1
To add the password run `./services/mosquitto/terminal.sh`, I put some helper text in the script. Basically you use the `mosquitto_passwd -c /mosquitto/config/passwd MYUSER` command, replacing MYUSER with your username. it will then ask you to type your password and confirm it. exiting with `exit`. 

Step 2
Edit the file called services/mosquitto/mosquitto.conf and remove the comment in front of password_file. Restart the container with `docker-compose restart mosquitto`. Type those credentials into Nodered etc

# Node-RED
https://hub.docker.com/r/nodered/node-red

## GPIO
To communicate to your pi's GPIO you need to use the new `node-red-node-pi-gpiod`. The nice thing is that you can now connect to multiple PIs from the same nodered.

You need to make sure the pigpdiod is running. The recommented method is listed here https://github.com/node-red/node-red-nodes/tree/master/hardware/pigpiod
Basically you run the following command `sudo nano /etc/rc.local` and add the line '/usr/bin/pigpiod' above 'exit 0' and reboot the pi. there is an option to secure the service see the writeup

drop the gpio node and use your pi's IP:8888 (127.0.0.1 wont work)

## Securing Node-RED
To secure Node-RED you need a password hash. There is a terminal script `./services/nodered/terminal.sh` execute it to get into the terminal.
Copy the helper text `node -e ..... PASSWORD`, paste it and change your password to get a hash.

Open the file `./nodered/data/settings.js` and follow the writeup on https://nodered.org/docs/user-guide/runtime/securing-node-red for further instrucitons

# Backups
Because container can easily be rebuilt from dockerhub we only have to backup the data in the "volumes" directory.

## Influxdb
`~/IOTstack/scripts/backup_influxdb.sh` does a database snapshot and stores it in ~/IOTstack/backups/influxdb/db . This can be restored with the help a script (that i still need to write)

## Docker backups
The script `~/IOTstack/docker_backup.sh` performs the master backup for the stack. 

This script can be placed in a cron job to backup on a schedule.
Edit the crontab with`crontab -e`
Then add `0 0 * * * ~/IOTstack/docker_backup.sh >/dev/null 2>&1` to have a backup everynight at midnight

This script cheats by copying the volume folder live. The correct way would be to stop the stack first then copy the volumes and restart. The cheat method shouldn't be a problem unless you have fast changing data like in influxdb. This is why the script makes a database export of influxdb and ignores it's volume. 

### Dropbox integration
To enable the the docker_backups.sh file and uncomment the lines in front of the Dropbox-Uploader command.

## Restoring a backup
The "volumes" directory contains all the persistent data necessary to recreate the container.The docker-compose.yml and the environment files are optional as they can be regenerated with the menu. Simply copy the volumes directory into the IOTstack directory, Rebuild the stack and start. 

# Accessing your Device from the internet
The challenge most of us face with remotely accessing your home network is that don't have a static IP. From time to time the IP that yopur ISP assigns to you changes and its difficult to keep up. Fortunatley there is a solution, a DynamicDNS. The section below shows you how to setup an easy to remember address that follows your public IP no matter when it changes.

Secondly how do you get into your home network. Your router has a firewall that is designed to keep the rest of the internet out of your network to protect you. Here we install a VPN and configure the firewall to only allow very secure VPN traffic in. 

## DuckDNS
If you want to have a DynamicDNS point to your Public IP I added a helper script.
Register with duckdns.org and create a subdomain name. Then edit the `nano ~/IOTstack/duck.sh` file and add your `domain=` and `token=`.

first test the script to make sure it works `sudo ~/IOTstack/duck/duck.sh` then `cat /var/log/duck.log`. If you get KO then something has gone wrong and you should checkout your settings in the script. If you get an OK then you can do the next step. 

Create a cron job by running the follow cmd `crontab -e`

You will be asked to use an editor option 1 for nano should be fine
paste the following in the editor `*/5 * * * * sudo ~/IOTstack/duck/duck.sh >/dev/null 2>&1` then ctrl+s and ctrl+x to save

Your Public IP should be updated every five minutes

## PiVPN
pimylifeup.com has an excellent tutorial on how to install PiVPN https://pimylifeup.com/raspberry-pi-vpn-server/

In point 17 and 18 they mention using noip for their dynamicDNS. Here you can use the DuckDNS address if you created one.

Dont forget you need to open the port 1194 on your firewall. For most people you wont be able to VPN from inside your own network so download OpenVPN client for your mobile phone and try to connect over mobile data.

Once you activate your vpn (from you phone/laptop/work computer) you will effectlivley be on your home network and you can access your devices as if you were on the wifi at home.

Personally I use the VPN any time Im on public wifi, all your traffic is secure.

# Miscellaneous

## log2ram
https://github.com/azlux/log2ram
One of the drawbacks of an sd card is that it has limited lifespan. One way to reduce the load on the sd card is move you log files to RAM. log2ram is a convient tool to simply set this up. It can be installed from the miscellaneous menu.

## Drobox-Uploader
This a great utility to easily upload data from your PI to the cloud. https://magpi.raspberrypi.org/articles/dropbox-raspberry-pi
The MagPi has an excellent explanation of the process of setting up the Dropbox API. Dropbox-Uploader is used in the backup script.

# Add to the project
Feel free to add your comments on features or images that you think should be added. 
