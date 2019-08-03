# raspIOTstackd
docker stack for getting started on IOT on the Raspberry PI

This Docker stack consists of:
  * nodered
  * Grafana
  * influxDB
  
# Tested platform
Raspberry Pi 3B running Raspbian (Stretch)
  
# Youtube reference
this repo was inspired by Andreas Spiess's video on using these tools https://www.youtube.com/watch?v=JdV4x925au0 . This is an alternative approach to the setup. Be sure to watch the video for the instructions. Just note that the network addresses are different, see note below

## Download the project

```
git clone https://github.com/gcgarner/raspIOTstackd.git
```

For those not familar with git or not CLI savy, the clone command downloads the repository and creates a folder with the repository name.

To enter the direcory run:
```
cd raspIOTstackd
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

Note: when I installed docker-compose it is not the latest version.
It only supports Version '2' of the compose instructions and therefore some of the more advanced instructions have been omitted

# Running Docker commands
From this point on make sure you are executing the commands from inside the repo folder. If you need to at any point start or stop navigate back to the repo folder first

## Folder permissions
when docker starts the compose for the first time it creates the folders for linking the volumes.
There is an issue with Grafana where a different user and group is used run the `folderfix.sh`

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

docker deletes the containers with the docker-compose down command. However because the compose file specifies volumes the data is stored in persistent folders on the host system. This is good because it allows you to update the image and retain your data

## Updating the images
if a new version of a container it is simple to update it.
use the  `docker-compose down` command to stop the stack

pull the latest version from docker hub with one of the following commands

```
docker pull grafana/grafana:latest
docker pull influxdb:latest
docker pull nodered/node-red-docker:rpi
```

## Networking
The compose instruction creates a internal network for the containers to communicate in.
It also creates a "DNS" the name being the container name.
When you need to specify the address of your influxdb it will not be 127.0.0.1:8086 ! It will be influxdb:8086
Similarly inside the containers the containers talk by name. However if you need to interact with it (from outside) you do if via your pi's ip e.g. 192.168.0.n:3000 (or 1270.0.0.1:3000 if you are using the pi itself)
