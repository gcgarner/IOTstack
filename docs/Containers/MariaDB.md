# MariaDB

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

```yaml
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

		``` console
		$ cd ~/IOTstack
		$ docker-compose down mariadb
		$ sudo rm -rf ./volumes/mariadb
		```
		
		> see also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)

	* Edit `docker-compose.yml` and change the variables.
	* Bring up the container:

		``` console
		$ docker-compose up -d mariadb
		```

2. Open a terminal window within the container (see below) and change the values by hand.

	> The how-to is beyond the scope of this documentation. Google is your friend!

## Terminal

You can open a terminal session within the mariadb container via:

``` console
$ docker exec -it mariadb bash
```

To connect to the database: `mysql -uroot -p`

To close the terminal session, either:

* type "exit" and press <kbd>return</kbd>; or
* press <kbd>control</kbd>+<kbd>d</kbd>.

## Container health check { #healthCheck }

### theory of operation { #healthCheckTheory }

A script , or "agent", to assess the health of the MariaDB container has been added to the *local image* via the *Dockerfile*. In other words, the script is specific to IOTstack.

The agent is invoked 30 seconds after the container starts, and every 30 seconds thereafter. The agent:

1. Runs the command:

	```
	mysqladmin ping -h localhost
	```

2. If that command succeeds, the agent compares the response returned by the command with the expected response:

	```
	mysqld is alive
	```

3. If the command returned the expected response, the agent tests the responsiveness of the TCP port the `mysqld` daemon should be listening on (see [customising health-check](#healthCheckCustom)).

4. If all of those steps succeed, the agent concludes that MariaDB is functioning properly and returns "healthy".

### monitoring health-check { #healthCheckMonitor }

Portainer's *Containers* display contains a *Status* column which shows health-check results for all containers that support the feature.

You can also use the `docker ps` command to monitor health-check results. The following command narrows the focus to mariadb:

``` console
$ docker ps --format "table {{.Names}}\t{{.Status}}"  --filter name=mariadb
```

Possible reply patterns are:

1. The container is starting and has not yet run the health-check agent:

	```
	NAMES     STATUS
	mariadb   Up 5 seconds (health: starting)
	```

2. The container has been running for at least 30 seconds and the health-check agent has returned a positive result within the last 30 seconds:

	```
	NAMES     STATUS
	mariadb   Up 33 seconds (healthy)
	```

3. The container has been running for more than 90 seconds but has failed the last three successive health-check tests:

	```
	NAMES     STATUS
	mariadb   Up About a minute (unhealthy)
	```

### customising health-check { #healthCheckCustom }

You can customise the operation of the health-check agent by editing the `mariadb` service definition in your *Compose* file:

1. By default, the `mysqld` daemon listens to **internal** port 3306. If you need change that port, you also need to inform the health-check agent via an environment variable. For example, suppose you changed the **internal** port to 12345:

	```yaml
	    environment:
	      - MYSQL_TCP_PORT=12345
	```

	Notes:

	* The `MYSQL_TCP_PORT` variable is [defined by MariaDB](https://mariadb.com/kb/en/mariadb-environment-variables/), not IOTstack, so changing this variable affects more than just the health-check agent.
	* If you are running "old menu", this change should be made in the file:

		```
		~/IOTstack/services/mariadb/mariadb.env
		```

2. The `mysqladmin ping` command relies on the root password supplied via the `MYSQL_ROOT_PASSWORD` environment variable in the *Compose* file. The command will not succeed if the root password is not correct, and the agent will return "unhealthy". 

3. If the health-check agent misbehaves in your environment, or if you simply don't want it to be active, you can disable all health-checking for the container by adding the following lines to its service definition:

	```yaml
	    healthcheck:
	      disable: true
	```

	Note:

	* The mere presence of a `healthcheck:` clause in the `mariadb` service definition overrides the supplied agent. In other words, the following can't be used to re-enable the supplied agent:

		```yaml
		    healthcheck:
		      disable: false
		```

		You must remove the entire `healthcheck:` clause.

## Keeping MariaDB up-to-date

To update the `mariadb` container:

``` console
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull mariadb
$ docker-compose up -d mariadb
$ docker system prune
$ docker system prune
```

The first "prune" removes the old *local* image, the second removes the old *base* image.
