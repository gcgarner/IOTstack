# AdGuard Home

## References

* [AdGuard Home GitHub](https://github.com/AdguardTeam/AdGuardHome)
* [AdGuard Home DockerHub](https://hub.docker.com/r/adguard/adguardhome)

## Either *AdGuard Home* or *PiHole*, but not both

AdGuard Home and PiHole perform similar functions. They use the same ports so you can **not** run both at the same time. You must choose one or the other.

## <a name="quickStart"> Quick Start </a>

When you first install AdGuard Home:

1. Use a web browser to connect to it using port 3001. For example:

	```
	http://raspberrypi.local:3001
	```

2. Click "Getting Started".

3. Change the port number for the Admin Web Interface to be "8089". Leave the other settings on the page at their defaults and click "Next".
4. Enter a username and password and click "Next".
5. Click "Open Dashboard". This redirects to port 8089.
6. After the initial setup, you connect to AdGuard Home via port 8089:

	```
	http://raspberrypi.local:8089
	```

## About port 8089

Port 8089 is the default administrative user interface for AdGuard Home running under IOTstack.

Port 8089 is not active until you have completed the [Quick Start](#quickStart) procedure. You must start by connecting to port 3001.

Because of AdGuard Home limitations, you must take special precautions if you decide to change to a different port number:

1. The internal and external ports **must** be the same; and

2. You **must** convince AdGuard Home that it is a first-time installation: 

	```
	 $ cd ~/IOTstack
	 $ docker-compose stop adguardhome
	 $ docker-compose rm -f adguardhome
	 $ sudo rm -rf ./volumes/adguardhome
	 $ docker-compose up -d adguardhome
	```

3. Repeat the [Quick Start](#quickStart) procedure, this time substituting the new Admin Web Interface port where you see "8089".

## About port 3001:3000

Port 3001 (external, 3000 internal) is only used during [Quick Start](#quickStart) procedure. Once port 8089 becomes active, port 3001 ceases to be active.

In other words, you need to keep port 3001 reserved even though it is only ever used to set up port 8089.

## About Host Mode

If you want to run AdGuard Home as your DHCP server, you need to put the container into "host mode". You need edit the AdGuard Home service definition in `docker-compose.yml` to:

1. add the line:

	```
	network_mode: host
	```

2. remove the `ports:` directive and **all** of the port mappings.

Note:

* It is not really a good idea to offer DHCP services from a container. This is because containers generally start far too late in a boot process to be useful. If you want to use AdGuard Home for DHCP, you should probably consider a native installation.
