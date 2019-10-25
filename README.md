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

Firstly what is docker. The corrent question is what are containers. Docker is just one of the utilities to run container.

Container can be thought of as ultra minimal virtual machines. You download a base image and create a new container and only the differences between the base and your "VM" are stored.
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

## Docker commands
This menu executes shell scripts in the root of the project. It is not necessary to run them from the menu. Open up the shell script files to see what is inside and what they do

## Miscellaneous commands
Some helpful commands have been added like disabling swap

# Running Docker commands
From this point on make sure you are executing the commands from inside the project folder. Docker-compose commands need to be run from the folder where the docker-compose.yml is located. If you want to move the folder make sure you move the whole project folder.

## Starting and Stopping containers
to start the stack navigate to the project folder containing the docker-compose.yml file

to start the stack run:
`docker-compose up -d` or `./start.sh`

to stop:
`docker-compose down` or `./stop.sh`

The first time you run start the stack docker will download all the images for the web. Depending on how many containers you selected and your internet speed this can take a long while.

The "docker-compose down" command stops the containers then deletes them. The alternative is to run "docker-compose stop" which does not delete the containers.

## Persistent data
Docker allowes you to map folders inside your containers to folders on the disk. This is done with "volume" key. There are two types of volumes. Any modification to the container reflects in the volume.

### Folder based volumes
Docker links a specified folder from your disk into the container. This allows you to easily access and backup your data. Folder permission can be an issue so be sure to use sudo to copy files where necessary.

### Docker volumes
Docker creates is own managed folder in its resource folder. These are a little harder to get to and get your info out of. 

## Updating the images
If a new version of a container it is simple to update it.
use the  `docker-compose down` command to stop the stack

pull the latest version from docker hub with one of the following command

`docker-compose pull` or the script `./update.sh`

## Deleting containers, volumes and images
Should you want to remove the containers, volumes or images from disk two scripts have been provided.

The script `./prune-volumes.sh` delets all stopped container, networks, docker volumes and hanging images. I does not delete the folder based link, these you will have to delete manually.

`./prune-images.sh` will remove all images not assosiated with a container. If you run this while you stack is down you will have to redownload all images from scratch. This command can be helful to reclaim diskspace after updating your images, just make sure to run it while your stack is running as not to delete the images in use

## Deleting folder volumes
If you want to delete the influxdb data folder run the following command `sudo rm -r influxdb/data`. Only the data folder is deleted leaving the env file intact. review the docker-compose.yml file to see where the file volumes are stored.

You can use git to delete all files and folders to return your folder to the freshly cloned state.
`sudo git clean -d -x -f` will return the working tree to its clean state. USE WITH CAUTION!

## Networking

The docker-compose instruction creates a internal network for the containers to communicate in, the ports get exposed to the PI's IP address when you want to connect from outside. It also creates a "DNS" the name being the container name. So it is important to note that when one container talks to another they talk by name. All the containers names are lowercase like nodered,influxdb...

An easy way to find out your ip is by typing `ifconfig` in the terminal and look next to eth0 or wlan0 for your ip. It is hightly recommended that you set a static IP for your PI or at least reserve a IP on your router so that you know it

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

# Portainer
Portainer is a great application for managing Docker. In your web browser navigate to `#yourip:9000`. You will be asked to choose a password. In the next window select 'Local' and connect, it shouldn't ask you this again. From here you can play around, click local, and take a look around. This can help you find unused images/containers. On the Containers section there are 'Quick actions' to view logs and other stats. Note: This can all be done from the CLI but portainer just makes it much much easier. The portainer password is stored in a docker volume, so if you forget it you will need to delete the volume the prune-volumes.sh can be used for that.

# Postgres
I added a SQL server, for those that need an SQL database. The database credentials can be found in the file postgres/postgres.env. It is highly recommended to change the user, password and default database

# Adminer
This is a nice tool for managing databases. Web interface on port 8080

# Grafana
Grafana's default credentials are username "admin" password "admin" it will ask you to choose a new password on boot. Go to yourIP:3000 in you web browser.

# influxdb
The credentials and default database name for influxdb are stored in the file called influxdb/influx.env . The default username and password is set to "nodered" for both it is HIGHLY recommended that you change that, the default db is "measurements".
To access the terminal for influxdb execute `./influxdb/terminal.sh`. Here you can set additional parameters or create other databases.

# Mosquitto (mqtt)
reference https://www.youtube.com/watch?v=1msiFQT_flo
By default the MQTT container has no password. You can leave it that way if you like but its always a good idea to secure your services.

Step 1
To add the password run `./mosquitto/terminal.sh`, i put some helper text in the script. Basically you use the `mosquitto_passwd -c /etc/mosquitto/passwd MYUSER` command, replacing MYUSER with your username. it will then ask you to type your password and confirm it. exiting with `exit`. 

Step 2
edit the file called mosquitto/mosquitto.conf and remove the comment in front of password_file. Stop and Start and you should be good to go. Type those credentials into Nodered etc

# Node-RED
## GPIO
To communicate to your pi's GPIO you need to use the new `node-red-node-pi-gpiod`. The nice thing is that you can now connect to multiple PIs from the same nodered.

You need to make sure the pigpdiod is running. The recommented method is listed here https://github.com/node-red/node-red-nodes/tree/master/hardware/pigpiod
Basically you run the following command `sudo nano /etc/rc.local` and add the line '/usr/bin/pigpiod' above 'exit 0' and reboot the pi. there is an option to secure the service see the writeup

drop the gpio node and use your pi's IP:8888 (127.0.0.1 wont work)

## Securing Node-RED
To secure Node-RED you need a password hash. There is a terminal script `./nodered/terminal.sh` execute it to get into the terminal.
Copy the helper text `node -e ..... PASSWORD`, paste it and change your password to get a hash.

Open the file `./nodered/data/settings.js` and follow the writeup on https://nodered.org/docs/user-guide/runtime/securing-node-red for further instrucitons
 

# DuckDNS
If you want to have a DynamicDNS point to your Public IP I added a helper script.
Register with DuckDNS then edit the `duck.sh` file and add your dns and token to your values.

Either run the `./make_duck.sh` from its folder or copy it to your folder of choice (my script just makes the folder and copies the file there)

first test the script to make sure it works `~/duckdns/duck.sh` then `cat ~duck/duck.log`. If you get an OK then you can do the next step.

Create a cron job by running the follow cmd `crontab -e`

You will be asked to use an editor option 1 for nano should be fine
paste the following in the editor `*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1` then ctrl+o and ctrl+x to save
(if you chose your own folder specify it in stead, just remember to change the curl statement to point to your desired log file logation)
Your Public IP should be updated every five minutes
