# Networking
The docker-compose instruction creates an internal network for the containers to communicate in, the ports get exposed to the PI's IP address when you want to connect from outside. It also creates a "DNS" the name being the container name. So it is important to note that when one container talks to another they talk by name. All the containers names are lowercase like nodered, influxdb...

An easy way to find out your IP is by typing `ip address` in the terminal and look next to eth0 or wlan0 for your IP. It is highly recommended that you set a static IP for your PI or at least reserve an IP on your router so that you know it

Check the docker-compose.yml to see which ports have been used

![net](https://user-images.githubusercontent.com/46672225/66702353-0bcc4080-ed07-11e9-994b-62219f50b096.png)

## Examples
- You want to connect your nodered to your mqtt server. In nodered drop an mqtt node, when you need to specify the address type `mosquitto`
- You want to connect to your influxdb from grafana. You are in the Docker network and you need to use the name of the Container. The address you specify in the grafana is `http://influxdb:8086`
- You want to connect to the web interface of grafana from your laptop. Now you are outside the container environment you type PI's IP eg 192.168.n.m:3000

## Ports
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