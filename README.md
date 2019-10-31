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

In addition, there is a write-up and some scripts to get a dynamic DNS via duckdns and VPN up and running.

Firstly what is docker? The correct question is "what are containers?". Docker is just one of the utilities to run container.

Container can be thought of as ultra-minimal virtual machines, they are a collection of binaries that run in a sandbox environment. You download a preconfigured base image and create a new container and only the differences between the base and your "VM" are stored.
Containers don't have [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)s so generally the way you interact with them is via web services or you can launch into a terminal.
One of the major advantages is that the image comes mostly preconfigured.  

There are pro's and cons for using native installs vs containers. For me, one of the best parts of containers is that it doesn't "clutter" your device, and if you don't need Postgres anymore then just stop the container and delete it and it's like it was never there.

It's not advised to try to run the native version of an app and the docker version, the container will fail. It would be best to install this on a fresh system.

For those looking for a script that installs native applications check out Peter Scargill's [script](https://tech.scargill.net/the-script/)
  
# Tested platform
Raspberry Pi 3B and 4B Raspbian (Buster)

# Feature Requests
Please direct all feature requests to [Discord](https://discord.gg/W45tD83)
  
# Youtube reference
This repo was originally inspired by Andreas Spiess's video on using some of these tools. Some containers have been added to extend its functionality.

[YouTube video](https://www.youtube.com/watch?v=JdV4x925au0): This is an alternative approach to the setup. Be sure to watch the video for the instructions. Just note that the network addresses are different, see note below

# Download the project

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

## Updating the images
If a new version of a container image is available on docker hub it can be updated by a pull command.

Use the `docker-compose down` command to stop the stack

Pull the latest version from docker hub with one of the following command

`docker-compose pull` or the script `./scritps/update.sh`

## Node-RED error after modifications to setup files
The Node-RED image differs from the rest of the images in this project. It uses the "build" key. It uses a dockerfile for the setup to inject the nodes for preinstallation. If you get an error for Node-RED run `docker-compose build` then `docker-compose up -d`

## Deleting containers, volumes and images

`./prune-images.sh` will remove all images not associated with a container. If you run it while the stack is up it will ignore any in-use images. If you run this while you stack is down it will delete all images and you will have to redownload all images from scratch. This command can be helpful to reclaim disk space after updating your images, just make sure to run it while your stack is running as not to delete the images in use. (your data will still be safe in your volume mapping)

## Deleting folder volumes
If you want to delete the influxdb data folder run the following command `sudo rm -r volumes/influxdb/`. Only the data folder is deleted leaving the env file intact. review the docker-compose.yml file to see where the file volumes are stored.

You can use git to delete all files and folders to return your folder to the freshly cloned state, AS IN YOU WILL LOSE ALL YOUR DATA.
`sudo git clean -d -x -f` will return the working tree to its clean state. USE WITH CAUTION!

## Networking

The docker-compose instruction creates an internal network for the containers to communicate in, the ports get exposed to the PI's IP address when you want to connect from outside. It also creates a "DNS" the name being the container name. So it is important to note that when one container talks to another they talk by name. All the containers names are lowercase like nodered, influxdb...

An easy way to find out your IP is by typing `ip address` in the terminal and look next to eth0 or wlan0 for your IP. It is highly recommended that you set a static IP for your PI or at least reserve an IP on your router so that you know it

Check the docker-compose.yml to see which ports have been used

![net](https://user-images.githubusercontent.com/46672225/66702353-0bcc4080-ed07-11e9-994b-62219f50b096.png)

### Examples
You want to connect your nodered to your mqtt server.
In nodered drop an mqtt node, when you need to specify the address type `mosquitto`

You want to connect to your influxdb from grafana. 
You are in the Docker network and you need to use the name of the Container.
The address you specify in the grafana is http://influxdb:8086

You want to connect to the web interface of grafana from your laptop.
Now you are outside the container environment you type PI's IP eg 192.168.n.m:3000

## How the script works
The build script creates the ./services directory and populates it from the template file in .templates . The script then appends the text withing each service.yml file to the docker-compose.yml . When the stack is rebuild the menu doesn not overwrite the service folder if it already exists. Make sure to sync any alterations you have made to the docker-compose.yml file with the respective service.yml so that on your next build your changes pull through.

The .gitignore file is setup such that if you do a `git pull origin master` it does not overwrite the files you have already created. Because the build script does not overwite your service directory any changes in the .templates directory will have no affect on the services you have already made. You will need to move your service folder out to get the latest version of the template.

# Ports
Many containers try to use popular ports such as 80,443,8080. For example openHAB and Adminer both want to use port 8080 for their web interface. Adminer's port has been moved 9080 to accommodate this. Please check the description of the container in the README to see if there are any changes as they may not be the same as the port you are used to.

Port mapping is done in the docker-compose.yml file. Each service should have a section that reads like this:
```
    ports:
      - HOST_PORT:CONTAINER_PORT
```
For adminer:
```
    ports:
      - 9080:8080
```
Port 9080 on Host Pi is mapped to port 8080 of the container. Therefore 127.0.0.1:8080 will take you to openHAB, where 127.0.0.1:9080 will take you to adminer

# Portainer
https://hub.docker.com/r/portainer/portainer/

Portainer is a great application for managing Docker. In your web browser navigate to `#yourip:9000`. You will be asked to choose a password. In the next window select 'Local' and connect, it shouldn't ask you this again. From here you can play around, click local, and take a look around. This can help you find unused images/containers. On the Containers section, there are 'Quick actions' to view logs and other stats. Note: This can all be done from the CLI but portainer just makes it much much easier. 

If you have forgotten the password you created for the container, stop the stack remove portainers volume with `sudo rm -r ./volumes/portainer` and start the stack. Your browser may get a little confused when it restarts. Just navigate to "yourip:9000" (may require more than one attempt) and create your new login details. If it doesn't ask you to connect to the 'Local' docker or shows an empty endpoint just logout and log back in and it will give you the option. From now on it should just work fine.

# Postgres
https://hub.docker.com/_/postgres

I added a SQL server, for those that need an SQL database. The database credentials can be found in the file postgres/postgres.env. It is highly recommended to change the user, password and default database

# Adminer
https://hub.docker.com/_/adminer

This is a nice tool for managing databases. Web interface has moved to port 9080. There was an issue where openHAB and Adminer were using the same ports. If you have an port conflict edit the docker-compose.yml and under the adminer service change the line to read:
```
    ports:
      - 9080:8080
```

# Grafana
https://hub.docker.com/r/grafana/grafana

Grafana's default credentials are username "admin" password "admin" it will ask you to choose a new password on boot. Go to yourIP:3000 in your web browser.

# Influxdb
https://hub.docker.com/_/influxdb

The credentials and default database name for influxdb are stored in the file called influxdb/influx.env . The default username and password is set to "nodered" for both it is HIGHLY recommended that you change them. The environment file contains several commented out options allowing you to set several access options such as default admin user credentials as well as the default database name. Any change to the environment file will require a restart of the service.

To access the terminal for influxdb execute `./services/influxdb/terminal.sh`. Here you can set additional parameters or create other databases.

# Mosquitto
https://hub.docker.com/_/eclipse-mosquitto

Extra reference https://www.youtube.com/watch?v=1msiFQT_flo


By default, the Mosquitto container has no password. You can leave it that way if you like but its always a good idea to secure your services.

Step 1
To add the password run `./services/mosquitto/terminal.sh`, I put some helper text in the script. Basically, you use the `mosquitto_passwd -c /mosquitto/config/passwd MYUSER` command, replacing MYUSER with your username. it will then ask you to type your password and confirm it. exiting with `exit`. 

Step 2
Edit the file called services/mosquitto/mosquitto.conf and remove the comment in front of password_file. Restart the container with `docker-compose restart mosquitto`. Type those credentials into Node-red etc.

# Node-RED
https://hub.docker.com/r/nodered/node-red

## Build warning
The Node-RED build will complain about several issues. This is completely normal behaviour.

## SQLite
Thanks to @fragolinux the SQLite node will install now. WARNING it will output many error and will look as if it has gotten stuck. Just give it time and it will continue.  

## GPIO
To communicate to your Pi's GPIO you need to use the `node-red-node-pi-gpiod` node. It allowes you to connect to multiple Pis from the same nodered service.

You need to make sure that pigpdiod is running. The recommended method is listed [here](https://github.com/node-red/node-red-nodes/tree/master/hardware/pigpiod)
You run the following command `sudo nano /etc/rc.local` and add the line `/usr/bin/pigpiod` above `exit 0` and reboot the Pi. There is an option to secure the service see the writeup for further instuctions.

Drop the gpio node and use your Pi's IP. Example: 192.168.1.123 (127.0.0.1 won't work because this is the local address of every computer'.)

## Securing Node-RED
To secure Node-RED you need a password hash. There is a terminal script `./services/nodered/terminal.sh` execute it to get into the terminal.
Copy the helper text `node -e ..... PASSWORD`, paste it and change your password to get a hash.

Open the file `./nodered/data/settings.js` and follow the writeup on https://nodered.org/docs/user-guide/runtime/securing-node-red for further instructions

# openHAB
https://hub.docker.com/r/openhab/openhab/

openHAB has been added without Amazon Dashbutton binding. Port binding is `8080` for http and `8443` for https. 

# Home-Assistant
https://hub.docker.com/r/homeassistant/home-assistant/

Extra reference: http://hass.io

Home Assistant is a home automation platform running on Python 3. It is able to track and control all devices at home and offer a platform for automating control. Port binding is `8123`.
Home Assistant is exposed to your hosts' network in order to discover devices on your LAN. That means that it does not sit inside docker's network.

# Backups
Because containers can easily be rebuilt from docker hub we only have to back up the data in the "volumes" directory.

## Influxdb
`~/IOTstack/scripts/backup_influxdb.sh` does a database snapshot and stores it in ~/IOTstack/backups/influxdb/db . This can be restored with the help a script (that I still need to write)

## Docker backups
The script `~/IOTstack/scripts/docker_backup.sh` performs the master backup for the stack. 

This script can be placed in a cron job to backup on a schedule.
Edit the crontab with`crontab -e`
Then add `0 23 * * * ~/IOTstack/scripts/docker_backup.sh >/dev/null 2>&1` to have a backup everynight at 23:00.

This script cheats by copying the volume folder live. The correct way would be to stop the stack first then copy the volumes and restart. The cheating method shouldn't be a problem unless you have fast changing data like in influxdb. This is why the script makes a database export of influxdb and ignores its volume. 

### Dropbox integration
To enable the the 'docker_backups.sh' file and uncomment the lines in front of the Dropbox-Uploader command.

## Restoring a backup
The "volumes" directory contains all the persistent data necessary to recreate the container. The docker-compose.yml and the environment files are optional as they can be regenerated with the menu. Simply copy the volumes directory into the IOTstack directory, Rebuild the stack and start. 

# Accessing your Device from the internet
The challenge most of us face with remotely accessing your home network is that you don't have a static IP. From time to time the IP that your ISP assigns to you changes and it's difficult to keep up. Fortunately, there is a solution, a DynamicDNS. The section below shows you how to set up an easy to remember address that follows your public IP no matter when it changes.

Secondly, how do you get into your home network? Your router has a firewall that is designed to keep the rest of the internet out of your network to protect you. Here we install a VPN and configure the firewall to only allow very secure VPN traffic in. 

## DuckDNS
If you want to have a dynamic DNS point to your Public IP I added a helper script.
Register with duckdns.org and create a subdomain name. Then edit the `nano ~/IOTstack/duck/duck.sh` file and add your `domain=` and `token=`.

first test the script to make sure it works `sudo ~/IOTstack/duck/duck.sh` then `cat /var/log/duck.log`. If you get KO then something has gone wrong and you should check out your settings in the script. If you get an OK then you can do the next step. 

Create a cron job by running the following command `crontab -e`

You will be asked to use an editor option 1 for nano should be fine
paste the following in the editor `*/5 * * * * sudo ~/IOTstack/duck/duck.sh >/dev/null 2>&1` then ctrl+s and ctrl+x to save

Your Public IP should be updated every five minutes

## PiVPN
pimylifeup.com has an excellent tutorial on how to install [PiVPN](https://pimylifeup.com/raspberry-pi-vpn-server/)

In point 17 and 18 they mention using noip for their dynamic DNS. Here you can use the DuckDNS address if you created one.

Don't forget you need to open the port 1194 on your firewall. Most people won't be able to VPN from inside their network so download OpenVPN client for your mobile phone and try to connect over mobile data. ([More info.](https://en.wikipedia.org/wiki/Hairpinning))

Once you activate your VPN (from your phone/laptop/work computer) you will effectively be on your home network and you can access your devices as if you were on the wifi at home.

I personally use the VPN any time I'm on public wifi, all your traffic is secure.

# Miscellaneous

## log2ram
https://github.com/azlux/log2ram
One of the drawbacks of an sd card is that it has a limited lifespan. One way to reduce the load on the sd card is to move your log files to RAM. log2ram is a convenient tool to simply set this up. It can be installed from the miscellaneous menu.

## Dropbox-Uploader
This a great utility to easily upload data from your PI to the cloud. https://magpi.raspberrypi.org/articles/dropbox-raspberry-pi
The MagPi has an excellent explanation of the process of setting up the Dropbox API. Dropbox-Uploader is used in the backup script.

# Add to the project
Feel free to add your comments on features or images that you think should be added.
