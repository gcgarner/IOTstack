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

Firstly what is docker. The corrent question is what are containers. Docker is just one of the utilities to run container.

Container can be thought of as ultra minimal virtual machines. You download a base image and create a new container and only the differences between the base and your "VM" are stored.
Containers dont have GUIs so generally the way you interact with them are via web services or you can launch into a terminal.
One of the major advantages is that the image comes mostly preconfigured.  
  
# Tested platform
Raspberry Pi 3B running Raspbian (Buster)
  
# Youtube reference
This repo was originally inspired by Andreas Spiess's video on using some of these tools. Some containers have been added to extend its functionality

https://www.youtube.com/watch?v=JdV4x925au0 
This is an alternative approach to the setup. Be sure to watch the video for the instructions. Just note that the network addresses are different, see note below

For those looking for a script that installs native applications check out Peter Scargill's script
https://tech.scargill.net/the-script/

## Download the project

```
git clone https://github.com/gcgarner/IOTstack.git
```

For those not familar with git or not CLI savy, the clone command downloads the repository and creates a folder with the repository name.

To enter the direcory run:
```
cd IOTstack
```
Personally I like to create a specific folder in my home directory for git repos so they are grouped together in `~/git`

# The Menu
I've added a menu to make things easier. It is good however to familiarise yourself with how things are installed.
The menu can be used to install docker and then build the docker-compose.yml file necessary for starting the stack and it runs a few common commands. I do recommend you start to learn the docker and docker-compose commands if you plan using docker in the long run. I've added several helper scripts, have a look inside.

Navigate to the project folder and run `./menu.sh`

## Installing from the menu
Select the first option and follow the prompts

## Build the docker-compose file
docker-compose uses the `docker-compose.yml` file to configure all the services. Run through the menu to select the options you want to install.

### Node-RED
There is an additional menu for Node-RED to pre-install some commonly used nodes. Warning the output spits out a lot of warning message. They can be ignored.

# Running Docker commands
From this point on make sure you are executing the commands from inside the project folder. Docker-compose commands need to be run from the folder where the docker-compose.yml is. If you want to move the folder make sure you move the whole project folder.

## Starting and Stopping containers
to start the stack navigate to the project folder containing the docker-compose.yml file

run the following
`docker-compose up -d`

to stop
`docker-compose down`

I've added two scripts for startin and stopping if you forget the commands
`./start.sh` starts the containers
`./stop.sh` stops the containers

The first time you run start the stack docker will download all the images for the web. Depending on how many containers you selected and your internet speed this can take a long while.

side note: Docker deletes the containers with the docker-compose down command. However because the compose file specifies volumes the data is stored in persistent folders on the host system. This is good because it allows you to update the image and retain your data

## Updating the images
If a new version of a container it is simple to update it.
use the  `docker-compose down` command to stop the stack

pull the latest version from docker hub with one of the following command

```
docker-compose pull
```


## Current issue with Grafana
As of the date of this publish the team at Grafana are working on an issue in the 6.4.X version for the ARM image. The compose file hard codes to version 6.3.6, when the issue is resolved the ":latest" tag can be used again in stead of ":6.3.6"

## Networking
An easy way to find out your ip is by typing `ifconfig` in the terminal and look next to eth0 or wlan0 for your ip. It is hightly recommended that you set a static IP for your PI or at least reserve a IP on your router so that you know it

The docker-compose instruction creates a internal network for the containers to communicate in, the ports get exposed to the PI's IP address when you want to connect from outside. It also creates a "DNS" the name being the container name. So it is important to note that when one container talks to another they talk by name. All the containers names are lowercase like nodered,influxdb...

check the docker-compose.yml to see which ports have been used

![net](https://user-images.githubusercontent.com/46672225/66702353-0bcc4080-ed07-11e9-994b-62219f50b096.png)

### Examples
You want to connect your nodered to your mqtt server.
In nodered drop an mqtt node, when you need to specify the address type `mqtt`

You want to connect to your influxdb from grafana. 
You are in the Docker network and you need to use the name of the Container.
The address you specify in the grafana is https://influx:8086

You want to connect to the web interface of grafana from you laptop.
Now you are outside the container environmnet you type PI's IP eg 192.168.n.m:3000


## Portainer
Portainer is a great application for managing Docker. In your web browser navigate to `#yourip:9000`. You will be asked to choose a password. In the next window select 'Local' and connect, it shouldn't ask you this again. From here you can play around, click local, and take a look around. This can help you find unused images/containers. On the Containers section there are 'Quick actions' to view logs and other stats. Note: This can all be done from the CLI but portainer just makes it much much easier

## Postgres
I added a SQL server, for those that need it see password section for login details

## Adminer
This is a nice tool for managing databases. Web interface on port 8080

## Passwords
### Grafana
Grafana's default credentials are username "admin" password "admin" it will ask you to choose a new password on boot

### influxdb
there is a file called influx.env in the folder influxdb inside it is the username and password. The default I set is "nodered" for both it is HIGHLY recommended that you change that

### Mosquitto (mqtt)
reference https://www.youtube.com/watch?v=1msiFQT_flo
By default the MQTT container has no password. You can leave it that way if you like but its always a good idea to secure your services.

Step 1
To add the password run `./terminal_mosquitto.sh`, i put some helper text in the script. Basically you use the `mosquitto_passwd -c /etc/mosquitto/passwd MYUSER` command, replacing MYUSER with your username. it will then ask you to type your password and confirm it. exiting with `exit`. 

Step 2
edit the file called mosquitto/mosquitto.conf and remove the comment in front of password_file. Stop and Start and you should be good to go. Type those credentials into Nodered etc

## Influxdb
I've added a script to access the influxdb shell `./terminal_influxdb.sh` from here you can and you database etc

## Postgres
in the file postgres/postgres.env. change the user, password and default database

## Node-red
### GPIO
To communicate to your pi's GPIO you need to use the new `node-red-node-pi-gpiod`. The nice thing is that you can now connect to multiple PIs from the same nodered.

You need to make sure the pigpdiod is running. The recommented method is listed here https://github.com/node-red/node-red-nodes/tree/master/hardware/pigpiod
Basically you run the following command `sudo nano /etc/rc.local` and add the line '/usr/bin/pigpiod' above 'exit 0' and reboot the pi. there is an option to secure the service see the writeup

drop the gpio node and use your pi's IP:8888 (127.0.0.1 wont work)

### Securing Node-RED
To secure Node-RED you need a password hash. There is a terminal script `./terminal_nodered.sh` execute it to get into the termina.
Copy the helper text `node -e ..... PASSWORD`, paste it and change your password to get a hash.

Open the file `./nodered/data/settings.js` and follow the writeup on https://nodered.org/docs/user-guide/runtime/securing-node-red for further instrucitons
 

## DuckDNS
If you want to have a DynamicDNS point to your Public IP I added a helper script.
Register with DuckDNS then edit the `duck.sh` file and add your dns and token to your values.

Either run the `./make_duck.sh` from its folder or copy it to your folder of choice (my script just makes the folder and copies the file there)

first test the script to make sure it works `~/duckdns/duck.sh` then `cat ~duck/duck.log`. If you get an OK then you can do the next step.

Create a cron job by running the follow cmd `crontab -e`

You will be asked to use an editor option 1 for nano should be fine
paste the following in the editor `*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1` then ctrl+o and ctrl+x to save
(if you chose your own folder specify it in stead, just remember to change the curl statement to point to your desired log file logation)
Your Public IP should be updated every five minutes


