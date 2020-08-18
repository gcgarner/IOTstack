# Getting started
## Download the project

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
## The Menu
I've added a menu to make things easier. It is good however to familiarise yourself with how things are installed.
The menu can be used to install docker and then build the docker-compose.yml file necessary for starting the stack and it runs a few common commands. I do recommend you start to learn the docker and docker-compose commands if you plan using docker in the long run. I've added several helper scripts, have a look inside.

Navigate to the project folder and run `./menu.sh`

### Installing from the menu
Select the first option and follow the prompts

### Build the docker-compose file
docker-compose uses the `docker-compose.yml` file to configure all the services. Run through the menu to select the options you want to install.

### Docker commands
This menu executes shell scripts in the root of the project. It is not necessary to run them from the menu. Open up the shell script files to see what is inside and what they do

### Miscellaneous commands
Some helpful commands have been added like disabling swap

## Running Docker commands
From this point on make sure you are executing the commands from inside the project folder. Docker-compose commands need to be run from the folder where the docker-compose.yml is located. If you want to move the folder make sure you move the whole project folder.

### Starting and Stopping containers
to start the stack navigate to the project folder containing the docker-compose.yml file

To start the stack run:
`docker-compose up -d` or `./scripts/start.sh`

To stop:
`docker-compose stop` stops without removing containers

To remove the stack: 
`docker-compose down` stops containers, deletes them and removes the network

The first time you run 'start' the stack docker will download all the images for the web. Depending on how many containers you selected and your internet speed this can take a long while.

### Persistent data
Docker allows you to map folders inside your containers to folders on the disk. This is done with the "volume" key. There are two types of volumes. Any modification to the container reflects in the volume.

#### Sharing files between the Pi and containers
Have a look a the wiki on how to share files between Node-RED and the Pi. [Wiki](https://github.com/gcgarner/IOTstack/wiki/Node-RED#sharing-files-between-node-red-and-the-host)

### Updating the images
If a new version of a container image is available on docker hub it can be updated by a pull command.

Use the `docker-compose stop` command to stop the stack

Pull the latest version from docker hub with one of the following command

`docker-compose pull` or the script `./scripts/update.sh`

Start the new stack based on the updated images

`docker-compose up -d`

### Node-RED error after modifications to setup files
The Node-RED image differs from the rest of the images in this project. It uses the "build" key. It uses a dockerfile for the setup to inject the nodes for pre-installation. If you get an error for Node-RED run `docker-compose build` then `docker-compose up -d`

### Deleting containers, volumes and images

`./prune-images.sh` will remove all images not associated with a container. If you run it while the stack is up it will ignore any in-use images. If you run this while you stack is down it will delete all images and you will have to redownload all images from scratch. This command can be helpful to reclaim disk space after updating your images, just make sure to run it while your stack is running as not to delete the images in use. (your data will still be safe in your volume mapping)

### Deleting folder volumes
If you want to delete the influxdb data folder run the following command `sudo rm -r volumes/influxdb/`. Only the data folder is deleted leaving the env file intact. review the docker-compose.yml file to see where the file volumes are stored.

You can use git to delete all files and folders to return your folder to the freshly cloned state, AS IN YOU WILL LOSE ALL YOUR DATA.
`sudo git clean -d -x -f` will return the working tree to its clean state. USE WITH CAUTION!