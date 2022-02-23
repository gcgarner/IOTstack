# Home Assistant

Home Assistant is a home automation platform. It is able to track and control all devices at your home and offer a platform for automating control.

## <a name="references"> References </a>

- [Home Assistant home page](https://www.home-assistant.io/)

	- [Raspberry Pi installation](https://www.home-assistant.io/installation/raspberrypi/)
	- [General installation](https://www.home-assistant.io/installation) (may be useful if you are trying to run on other hardware).

- [GitHub repository](https://github.com/home-assistant/core)
- [DockerHub](https://hub.docker.com/r/homeassistant/home-assistant/)


## <a name="twoVersions">Home Assistant: two versions</a>

There are two versions of Home Assistant:

* Home Assistant Container; and
* Supervised Home Assistant (also known as both "Hass.io" and "Home Assistant Core").

Each version:

* provides a web-based management interface on port 8123; and
* runs in "host mode" in order to discover devices on your LAN, including devices communicating via multicast traffic.

Home Assistant Container runs as a **single** Docker container, and doesn't support all the features that Supervised Home Assistant does (such as add-ons). Supervised Home Assistant runs as a **collection** of Docker containers under its own orchestration.

Technically, both versions of Home Assistant can be installed on your Raspberry Pi but you can't **run** both at the same time. Each version runs in "host mode" and binds to port 8123 so, in practice, the first version to start will claim the port and the second will then be blocked.

IOTstack used to offer a menu entry leading to a convenience script that could install Supervised Home Assistant but that stopped working when Home Assistant changed their approach. Now, the only method supported by IOTstack is Home Assistant Container.

### <a name="installHAContainer"> Installing Home Assistant Container </a>

Home Assistant (Container) can be found in the `Build Stack` menu. Selecting it in this menu results in a service definition being added to:

```
~/IOTstack/docker-compose.yml
```

When you choose "Home Assistant", the service definition added to your `docker-compose.yml` includes the following:

```yaml
image: ghcr.io/home-assistant/home-assistant:stable
#image: ghcr.io/home-assistant/raspberrypi3-homeassistant:stable
#image: ghcr.io/home-assistant/raspberrypi4-homeassistant:stable
```

The active image is *generic* in the sense that it should work on any platform. You may wish to edit your `docker-compose.yml` to deactivate the generic image in favour of an image tailored to your hardware.

The normal IOTstack commands apply to Home Assistant Container such as:

```bash
$ cd ~/IOTstack
$ docker-compose up -d
```

### <a name="installHASupervised"> Installing Supervised Home Assistant </a>

The direction being taken by the Home Assistant folks is to supply a ready-to-run image for your Raspberry Pi. That effectively dedicates your Raspberry Pi to Home Assistant and precludes the possibility of running alongside IOTstack and containers like Mosquitto, InfluxDB, Node-RED, Grafana, PiHole and WireGuard.

It is possible to run Supervised Home Assistant on the same Raspberry Pi as IOTstack. The recommended approach is to start from a clean slate and use [PiBuilder](https://github.com/Paraphraser/PiBuilder).

When you visit the PiBuilder link you may well have a reaction like "all far too complicated" but you should try to get past that. PiBuilder has two main use-cases:

1. Getting a Raspberry Pi built for IOTstack (and, optionally, Supervised Home Assistant) with the least fuss.
2. Letting you record all your own customisations so that you can rebuild your Pis quickly with all your customisations already in place (the "magic smoke" scenario).

It's the second use-case that produces most of the apparent complexity you see when you read the [PiBuilder README](https://github.com/Paraphraser/PiBuilder/blob/master/README.md) for the first time.

The first time you use PiBuilder, the process boils down to:

1. Clone the PiBuilder repo onto your support host (Mac, Windows, etc).
2. Customise two files within the PiBuilder scope:

	- `wpa_supplicant.conf`
	- `options.sh` where, among other things, you will enable:

		- `HOME_ASSISTANT_SUPERVISED_INSTALL=true`

3. Choose a Raspbian image and transfer it to your installation media (SD/SSD). The imaging tools typically finish by ejecting the installation media.
4. Re-mount the installation media on your support host and either:

	- Run the supplied `setup_boot_volume.sh` script (if your support host is macOS or Unix); or
	- Just drag the *contents* of the PiBuilder "boot" folder into the top level of the "/boot" partition on your installation media (if your support host is Windows).

5. Move the installation media to your Raspberry Pi and apply power.
6. Run the scripts in order:

	Step | Command run on support host       | Command run on Raspberry Pi
	:---:|-----------------------------------|-------------
	1    | `ssh -4 pi@raspberrypi.local`     |
	2    |                                   | `/boot/scripts/01_setup.sh «name»`
	3    | `ssh-keygen -R raspberrypi.local` |
	4    | `ssh -4 pi@«name».local`          |
	5    |                                   | `/boot/scripts/02_setup.sh`
	6    | `ssh pi@«name».local`             |
	7    |                                   | `/boot/scripts/03_setup.sh`
	8    | `ssh pi@«name».local`             |
	9    |                                   | `/boot/scripts/04_setup.sh`
	10   | `ssh pi@«name».local`             |
	11   |                                   | `/boot/scripts/05_setup.sh`

	where «name» is the name you give to your Raspberry Pi (eg "iot-hub").

After step 9, Supervised Home Assistant will be running. The `04_setup.sh` script also deals with the [random MACs](#aboutRandomMACs) problem. After step 11, you'll be able to either:

1. Restore a backup; or
2. Run the IOTstack menu and choose your containers.

## <a name="aboutRandomMACs"> Why random MACs are such a hassle </a>

> This material was originally posted as part of [Issue 312](https://github.com/SensorsIot/IOTstack/issues/312). It was moved here following a suggestion by [lole-elol](https://github.com/lole-elol).

When you connect to a Raspberry Pi via SSH (Secure Shell), that's a layer 7 protocol that is riding on top of TCP/IP. TCP (Transmission Control Protocol) is a layer 4 connection-oriented protocol which rides on IP (Internet Protocol) which is a layer 3 protocol. So far, so good.

But you also need to know what happens at layers 2 and 1. When your SSH client (eg Mac or PC or another Unix box) opens its SSH connection, at layer 3 the IP stack applies the subnet mask against the IP addresses of both the source device (your Mac, PC, etc) and destination device (Raspberry Pi) to split them into "network portion" (on the left) and "host portion" on the right. It then compares the two network portions and, if they are the same, it says "local network".

> To complete the picture, if they do not compare the same, then IP substitutes the so-called "default gateway" address (ie your router) and repeats the mask-and-compare process which, unless something is seriously mis-configured, will result in those comparing the same and being "local network". This is why data-comms gurus sometimes say, "all networking is local".

What happens next depends on the data communications media but we'll assume Ethernet and WiFi seeing as they are pretty much interchangeable for our purposes.

The source machine (Mac, PC, etc) issues an ARP (address resolution protocol). It is a broadcast frame (we talk about "frames" rather than "packets" at Layer 2) asking the question, "who has this destination IP address?" The Raspberry Pi responds with a unicast packet saying, "that's me" and part of that includes the MAC (media access control) address of the Raspberry Pi. The source machine only does this **once** (and this is a key point). It assumes the relationship between IP address and MAC address will not change and it adds the relationship to its "ARP cache". You can see the cache on any Unix computer with:

```bash
$ arp -a
```

The Raspberry Pi makes the same assumption: it has learned both the IP and MAC address of the source machine (Mac, PC, etc) from the ARP request and has added that to its own ARP cache.

In addition, every layer two switch (got one of those in your home?) has been snooping on this traffic and has learned, for each of its ports, which MAC address(es) are on those ports.

Not "MAC **and** IP". A switch works at Layer 2. All it sees are frames. It only caches MAC addresses!

When the switch saw the "who has?" ARP broadcast, it replicated that out of all of its ports but when the "that's me" came back from the Raspberry Pi as a unicast response, it only went out on the switch port where the source machine (Mac, PC, etc) was attached.

After that, it's all caching. The Mac or PC has a packet to send to the Pi. It finds the hit in its ARP cache, wraps the packet in a frame and sends it out its Ethernet or WiFi interface. Any switches receive the frame, consult their own tables, and send the frame out the port on the next hop to the destination device. It doesn't matter whether you have one switch or several in a cascade, they have all learned the "next hop" to each destination MAC address they have seen. 

Ditto when the Pi sends back any reply packets. ARP. Switch. Mac/PC. All cached.

The same basic principles apply, irrespective of whether the "switching function" is wired (Ethernet) or WiFi, so it doesn't really matter if your home arrangement is as straightforward as Mac or PC and Pi, both WiFi, via a local WiFi "hub" which is either standalone or part of your router. If something is capable of learning where a MAC is, it does.

Still so far so good.

Now comes the problem. You have established an SSH session connected to the Pi over its WiFi interface. You install Network Manager. As part of its setup, Network Manager discards the **fixed** MAC address which is burned into the Pi's WiFi interface and substitutes a randomly generated MAC address. It doesn't ask for permission to do that. It doesn't warn you it's about to do it. It just does it.

When the WiFi interface comes up, it almost certainly "speaks" straight away via DHCP to ask for an IP address. The DHCP server looks in its own table of MAC-to-IP associations (fixed or dynamic, doesn't matter) and says "never seen **that** MAC before - here's a brand new IP address lease".

The DHCP request is broadcast so all the switches will have learned the new MAC but they'll also still have the old MAC (until it times out). The Mac/PC will receive the DHCP broadcast but, unless it's the DHCP server, will discard it. Either way, it has no means of knowing that this new random MAC belongs to the Pi so it can't do anything sensible with the information.

Meanwhile, SSH is trying to keep the session alive. It still thinks "old IP address" and its ARP cache still thinks old IP belongs to old MAC. Switches know where the frames are meant to go but even if a frame does get somewhere near the Pi, the Pi's NIC (network interface card) ignores it because it's now the wrong destination MAC. The upshot is that SSH looks like the session has frozen and it will eventually time-out with a broken pipe.

To summarise: Network Manager has changed the MAC without so much as a by-your-leave and, unless you have assigned static IP addresses **in the Raspberry Pi** it's quite likely that the Pi will have a different IP address as well. But even a static IP can't save you from the machinations of Network Manager!

The Pi is as happy as the proverbial Larry. It goes on, blissfully unaware that it has just confused the heck out of everything else. You can speed-up some of the activities that need to happen before everything gets going again. You can do things like clear the old entry from the ARP cache on the Mac/PC. You can try to force a multicast DNS daemon restart so that the "raspberrypi.local" address gets updated more quickly but mDNS is a distributed database so it can be hit and miss (and can sometimes lead to complaints about two devices trying to use the same name). Usually, the most effective thing you can do is pull power from the Pi, reboot your Mac/PC (easiest way to clear its ARP cache) and then apply power to the Pi so that it announces its mDNS address at the right time for the newly-booted Mac/PC to hear it and update its mDNS records. 

That's why the installation advice says words to the effect of:

> whatever else you do, **don't** try to install Network Manager while you're connected over WiFi. If SSH is how you're going to do it, you're in for a world of pain if you don't run an Ethernet cable for at least that part of the process.

And it does get worse, of course. Installing Network Manager turns on random WiFi MAC. You can turn it off and go back to the fixed MAC. But then, when you install Docker, it happens again. It may also be that other packages come along in future and say, "hey, look, Network Manager is installed - let's take advantage of that" and it happens again when you least expect it.

Devices changing their MACs at random is becoming reasonably common. If you have a mobile device running a reasonably current OS, it is probably changing its MAC all the time. The idea is to make it hard for Fred's Corner Store to track you and conclude, "Hey, Alex is back in the shop again."

Random MACs are not a problem for a **client** device like a phone, tablet or laptop. But they are definitely a serious problem for a **server** device.

> In TCP/IP any device can be a client or a server for any protocol. The distinction here is about *typical* use. A mobile device is not usually set up to *offer* services like MQTT or Node-RED. It typically *initiates* connections with servers like Docker containers running on a Raspberry Pi.

It is not just configuration-time SSH sessions that break. If you decide to leave Raspberry Pi random Wifi MAC active **and** you have other clients (eq IoT devices) communicating with the Pi over WiFi, you will wrong-foot those clients each time the Raspberry Pi reboots. Data communications services from those clients will be impacted until those client devices time-out and catch up.

# Using bluetooth from the container
In order to be able to use BT & BLE devices from HA integrations, make sure that bluetooth is enabled and powered on at the start of the (Rpi) host by editing `/etc/bluetooth/main.conf`:

```conf
....
[Policy]
AutoEnable=true
```

After a reboot, check that BT is up:

```sh
(root) # hciconfig
...
UP
...
```
ref: https://scribles.net/auto-power-on-bluetooth-adapter-on-boot-up/
