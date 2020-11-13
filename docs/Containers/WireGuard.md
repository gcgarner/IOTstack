# WireGuard

WireGuard is a fast, modern, secure VPN tunnel. It can securely connect you to your home network, allowing you to access your home network's local services from anywhere. It can also secure your traffic when using public internet connections. 

WARNING: These instructions require that you have privileges to configure your network's gateway. If you are not able to make changes to your network's firewall settings, then you will not be able to finish this setup. If you are able to make these changes, then proceed to the next steps.

## Setup

There are a few things to configure before starting up the WireGuard container. First, it may be necessary to set up a way to locate your home network from the internet. One way to achieve this, if you haven't done so yet, is to set up a DuckDNS account as described in the [Wiki](https://sensorsiot.github.io/IOTstack/Accessing-your-Device-from-the-internet.md) under the section DuckDNS. This address will be used in the following configuration. After configuring the service, it needs to be made accessible from outside the home network. Lastly, each device will need WireGuard installed and set up with the details of your WireGuard service. 

## WireGuard Configuration 

The [Custom services and overriding default settings for IOTstack](https://sensorsiot.github.io/IOTstack/Custom/) page describes how to use a `compose-override.yml` file to allow `./menu.sh` to automatically incorporate your custom configurations into the final `docker-compose.yml` file that is responsible for defining all service containers. 

You will need to create the `compose-override.yml` before building your stack via `./menu.sh`. If you have already built your stack, you'll have to re-build it after creating `compose-override.yml`.

Here is an example `compose-override.yml` file:
```
services:
  wireguard:
    environment:
      - PUID=1000                                       
      - PGID=1000                                     
      - TZ=America/Los_Angeles                  
      - SERVERURL=<Your-DuckDNS-account>.duckdns.org #optional 
      - SERVERPORT=51820 #optional
      - PEERS=3 #optional                       
      - PEERDNS=auto #optional
      - INTERNAL_SUBNET=100.64.0.0/24 #optional
```

The values you will probably want to change are `TZ` to your own timezone, `SERVERURL` to your own DuckDNS address and `PEERS` to set the number of devices you plan to connect to your VPN. If you also decide to edit the `SERVERPORT` value, you will also need to include a matching value in the `ports:` section as follows:

```
services:
  wireguard:
    environment:
      - PUID=1000                                       
      - PGID=1000                                     
      - TZ=America/Los_Angeles                  
      - SERVERURL=<Your-DuckDNS-account>.duckdns.org #optional 
      - SERVERPORT=55555 #optional
      - PEERS=3 #optional                       
      - PEERDNS=auto #optional
      - INTERNAL_SUBNET=100.64.0.0/24 #optional
    ports:
      - 55555:55555/udp
```

If you customize other containers, just make sure the file only says `services:` once at the beginning of the file. Once you are done, you can run `./menu.sh` to build your stack. Finally, check that your changes were successfully integrated by running:

`$ cat docker-compose.yml`

If everything looks good, you can run the following to start your container: `$ docker-compose up -d`

## Network Configuration

A typical home network will have a firewall configured that effectively blocks all incoming attempts to open a new connection with devices on the network. However, in order to use our VPN from outside of our home network (which is precisely the point of running the service!), we need to configure port fowarding to allow incoming connections to reach our device running IOTstack. This step of the configuration varies based on the specific gateway device for your network. Note that these instructions assume you have privileges to configure your gateway's firewall settings (see warning above). This section will include some tips, but if you are unsure how to do this, the best idea would be to search the web for "[YOUR DEVICE NAME] port forwarding configuration".

NOTE: WireGuard uses UDP, not TCP. So make sure your port forwarding rules are for UDP only. 

First, it's a good idea to check that WireGuard is at least accessible on the local network by using `nmap`:

```
$ sudo nmap -sU -p 51820 ip.of.IOTstack.device
OR from the IOTstack device itself:
$ sudo nmap -sU -p 51820 127.0.0.1

PORT      STATE         SERVICE
51820/udp open|filtered unknown
MAC Address: XX:XX:XX:XX:XX:XX (Unknown)
```
If your result looks similar, then WireGuard is up and running and you simply need to set up port forwarding. Notice again, that WireGuard uses UDP. 

Many routers/gateways are configurable via a web interface, in which case you will only need the ip address of the device, as well as the account and password to access it. You should be able to find  your gateway's address with the following command:

```
$ ip route | grep default

default via 192.168.1.1 dev eth0 proto dhcp metric 100
```
Then copy the ip to a browser window to configure. The login credentials may be physically printed on the device if you have never logged in or changed the default credentials. 

Follow the instructions to configure UDP port forwarding for your network. Make sure that you configure only UDP port forwarding, only pointing specifically at your IOTstack device (by ip or hostname, whichever is more appropriate for your network configuration) and only for port 51820 (or whichever port you have configured for WireGuard). Remember that you are opening this port to the public internet, so be careful not to leave anything open that you're not using or point to the wrong device. Once you are finished, save your changes and test that the port is open from the internet, again using `nmap`:

```
$ sudo nmap -sU -p 51820 <your-duckdns-account>.duckdns.org

PORT      STATE         SERVICE
51820/udp open|filtered unknown
MAC Address: XX:XX:XX:XX:XX:XX (Unknown)
```                                           
If everything looks good, then the last step is to set up your devices to connect to your WireGuard service.

## Device Setup

Lastly, it's time to set up each device to connect to your VPN. You will need to install the WireGuard client on each device. This can be typically be done via each device's app store or package manager. For complete install instructions, see the [WireGuard Installation page](https://www.wireguard.com/install/).

## QR Code Mobile Device Setup
After the client is installed on your devices, each one needs its own WireGuard peer configuration. The easiest devices to set up are mobile devices, which can be done by using the QR codes that are automatically generated for each WireGuard PEER, as defined in the `docker-compose.yml` file. The QR codes are located in the following locations:

```
~/IOTstack/services/wireguard/config/peer1/peer1.png
~/IOTstack/services/wireguard/config/peer2/peer2.png
~/IOTstack/services/wireguard/config/peer3/peer3.png
...
```

To copy the files from a Raspberry Pi onto another Linux machine for example, you can use the following command:

```
$ sudo scp pi@<Rpi-ip-address>:/home/pi/IOTstack/services/wireguard/config/peer1/peer1.png ~/peer1.png
```
(Hint: you can use the `scp -i` flag to specify an IdentityFile or better yet, `scp -F` flag if you have your device configured in `.ssh/config`)

You can repeat this step for each peer's QR code `.png` file and then scan the QR codes in the mobile app on your devices. The devices should now be configured and able to connect to your VPN.

## Setting Up Other Devices

Setting up other devices is a bit more complicated. Refer to the [WireGuard Quick Start](https://www.wireguard.com/quickstart/) page or search for instructions specific to your OS. 
