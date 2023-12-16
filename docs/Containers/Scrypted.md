---
title: Scrypted
---

# Scrypted – home video integration platform

## References

* [Scrypted home page](https://www.scrypted.app/?)
* [DockerHub](https://hub.docker.com/r/koush/scrypted)
* [GitHub](https://github.com/koush/scrypted#installation)

## Getting started

1. Run the IOTstack menu and select "Scrypted" so that the service definition is added to your compose file.
2. Before starting the container for the first time, run the following commands:

	``` console
	$ cd ~/IOTstack
	$ echo "SCRYPTED_WEBHOOK_UPDATE_AUTHORIZATION=$(cat /proc/sys/kernel/random/uuid | md5sum | head -c 24)" >>.env
	```

	This generates a random token and places it in `~/IOTstack/.env`.
	
	Notes:
	
	1. You only need to do this **once**.
	2. It is not clear whether the token is respected on every launch, or only on first launch.

3. Start Scrypted:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d scrypted
	```
	
	Note:
	
	* scrypted is a **large** image (2.5GB). It takes time to download and decompress!

4. Use the following URL as a template:

	```
	https://«host-or-ip»:10443
	```
	
	Replace `«host-or-ip»` with the domain name or IP address of your Raspberry Pi. Examples:
	
	* `https://raspberrypi.my.domain.com:10443`
	* `https://raspberrypi.local:10443`
	* `https://192.168.1.10:10443`
	
	Note:
	
	* You can't use the `http` protocol. You must use `https`.

5. Paste the URL into a browser window. The container uses a self-signed certificate so you will need to accept that using your browser's mechanisms.
6. Enter a username and password to create your administrator account.


## Troubleshooting

If you see the message:

```
required variable SCRYPTED_WEBHOOK_UPDATE_AUTHORIZATION is missing a value: see instructions for generating a token
```

it means that you did not complete step 2 before starting the container. Go back and perform step 2.

If you need to start over from scratch:

``` console
$ cd ~/IOTstack
$ docker-compose down scrypted
$ sudo rm -rf ./volumes/scrypted
$ docker-compose up -d scrypted
```

> see also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)

## About the service definition

The Scrypted container runs in host mode, which means it binds directly to the Raspberry Pi's ports. The service definition includes:

``` yaml
x-ports:
- "10443:10443"
```

The effect of the `x-` prefix is to comment-out that port mapping. It is included as an aide-memoire to help you remember the port number.

The service definition also includes the following environment variable:

``` yaml
- SCRYPTED_WEBHOOK_UPDATE=http://localhost:10444/v1/update
```

The container does not bind to port 10444 so the purpose of this is not clear. The port number should be treated as reserved. 
