# IOTstack
docker stack for getting started on IOT on the Raspberry PI

This Docker stack consists of:
  * nodered
  * grafana
  * influxDB
  * postgres
  * mosquitto mqtt
  * portainer
  * adminer
  
The idea here is you delete what you dont need. Only need nodered and mosquitto, open up the docker-compose.yml and delete services you dont need. Running all these services is very taxing on my poor 3B, the more you run its a good idea to get some cooling (and it makes my wifi fall over). Ideally if you want to run these services a PI4 with 2GB RAM is a good option. And if you can run it over a lan cable.
  
# Tested platform
Raspberry Pi 3B running Raspbian (Stretch)
  
# Youtube reference
this repo was inspired by Andreas Spiess's video on using these tools https://www.youtube.com/watch?v=JdV4x925au0 . This is an alternative approach to the setup. Be sure to watch the video for the instructions. Just note that the network addresses are different, see note below

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

## Before you start
Installing docker
```
curl -sSL https://get.docker.com | sh
```

to install docker-compose
```
sudo apt update && sudo apt install -y docker-compose
```

Note: when I installed docker-compose it is not the latest version it did not support version 3.
I decided to leave the yml file on version 2 for backwards compatibility.

# Running Docker commands
From this point on make sure you are executing the commands from inside the repo folder. If you need to at any point start or stop navigate back to the repo folder first

## Folder permissions
The containers are set to store persistent data in folder. Grafana runs with a different userid than the standard pi user. This workaround changes the permission of the folder so that data can be stored locally, run  `sudo ./folderfix.sh`

if the script wont execute then run the following first (this applies to the other scripts as well)

```
sudo chmod +x ./folderfix.sh
sudo ./folderfix.sh
```
you only need to run this once.

## Starting and Stopping containers
to start the stack navigate to the folder containing the docker-compose.yml file

run the following
`docker-compose up -d`

to stop
`docker-compose down`

I've added two scripts for startin and stopping if you forget the commands
`./start.sh` starts the containers
`./stop.sh` stops the containers

side note: Docker deletes the containers with the docker-compose down command. However because the compose file specifies volumes the data is stored in persistent folders on the host system. This is good because it allows you to update the image and retain your data

## Updating the images
If a new version of a container it is simple to update it.
use the  `docker-compose down` command to stop the stack

pull the latest version from docker hub with one of the following commands

```
docker pull grafana/grafana:latest
docker pull influxdb:latest
docker pull nodered/node-red:latest
```

## Current issue with Grafana
As of the date of this publish the team at Grafana are working on an issue in the 6.4.X version for the ARM image. The compose file hard codes to version 6.3.6, when the issue is resolved the ":latest" tag can be used again in stead of ":6.3.6"

## Networking
An easy way to find out your ip is by typing `ifconfig` in the terminal and look next to eth0 or wlan0 for your ip. It is hightly recommended that you set a static IP for your PI or at least reserve a IP on your router so that you know it

The docker-compose instruction creates a internal network for the containers to communicate in, the ports get exposed to the pi's IP address when you want to connect from outside. It also creates a "DNS" the name being the container name. So it is important to note that when one container talks to another they talk by name. I gave all the containers names in allcaps like NODERED,INFLUXDB...

check the docker-compose.yml to see which ports have been used

![net](https://user-images.githubusercontent.com/46672225/66629049-dfc69780-ec00-11e9-998d-c4a5d50a46e4.png)

### Examples
You want to connect your nodered to your mqtt server.
In nodered drop an mqtt node, when you need to specify the address type `MQTT`

You want to connect to your influxdb from grafana. 
You are in the Docker network and you need to use the name of the Container.
The address you specify in the grafana is https://INFLUXDB:8086

You want to connect to the web interface of Grafana from you laptop.
Now you are outside the container environmnet you type PI's IP eg 192.168.n.m:9000


## Portainer
Portainer is a great application for managing Docker. In your web browser navigate to `#yourip:9000`. You will be asked to choose a password. In the next window select 'Local' and connect, it shouldn't ask you this again. From here you can play around, click local, and take a look around. This can help you find unused images/containers. On the Containers section there are 'Quick actions' to view logs and other stats. Note: This can all be done from the CLI but portainer just makes it much much easier

## Postgres
I added a SQL server, for those that need it see password section for login details

## Adminer
This is a nice tool for managing databases. Web interface on port 8080

## Passwords
### Grafana
Grafana's default credentials are username "admin" passord "admin" it will ask you to choose a new password on boot

### influxdb
there is a file called influx.env in the folder influxdb inside it is the username and password. The default I set is "nodered" for both it is HIGHLY recommended that you change that

### Mosquitto (MQTT)
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

## Node-red GPIO
To communicate to your pi's GPIO you need to install `node-red-node-pi-gpiod` from the palette. The nice thing is that you can now connect to multiple pis from the same nodered.

You need to make sure the pigpdiod is running. The recommented method is listed here https://github.com/node-red/node-red-nodes/tree/master/hardware/pigpiod
Basically you run the following command `sudo nano /etc/rc.local` and add the line '/usr/bin/pigpiod' above 'exit 0' and reboot the pi. there is an option to secure the service see the writeup

drop the gpio node and use your pi's IP:8888 (127.0.0.1 wont work)


