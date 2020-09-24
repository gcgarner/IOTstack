# Node-RED
## References
- [Docker](https://hub.docker.com/r/nodered/node-red)
- [website](https://nodered.org/)

## Build warning
The Node-RED build will complain about several issues. This is completely normal behaviour.

## SQLite
Thanks to @fragolinux the SQLite node will install now. **WARNING it will output many error and will look as if it has gotten stuck. Just give it time and it will continue.** 

## GPIO
To communicate to your Pi's GPIO you need to use the `node-red-node-pi-gpiod` node. It allowes you to connect to multiple Pis from the same nodered service.

You need to make sure that pigpdiod is running. The recommended method is listed [here](https://github.com/node-red/node-red-nodes/tree/master/hardware/pigpiod)
You run the following command `sudo nano /etc/rc.local` and add the line `/usr/bin/pigpiod` above `exit 0` and reboot the Pi. There is an option to secure the service see the writeup for further instuctions.

Fot the Rpi Image you will also need to update to the most recent version 

```
sudo apt-get update
sudo apt-get install pigpio python-pigpio python3-pigpio
```

Drop the gpio node and use your Pi's IP. Example: 192.168.1.123 (127.0.0.1 won't work because this is the local address of every computer'.)

## Securing Node-RED
To secure Node-RED you need a password hash. There is a terminal script `./services/nodered/terminal.sh` execute it to get into the terminal.
Copy the helper text `node -e ..... PASSWORD`, paste it and change your password to get a hash.

Open the file `./volumes/nodered/data/settings.js` and follow the writeup on https://nodered.org/docs/user-guide/runtime/securing-node-red for further instructions


## Sharing files between Node-RED and the host
Containers run in a sandboxed environment they can't see the host (the Pi itself) file system. This presents a problem if you want to read a file directly to the host from inside the container. Fortunately there is a method, the containers have been set up with volume mapping. The volume maps a specific directory or file from the host file system into the container. Therefore if you write to that directory both the host and the container can see the files.

Consider the following:

The docker-compose.yml file shows the following for Node-RED
```
    volumes:
      - ./volumes/nodered/data:/data
```
If inside Node-RED you were to write to the `/data` folder then the host would see it in `~/IOTstack/volumes/nodered/data` (the ./volumes above implies relative to the docker-compose.yml file)

![image](https://user-images.githubusercontent.com/46672225/68073532-e2e51b80-fd99-11e9-955e-3f27e1c57998.png)

The flow writes the file `/data/test.txt` and it is visible in the host as `~/IOTstack/volumes/nodered/data/test.txt`

Remember, files and directories in the volume are persistent between restarts. If you save your data elsewhere it will be destroyed should you restart. Creating a subdirectory in volume i.e. `/data/storage/` would be advised

## Using Bluetooth
In order to allow Node-RED to access the Pi's Bluetooth module the docker-comose.yml file needs to be modified to allow it access. `network_mode: "host"` needs to be added (make sure the indentation is correct, us spaces not tabs):

```
  nodered:
    container_name: nodered
    build: ./services/nodered/.
    restart: unless-stopped
    user: "0"
    network_mode: "host"
```
By activating host mode the Node-RED container can no longer access containers by name `http://influxdb:8086` will no longer work. Node-RED thinks it now is the host and therefore access to the following services will look as follows:
* influxdb `http://127.0.0.1:8086`
* GPIO `127.0.0.1` port `8888`
* MQTT `127.0.0.1`

## Unused node in Protainer

Portainer will report that the nodered image is unsed, this is normal due to the method used build the image. This is normal behavior. It is not advised to remove it as it is used as the base for the iotstack_nodered image, you will need to redownload it should you rebuild the nodered image.

<img width="1444" alt="UnusedImage" src="https://user-images.githubusercontent.com/34226495/69213978-cd555b80-0bb9-11ea-8734-1c42ff52bf7d.png">

## Running the exec node against the host Pi

Due to the isolation between containers and the host the exec node will run against the container.

There is a solution to work around this. You can use ssh to execute a script on the pi. It requires a little setup but is possible.

For this example I'll be running a simple script called test.sh
I create a file called test.sh in my IOTstack directory with nano

The contents are as follows:
```bash
#!/bin/bash
echo "hello"
exit 0
```

The exit 0 will stop the exec node from reporting an issue.

Its a good idea to add the shebang at the top. make it executable with `chmod +x test.sh`

This nodered running open the nodered terminal with `./services/nodered/terminal.sh` or `docker exec -it nodered /bin/bash` or use portainer

create the ssh folder in the data directory (the /data directory is persistently mapped volume)

`mkdir -p /data/ssh`

create key, this will require naming the output file

`ssh-keygen -f /data/ssh/nodered` put in any additional config you want key type strength
copy the key to the Pi. When asked for a password leave it blank

copy the ssh-key to your pi

`ssh-copy-id -i /data/ssh/nodered pi@192.168.x.x` replace with your static IP address. You will have to reply yes to the prompt. You may also see an error referring to regular expressions however you can ignore it.

now to execute a script on the pi run `ssh -i /data/ssh/nodered pi@192.168.x.x /home/pi/IOTstack/test.sh`

type exit to leave the terminal

(you could also restart your pi with `ssh -i /data/ssh/nodered pi@192.168.x.x sudo reboot`)

in node red in your exec node you can run the command `ssh -i /data/ssh/nodered pi@192.168.x.x /home/pi/IOTstack/test.sh` other the script or command of your choice

![image](https://user-images.githubusercontent.com/46672225/70431264-55c27000-1a85-11ea-8706-b087dc39479d.png)

