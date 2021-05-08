# Home assistant

## References
- [Docker](https://hub.docker.com/r/homeassistant/home-assistant/)
- [Webpage](https://www.home-assistant.io/)

Hass.io is a home automation platform running on Python 3. It is able to track and control all devices at home and offer a platform for automating control. Port binding is `8123`.
Hass.io is exposed to your hosts' network in order to discover devices on your LAN. That means that it does not sit inside Docker's network.

## To avoid confusion

There are two versions of Home Assistant:

* Hass.io, and
* Home Assistant Docker.

Hass.io uses its own orchestration with 3 docker images:

* `hassio_supervisor`,
* `hassio_dns` and
* `homeassistant`.

Home Assistant Docker runs inside a single Docker image, and doesn't support all the features that Hass.io does (such as add-ons). IOTstack allows installing either, but we can only offer limited configuration of Hass.io since it is its own platform.

> [More info on versions](https://www.home-assistant.io/docs/installation/#recommended).

## Menu installation

Hass.io installation can be found inside the `Native Installs` menu on the main menu. Home Assistant can be found in the `Build Stack` menu.

You will be asked to select your device type during the installation. Hass.io is no longer dependant on the IOTstack, it has its own service for maintaining its uptime.

## Installation

Hass.io creates a conundrum:

* If you are definitely going to install Hass.io then you **must** install its dependencies **before** you install Docker.
* One of Hass.io's dependencies is [Network Manager](https://wiki.archlinux.org/index.php/NetworkManager). Network Manager makes **serious** changes to your operating system, with side-effects you may not expect such as giving your Raspberry Pi's WiFi interface a random MAC address both during the installation and, then, each time you reboot. You are in for a world of pain if you install Network Manager without first understanding what is going to happen and planning accordingly.
* If you don't install Hass.io's dependencies before you install Docker, you will either have to uninstall Docker or rebuild your system. This is because both Docker and Network Manager adjust your Raspberry Pi's networking. Docker is happy to install after Network Manager, but the reverse is not true.

### If Docker is already installed, uninstall it

```
$ sudo apt -y purge docker-ce docker-ce-cli containerd.io
$ sudo apt -y remove docker-compose
$ sudo pip3 uninstall docker-compose
```

Note that this does **not** interfere with your existing `~/IOTstack` folder.

### Ensure your system is fully up-to-date

```
$ sudo apt update
$ sudo apt upgrade -y
```

### Install Hass.io dependencies (stage 1)

```bash
$ sudo apt install -y apparmor apparmor-profiles apparmor-utils
$ sudo apt install -y software-properties-common apt-transport-https ca-certificates dbus
```

The first line is required. A post at [community.home-assistant.io](ttps://community.home-assistant.io/t/installing-home-assistant-supervised-on-raspberry-pi-os/201836) implies the second line may also be required but it is not clear whether those packages are strictly necessary.

### Connect to your Raspberry Pi via Ethernet

You can skip this step if you interact with your Raspberry Pi via a screen connected to its HDMI port, along with a keyboard and mouse.

If, however, you are running "headless" (SSH or VNC), connect your Raspberry Pi to Ethernet.

When the Ethernet interface initialises, work out its IP address:

```bash
$ ifconfig eth0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.132.9  netmask 255.255.255.0  broadcast 192.168.132.255
        ether ab:cd:ef:12:34:56  txqueuelen 1000  (Ethernet)
        RX packets 4166292  bytes 3545370373 (3.3 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2086814  bytes 2024386593 (1.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```   

In the above, the IP address assigned to the Ethernet interface is 192.168.132.9.

Drop out of your existing session (SSH or VNC) and re-connect to your Raspberry Pi using the IP address assigned to its Ethernet interface:

```bash
$ ssh pi@192.168.132.9
```

or:

```
vnc://pi@192.168.132.9
```

The reason for stipulating the IP address, rather than a name like `raspberrypi.local` is so that you are *definitely* connected to the Ethernet interface.

If you ignore the advice about connecting via Ethernet and install Network Manager while your session is connected via WiFi, your connection will freeze part way through the installation (when Network Manager starts running and unconditionally changes your Raspberry Pi's WiFi MAC address).

> If you want to know more about why the connection freezes, see [why random MACs are such a hassle ](#aboutRandomMACs).

You *may* be able to re-connect after the WiFi interface acquires a new IP address and advertises that via multicast DNS associated with the name of your device (eg `raspberrypi.local`), but you may also find that the only way to regain control is to power-cycle your Raspberry Pi.

The advice about using Ethernet is well-intentioned. You should heed this advice even if means you need to temporarily relocate your Raspberry Pi just so you can attach it via Ethernet for the next few steps. You can go back to WiFi later, once everything is set up. You have been warned!

### Install Hass.io dependencies (stage 2)

Install Network Manager:

```bash
$ sudo apt install -y network-manager
```

### Consider disabling random MAC address allocation

According to [@steveatk on Discord](https://discordapp.com/channels/638610460567928832/638610461109256194/758825690715652116), you can stop Network Manager from allocating random MAC addresses to your WiFi interface by editing:

```bash
$ sudo vi /etc/NetworkManager/NetworkManager.conf
```

and adding:

```bash
[device]
wifi.scan-rand-mac-address=no
```

This needs to be done **twice**:

* after Network Manager is installed; and again
* after Hass.io is installed via the IOTstack menu.

In both cases, `NetworkManager.conf` is replaced with a version that enables random MAC allocation.

### Re-install docker

If you had to uninstall Docker in the earlier step, now is the time to re-install it. You can use the menu or one of the scripts provided with IOTstack but it is probably just as easy to run:

```bash
$ curl -fsSL https://get.docker.com | sh
$ sudo usermod -G docker -a $USER
$ sudo usermod -G bluetooth -a $USER
$ sudo apt install -y python3-pip python3-dev
$ sudo pip3 install -U docker-compose
$ sudo pip3 install -U ruamel.yaml==0.16.12 blessed
$ sudo reboot
```

Note that this does **not** interfere with your existing `~/IOTstack` folder.

### Run the Hass.io installation

Start at:

```
$ cd ~/IOTstack
$ ./menu.sh
```

and then navigate to the installation option.

The installation of Hass.io takes up to 20 minutes (depending on your internet connection). Refrain from restarting your machine until it has come online and you are able to create a user account.

## Removal

To remove Hass.io you first need to stop the service that controls it. Run the following in the terminal: 

```bash
$ sudo systemctl stop hassio-supervisor.service
$ sudo systemctl disable hassio-supervisor.service
```

This should stop the main service however there are two additional container that still need to be address

This will stop the service and disable it from starting on the next boot.

Next you need to stop the `hassio_dns` and `hassio_supervisor`:

```bash
$ docker stop hassio_supervisor
$ docker stop hassio_dns
$ docker stop homeassistant
```

If you want to remove the containers:

```bash
$ docker rm hassio_supervisor
$ docker rm hassio_dns
$ docker stop homeassistant
```

After rebooting you should be able to reinstall.

The stored files are located in `/usr/share/hassio` which can be removed if you need to.

Double-check with `docker ps` to see if there are other hassio containers running. They can stopped and removed in the same fashion for the dns and supervisor.

You can use Portainer to view what is running and clean up the unused images.

## <a name="aboutRandomMACs"> Why random MACs are such a hassle </a>

> This material was originally posted as part of [Issue 312](https://github.com/SensorsIot/IOTstack/issues/312). It was moved here following a suggestion by [lole-elol](https://github.com/lole-elol).

When you connect to a Raspberry Pi via SSH, that's a protocol that is riding on top of TCP/IP. SSH (the layer 4 protocol) uses TCP (a connection-oriented protocol) which rides on IP (the layer 3 protocol). So far, so good.

But you also need to know what happens at layers 2 and 1. When your SSH client (eg Mac or PC or another Unix box) opens its SSH connection, at layer 3 the IP stack applies the subnet mask against the IP addresses of both the source device (your Mac, PC, etc) and destination device (Raspberry Pi) to split them into "network portion" (on the left) and "host portion" on the right. It then compares the two network portions and, if they are the same, it says "local network".

> To complete the picture, if they do not compare the same, then IP substitutes the so-called "default gateway" address (ie your router) and repeats the mask-and-compare process which, unless something is seriously mis-configured, will result in those comparing the same and being "local network". This is why data-comms gurus sometimes say, "all networking is local".

What happens next depends on the data communications media but we'll assume Ethernet and WiFi seeing as they are pretty much interchangeable for our purposes.

The source machine (Mac, PC, etc) issues an ARP (address resolution protocol). It is a broadcast frame (we talk about "frames" rather than "packets" at Layer 2) asking the question, "who has this destination IP address?" The Raspberry Pi responds with a unicast packet saying, "that's me" and part of that includes the MAC (media access control) address of the Raspberry Pi. The source machine only does this **once** (and this is a key point). It assumes the relationship between IP address and MAC address will not change and it adds the relationship to its "ARP cache". You can see the cache on any Unix computer with:

```
$ arp -a
```

The Raspberry Pi makes the same assumption: it has learned both the IP and MAC address of the source machine (Mac, PC, etc) from the ARP request and has added that to its own ARP cache.

In addition, every layer two switch (got one of those in your home?) has been snooping on this traffic and has learned, for each of its ports, which MAC address(es) are on those ports.

Not "MAC **and** IP". A switch works at Layer 2. All it sees are frames. It only caches MAC addresses!

When the switch saw the ARP broadcast, it replicated that out of all of its ports but when the "that's me" came back from the Raspberry Pi as a unicast response, it only went out on the switch port where the source machine (Mac, PC, etc) was attached.

After that, it's all caching. The Mac or PC has a packet to send to the Pi. It finds the hit in its ARP cache, wraps the packet in a frame and sends it out its Ethernet or WiFi interface. Any switches receive the frame, consult their own tables, and send the frame out the port on the next hop to the destination device. It doesn't matter whether you have one switch or several in a cascade, they have all learned the "next hop" to each destination MAC address they have seen. 

Ditto when the Pi sends back any reply packets. ARP. Switch. Mac/PC. All cached.

The same basic principles apply, irrespective of whether the "switching function" is wired (Ethernet) or WiFi, so it doesn't really matter if your home arrangement is as straightforward as Mac or PC and Pi, both WiFi, via a local WiFi "hub" which is either standalone or part of your router. If something is capable of learning where a MAC is, it does.

Still so far so good.

Now comes the problem. You have established an SSH session connected to the Pi over its WiFi interface. You install Network Manager. As part of its setup, Network Manager discards the **fixed** MAC address which is burned into the Pi's WiFi interface and substitutes a randomly generated MAC address. It doesn't ask for permission to do that. It doesn't warn you it's about to do it. It just does it.

When the WiFi interface comes up, it almost certainly "speaks" straight away via DHCP to ask for an IP address. The DHCP server looks in its own table of MAC-to-IP associations (fixed or dynamic, doesn't matter) and says "never seen **that** MAC before - here's a brand new IP address lease".

The DHCP request is broadcast so all the switches will have learned the new MAC but they'll also still have the old MAC (until it times out). The Mac/PC will receive the DHCP broadcast but, unless it's the DHCP server, will discard it. Either way, it has no means of knowing that this new random MAC belongs to the Pi so it can't do anything sensible with the information.

Meanwhile, SSH is trying to keep the session alive. It still thinks "old IP address" and its ARP cache still thinks old IP belongs to old MAC. Switches know where the frames are meant to go but even if a frame does get somewhere near the Pi, the Pi's NIC (network interface card) ignores it because it's the wrong destination MAC. The upshot is that SSH looks like the session has frozen and it will eventually time-out with a broken pipe.

To summarise: Network Manager has changed the MAC without so much as a by-your-leave and, unless you have assigned static IP addresses **in the Raspberry Pi** it's quite likely that the Pi will have a different IP address as well. But even a static IP can't save you from the machinations of Network Manager!

The Pi is as happy as the proverbial Larry. It goes on, blissfully unaware that it has just confused the heck out of everything else. You can speed-up some of the activities that need to happen before everything gets going again. You can do things like clear the old entry from the ARP cache on the Mac/PC. You can try to force a multicast DNS daemon restart so that the "raspberrypi.local" address gets updated more quickly but mDNS is a distributed database so it can be hit and miss (and can sometimes lead to complaints about two devices trying to use the same name). Usually, the most effective thing you can do is pull power from the Pi, reboot your Mac/PC (easiest way to clear its ARP cache) and then apply power to the Pi so that it announces its mDNS address at the right time for the newly-booted Mac/PC to hear it and update its mDNS records. 

That's why the installation advice says words to the effect of:

> whatever else you do, **don't** try to install Network Manager while you're connected over WiFi. If SSH is how you're going to do it, you're in for a world of pain if you don't run an Ethernet cable for at least that part of the process.

And it does get worse, of course. Installing Network Manager turns on random WiFi MAC. You can turn it off and go back to the fixed MAC. But then, when you install Docker, it happens again. It may also be that other packages come along in future and say, "hey, look, Network Manager is installed - let's take advantage of that" and it happens again when you least expect it.

Devices changing their MACs at random is becoming reasonably common. If you have a mobile device running a reasonably current OS, it is probably changing its MAC all the time. The idea is to make it hard for Fred's Corner Store to track you and conclude, "Hey, Jim is back in the shop again."

Random MACs are not a problem for a **client** device like a phone, tablet or laptop. But they are definitely a serious problem for a **server** device.

> In TCP/IP any device can be a client or a server for any protocol. The distinction here is about *typical* use. A mobile device is not usually set up to *offer* services like MQTT or Node-RED. It typically *initiates* connections with servers like Docker containers running on a Raspberry Pi.

It is not just configuration-time SSH sessions that break. If you decide to leave Raspberry Pi random Wifi MAC active **and** you have other clients (eq IoT devices) communicating with the Pi over WiFi, you will wrong-foot those clients each time the Raspberry Pi reboots. Data communications services from those clients will be impacted until those client devices time-out and catch up.