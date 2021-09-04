## Source
* [Docker hub](https://hub.docker.com/r/linuxserver/mariadb/)
* [Webpage](https://mariadb.org/)

## About

MariaDB is a fork of MySQL. This is an unofficial image provided by linuxserver.io because there is no official image for arm.

## Connecting to the DB

The port is 3306. It exists inside the docker network so you can connect via `mariadb:3306` for internal connections. For external connections use `<your Pis IP>:3306`

![image](https://user-images.githubusercontent.com/46672225/69734358-7f030800-1137-11ea-9874-7d2c86b3d239.png)

## Setup

Before starting the stack, edit the `docker-compose.yml` file and check your environment variables. In particular:

```
  environment:
    - TZ=Etc/UTC
    - MYSQL_ROOT_PASSWORD=
    - MYSQL_DATABASE=default
    - MYSQL_USER=mariadbuser
    - MYSQL_PASSWORD=
```

If you are running old-menu, you will have to set both passwords. Under new-menu, the menu may have allocated random passwords for you but you can change them if you like.

You only get the opportunity to change the `MQSL_` prefixed environment variables before you bring up the container for the first time. If you decide to change these values after initialisation, you will either have to:

1. Erase the persistent storage area and start again. There are three steps:

	* Stop the container and remove the persistent storage area:

		```
		$ cd ~/IOTstack
		$ docker-compose rm --force --stop -v mariadb
		$ sudo rm -rf ./volumes/mariadb
		```
		
	* Edit `docker-compose.yml` and change the variables.
	* Bring up the container:
	
		```
		$ docker-compose up -d mariadb 
		```

2. Open a terminal window within the container (see below) and change the values by hand.

	> The how-to is beyond the scope of this documentation. Google is your friend!

## Terminal

You can open a terminal session within the mariadb container via:

```
$ docker exec -it mariadb bash
```

To close the terminal session, either:

* type "exit" and press <kbd>return</kbd>; or
* press <kbd>control</kbd>+<kbd>d</kbd>.

## Keeping MariaDB up-to-date

To update the `mariadb` container:

```
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull mariadb
$ docker-compose up -d mariadb
$ docker system prune
$ docker system prune
```

The first "prune" removes the old *local* image, the second removes the old *base* image.
