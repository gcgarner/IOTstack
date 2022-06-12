# Mosquitto

This document discusses an IOTstack-specific version of Mosquitto built on top of [Eclipse/Mosquitto](https://github.com/eclipse/mosquitto) using a *Dockerfile*.

> If you want the documentation for the original implementation of Mosquitto (just "as it comes" from *DockerHub*) please see [Mosquitto.md](https://github.com/SensorsIot/IOTstack/blob/old-menu/docs/Containers/Mosquitto.md) on the old-menu branch.
 
<hr>

## References

- [*Eclipse Mosquitto* home](https://mosquitto.org)
- [*GitHub*: eclipse/mosquitto](https://github.com/eclipse/mosquitto)
- [*DockerHub*: eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)
- [Setting up passwords](https://www.youtube.com/watch?v=1msiFQT_flo) (video)
- [Tutorial: from MQTT to InfluxDB via Node-Red](https://gist.github.com/Paraphraser/c9db25d131dd4c09848ffb353b69038f)

## Significant directories and files

```
~/IOTstack
├── .templates
│   └── mosquitto
│       ├── service.yml ❶
│       ├── Dockerfile ❷
│       ├── docker-entrypoint.sh ❸
│       └── iotstack_defaults ❹
│           ├── config
│           │   ├── filter.acl
│           │   └── mosquitto.conf
│           └── pwfile
│               └── pwfile
├── services
│   └── mosquitto
│       └── service.yml ❺
├── docker-compose.yml ❻
└── volumes
    └── mosquitto ❼
        ├── config
        │   ├── filter.acl 
        │   └── mosquitto.conf
        ├── data
        │   └── mosquitto.db
        ├── log
        └── pwfile 
            └── pwfile
```

1. The *template service definition*.
2. The *Dockerfile* used to customise Mosquitto for IOTstack.
3. A replacement for the Eclipse-Mosquitto script of the same name, extended to handle container self-repair.
4. A standard set of defaults for IOTstack (used to initialise defaults on first run, and for container self-repair).
5. The *working service definition* (only relevant to old-menu, copied from ❶).
6. The *Compose* file (includes ❶).
7. The *persistent storage area*:

	* Directories and files in ❼ are owned by userID 1883. This is enforced each time Mosquitto starts.
	* You will normally need `sudo` to make changes in this area.
	* Each time Mosquitto starts, it automatically replaces anything originating in ❹ that has gone missing from ❼. This "self-repair" function is intended to provide reasonable assurance that Mosquitto will at least **start** instead of going into a restart loop.

## How Mosquitto gets built for IOTstack

### Mosquitto source code ([*GitHub*](https://github.com))

The source code for Mosquitto lives at [*GitHub* eclipse/mosquitto](https://github.com/eclipse/mosquitto).

### Mosquitto images ([*DockerHub*](https://hub.docker.com))

Periodically, the source code is recompiled and the resulting image is pushed to [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto?tab=tags&page=1&ordering=last_updated) on *DockerHub*.
 
### IOTstack menu

When you select Mosquitto in the IOTstack menu, the *template service definition* is copied into the *Compose* file.

> Under old menu, it is also copied to the *working service definition* and then not really used.

### IOTstack first run

On a first install of IOTstack, you run the menu, choose Mosquitto as one of your containers, and are told to do this:

```console
$ cd ~/IOTstack
$ docker-compose up -d
```

> See also the [Migration considerations](#migration) (below).

`docker-compose` reads the *Compose* file. When it arrives at the `mosquitto` fragment, it finds:

```yaml
  mosquitto:
    container_name: mosquitto
    build:
      context: ./.templates/mosquitto/.
      args:
      - MOSQUITTO_BASE=eclipse-mosquitto:latest
    …
```

Note:

* Earlier versions of the Mosquitto service definition looked like this:

	```yaml
	  mosquitto:
	    container_name: mosquitto
	    build: ./.templates/mosquitto/.
	    …
	```

	The single-line `build` produces *exactly* the same result as the four-line `build`, save that the single-line form does not support [pinning Mosquitto to a specific version](#versionPinning).

The `./.templates/mosquitto/.` path associated with the `build` tells `docker-compose` to look for:

```
~/IOTstack/.templates/mosquitto/Dockerfile
```

> The *Dockerfile* is in the `.templates` directory because it is intended to be a common build for **all** IOTstack users. This is different to the arrangement for Node-RED where the *Dockerfile* is in the `services` directory because it is how each individual IOTstack user's version of Node-RED is customised.

The *Dockerfile* begins with:

```dockerfile
ARG MOSQUITTO_BASE=eclipse-mosquitto:latest
FROM $MOSQUITTO_BASE
```

The `FROM` statement tells the build process to pull down the ***base image*** from [*DockerHub*](https://hub.docker.com).

> It is a ***base*** image in the sense that it never actually runs as a container on your Raspberry Pi.

The remaining instructions in the *Dockerfile* customise the *base image* to produce a ***local image***. The customisations are:

1. Add the `rsync` and `tzdata` packages.

	* `rsync` helps the container perform self-repair; while
	* `tzdata` enables Mosquitto to respect the "TZ" environment variable.

2. Add a standard set of configuration defaults appropriate for IOTstack.
3. Replace `docker-entrypoint.sh` with a version which:

	* Calls `rsync` to perform self-repair if configuration files go missing; and
	* Enforces 1883:1883 ownership in `~/IOTstack/volumes/mosquitto`.

The *local image* is instantiated to become your running container.

When you run the `docker images` command after Mosquitto has been built, you *may* see two rows for Mosquitto:

```console
$ docker images
REPOSITORY                      TAG         IMAGE ID       CREATED        SIZE
iotstack_mosquitto              latest      cf0bfe1a34d6   4 weeks ago    11.6MB
eclipse-mosquitto               latest      46ad1893f049   4 weeks ago    8.31MB
```

* `eclipse-mosquitto` is the *base image*; and
* `iotstack_mosquitto` is the *local image*.

You *may* see the same pattern in Portainer, which reports the *base image* as "unused". You should not remove the *base* image, even though it appears to be unused.

> Whether you see one or two rows depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

### Migration considerations { #migration }

Under the original IOTstack implementation of Mosquitto (just "as it comes" from *DockerHub*), the service definition expected the configuration files to be at:

```
~/IOTstack/services/mosquitto/mosquitto.conf
~/IOTstack/services/mosquitto/filter.acl
```

Under this implementation of Mosquitto, the configuration files have moved to:

```
~/IOTstack/volumes/mosquitto/config/mosquitto.conf
~/IOTstack/volumes/mosquitto/config/filter.acl
```

> The change of location is one of the things that allows self-repair to work properly. 

The default versions of each configuration file are the **same**. Only the **locations** have changed. If you did not alter either file when you were running the original IOTstack implementation of Mosquitto, there will be no change in Mosquitto's behaviour when it is built from a *Dockerfile*.

However, if you did alter either or both configuration files, then you should compare the old and new versions and decide whether you wish to retain your old settings. For example:

```console
$ cd ~/IOTstack
$ diff ./services/mosquitto/mosquitto.conf ./volumes/mosquitto/config/mosquitto.conf 
```

> You can also use the `-y` option on the `diff` command to see a side-by-side comparison of the two files.

Using `mosquitto.conf` as the example, assume you wish to use your existing file instead of the default:

1. To move your existing file into the new location:

	```console
	$ cd ~/IOTstack
	$ sudo mv ./services/mosquitto/mosquitto.conf ./volumes/mosquitto/config/mosquitto.conf
	```

	> The move overwrites the default. At this point, the moved file will probably be owned by user "pi" but that does not matter.

2. Mosquitto will always enforce correct ownership (1883:1883) on any restart but it will not overwrite permissions. If in doubt, use mode 644 as your default for permissions:

	```console
	$ sudo chmod 644 ./services/mosquitto/mosquitto.conf
	```

3. Restart Mosquitto:

	```console
	$ docker-compose restart mosquitto
	```

4. Check your work:

	```console
	$ ls -l ./volumes/mosquitto/config/mosquitto.conf
	-rw-r--r-- 1 1883 1883 ssss mmm dd hh:mm ./volumes/mosquitto/config/mosquitto.conf
	```

5. If necessary, repeat these steps with `filter.acl`.

## Logging

Mosquitto logging is controlled by `mosquitto.conf`. This is the default configuration:

```apacheconf
#log_dest file /mosquitto/log/mosquitto.log
log_dest stdout
log_timestamp_format %Y-%m-%dT%H:%M:%S
# Reduce size and SD-card flash wear, safe to remove if using a SSD
connection_messages false
```

When `log_dest` is set to 	`stdout`, you inspect Mosquitto's logs like this:

```console
$ docker logs mosquitto
```

Logs written to `stdout` are stored and persisted to disk as managed by Docker.
They are kept over reboots, but are lost when your Mosquitto container is
removed or updated.

The alternative, which *may* be more appropriate if you are running on an SSD or HD, is to change `mosquitto.conf` to be like this:

```
log_dest file /mosquitto/log/mosquitto.log
#log_dest stdout
log_timestamp_format %Y-%m-%dT%H:%M:%S
```

and then restart Mosquitto:

```console
$ cd ~/IOTstack
$ docker-compose restart mosquitto
```

The path `/mosquitto/log/mosquitto.log` is an **internal** path. When this style of logging is active, you inspect Mosquitto's logs using the **external** path like this:

```console
$ sudo tail ~/IOTstack/volumes/mosquitto/log/mosquitto.log
```

> You need to use `sudo` because the log is owned by userID 1883 and Mosquitto creates it without "world" read permission.

Logs written to `mosquitto.log` persist until you take action to prune the file.

## Security

### Configuring security

Mosquitto security is controlled by `mosquitto.conf`. These are the relevant directives:

```
#password_file /mosquitto/pwfile/pwfile
allow_anonymous true
```

Mosquitto security can be in four different states, which are summarised in the following table:

`password_file` | `allow_anonymous` | security enforcement | remark            |
:--------------:|:-----------------:|:--------------------:|-------------------|
disabled        | true              | open access          | default           |
disabled        | false             | all access denied    | not really useful |
enabled         | true              | credentials optional |                   |
enabled         | false             | credentials required |                   |


### Password file management

The password file for Mosquitto is part of a mapped volume:

* The **internal** path is `/mosquitto/pwfile/pwfile`
* The **external** path is `~/IOTstack/volumes/mosquitto/pwfile/pwfile`

A common problem with the previous version of Mosquitto for IOTstack occurred when the `password_file` directive was enabled but the `pwfile` was not present. Mosquitto went into a restart loop.

The Mosquitto container performs self-repair each time the container is brought up or restarts. If `pwfile` is missing, an empty file is created as a placeholder. This prevents the restart loop. What happens next depends on `allow_anonymous`:

* If `true` then:

	- Any MQTT request *without* credentials will be permitted;
	- Any MQTT request *with* credentials will be rejected (because `pwfile` is empty so there is nothing to match on).

* If `false` then **all** MQTT requests will be rejected.

#### create username and password

To create a username and password, use the following as a template.
 
```console
$ docker exec mosquitto mosquitto_passwd -b /mosquitto/pwfile/pwfile «username» «password» 
```

Replace «username» and «password» with appropriate values, then execute the command. For example, to create the username "hello" with password "world":

```console
$ docker exec mosquitto mosquitto_passwd -b /mosquitto/pwfile/pwfile hello world
```

Note:

* See also [customising health-check](#healthCheckCustom). If you are creating usernames and passwords, you may also want to create credentials for the health-check agent.

#### check password file

There are two ways to verify that the password file exists and has the expected content:

1. View the file using its **external** path: 

	```console
	$ sudo cat ~/IOTstack/volumes/mosquitto/pwfile/pwfile 
	```

	> `sudo` is needed because the file is neither owned nor readable by `pi`.

2. View the file using its **internal** path:

	```console
	$ docker exec mosquitto cat /mosquitto/pwfile/pwfile
	```

Each credential starts with the username and occupies one line in the file: 

```
hello:$7$101$ZFOHHVJLp2bcgX+h$MdHsc4rfOAhmGG+65NpIEJkxY0beNeFUyfjNAGx1ILDmI498o4cVOaD9vDmXqlGUH9g6AgHki8RPDEgjWZMkDA==
```

#### remove entry from password file

To remove an entry from the password file:

```console
$ docker exec mosquitto mosquitto_passwd -D /mosquitto/pwfile/pwfile «username»
```

#### reset the password file

There are several ways to reset the password file. Your options are:

1. Remove the password file and restart Mosquitto:

	```console
	$ cd ~/IOTstack
	$ sudo rm ./volumes/mosquitto/pwfile/pwfile
	$ docker-compose restart mosquitto 
	```

	The result is an empty password file.

2. Clear all existing passwords while adding a new password:

	```console
	$ docker exec mosquitto mosquitto_passwd -c -b /mosquitto/pwfile/pwfile «username» «password»
	```

	The result is a password file with a single entry.

3. Clear all existing passwords in favour of a single dummy password which is then removed:

	```console
	$ docker exec mosquitto mosquitto_passwd -c -b /mosquitto/pwfile/pwfile dummy dummy
	$ docker exec mosquitto mosquitto_passwd -D /mosquitto/pwfile/pwfile dummy
	```

	The result is an empty password file.

### Activate Mosquitto security

1. Use `sudo` and your favourite text editor to open the following file:

	```
	~/IOTstack/volumes/mosquitto/config/mosquitto.conf
	```

2. Remove the comment indicator from the following line:

	```
	#password_file /mosquitto/pwfile/pwfile
	```

	so that it becomes:

	```
	password_file /mosquitto/pwfile/pwfile
	```

3. Set `allow_anonymous` as required:

	```
	allow_anonymous true
	```

	If `true` then:

	* Any MQTT request without credentials will be permitted;
	* The validity of credentials supplied with any MQTT request will be enforced.

	If `false` then:

	* Any MQTT request without credentials will be rejected;
	* The validity of credentials supplied with any MQTT request will be enforced.

4. Save the modified configuration file and restart Mosquitto:

	```console
	$ cd ~/IOTstack
	$ docker-compose restart mosquitto
	```

### Testing Mosquitto security

#### assumptions

1. You have created at least one username ("hello") and password ("world").
2. `password_file` is enabled.
3. `allow_anonymous` is `false`.

#### install testing tools

If you do not have the Mosquitto clients installed on your Raspberry Pi (ie `$ which mosquitto_pub` does not return a path), install them using:

```console
$ sudo apt install -y mosquitto-clients
```

#### test: *anonymous access is prohibited*

Test **without** providing credentials:

```console
$ mosquitto_pub -h 127.0.0.1 -p 1883 -t "/password/test" -m "up up and away"
Connection Refused: not authorised.
Error: The connection was refused.
```

Note:

* The error is the expected result and shows that Mosquitto will not allow anonymous access.

#### test: *access with credentials is permitted*

Test with credentials

```console
$ mosquitto_pub -h 127.0.0.1 -p 1883 -t "/password/test" -m "up up and away" -u hello -P world
$ 
```

Note:

* The absence of any error message means the message was sent. Silence = success!

#### test: *round-trip with credentials is permitted*

Prove round-trip connectivity will succeed when credentials are provided. First, set up a subscriber as a background process. This mimics the role of a process like Node-Red:

```console
$ mosquitto_sub -v -h 127.0.0.1 -p 1883 -t "/password/test" -F "%I %t %p" -u hello -P world &
[1] 25996
```

Repeat the earlier test:

```console
$ mosquitto_pub -h 127.0.0.1 -p 1883 -t "/password/test" -m "up up and away" -u hello -P world
2021-02-16T14:40:51+1100 /password/test up up and away
```

Note:

* the second line above is coming from the `mosquitto_sub` running in the background.

When you have finished testing you can kill the background process (press return twice after you enter the `kill` command):

```console
$ kill %1
$
[1]+  Terminated              mosquitto_sub -v -h 127.0.0.1 -p 1883 -t "/password/test" -F "%I %t %p" -u hello -P world
```

## Container health check

### theory of operation

A script , or "agent", to assess the health of the Mosquitto container has been added to the *local image* via the *Dockerfile*. In other words, the script is specific to IOTstack.

The agent is invoked 30 seconds after the container starts, and every 30 seconds thereafter. The agent:

* Publishes a retained MQTT message to the broker running in the same container. The message payload is the current date and time, and the default topic string is:

	```
	iotstack/mosquitto/healthcheck
	```

* Subscribes to the same broker for the same topic for a single message event.
* Compares the payload sent with the payload received. If the payloads (ie time-stamps) match, the agent concludes that the Mosquitto broker (the process running inside the same container) is functioning properly for round-trip messaging.

### monitoring health-check { #healthCheckMonitor }

Portainer's *Containers* display contains a *Status* column which shows health-check results for all containers that support the feature.

You can also use the `docker ps` command to monitor health-check results. The following command narrows the focus to mosquitto:

```console
$ docker ps --format "table {{.Names}}\t{{.Status}}"  --filter name=mosquitto
```

Possible reply patterns are:

1. The container is starting and has not yet run the health-check agent:

	```
	NAMES       STATUS
	mosquitto   Up 3 seconds (health: starting)
	```

2. The container has been running for at least 30 seconds and the health-check agent has returned a positive result within the last 30 seconds:

	```
	NAMES       STATUS
	mosquitto   Up 34 seconds (healthy)
	```

3. The container has been running for more than 90 seconds but has failed the last three successive health-check tests:

	```
	NAMES       STATUS
	mosquitto   Up About a minute (unhealthy)
	```

You can also subscribe to the same topic that the health-check agent is using to view the retained messages as they are published:

```console
$ mosquitto_sub -v -h localhost -p 1883 -t "iotstack/mosquitto/healthcheck" -F "%I %t %p"
```

Notes:

* This assumes you are running the command *outside* container-space on the *same* host as your Mosquitto container. If you run this command from *another* host, replace `localhost` with the IP address or domain name of the host where your Mosquitto container is running.
* The `-p 1883` is the *external* port. You will need to adjust this if you are using a different *external* port for your MQTT service.
* If you enable authentication for your Mosquitto broker, you will need to add `-u «user»` and `-P «password»` parameters to this command.
* You should expect to see a new message appear approximately every 30 seconds. That indicates the health-check agent is functioning normally. Use <kbd>control</kbd>+<kbd>c</kbd> to terminate the command.

### customising health-check { #healthCheckCustom }

You can customise the operation of the health-check agent by editing the `mosquitto` service definition in your *Compose* file:

1. By default, the mosquitto broker listens to **internal** port 1883. If you need change that port, you also need to inform the health-check agent via an environment variable. For example, suppose you changed the **internal** port to 12345:

	```yaml
	    environment:
	      - HEALTHCHECK_PORT=12345
	```

2. If the default topic string used by the health-check agent causes a name-space collision, you can override it. For example, you could use a Universally-Unique Identifier (UUID):

	```yaml
	    environment:
	      - HEALTHCHECK_TOPIC=4DAA361F-288C-45D5-9540-F1275BDCAF02
	```

	Note:

	* You will also need to use the same topic string in the `mosquitto_sub` command shown at [monitoring health-check](#healthCheckMonitor).

3. If you have enabled authentication for your Mosquitto broker service, you will need to provide appropriate credentials for your health-check agent:

	```yaml
	    environment:
	      - HEALTHCHECK_USER=healthyUser
	      - HEALTHCHECK_PASSWORD=healthyUserPassword
	```

4. If the health-check agent misbehaves in your environment, or if you simply don't want it to be active, you can disable all health-checking for the container by adding the following lines to its service definition:

	```yaml
	    healthcheck:
	      disable: true
	```

	Notes:

	* The directives to disable health-checking are independent of the environment variables. If you want to disable health-checking temporarily, there is no need to remove any `HEALTHCHECK_` environment variables that may already be in place.
	* Conversely, the mere presence of a `healthcheck:` clause in the `mosquitto` service definition overrides the supplied agent. In other words, the following can't be used to re-enable the supplied agent:

		```yaml
		    healthcheck:
		      disable: false
		```

		You must remove the entire `healthcheck:` clause.

## Upgrading Mosquitto

You can update most containers like this:

```console
$ cd ~/IOTstack
$ docker-compose pull
$ docker-compose up -d
$ docker system prune
```

In words:

* `docker-compose pull` downloads any newer images;
* `docker-compose up -d` causes any newly-downloaded images to be instantiated as containers (replacing the old containers); and
* the `prune` gets rid of the outdated images.

This strategy doesn't work when a *Dockerfile* is used to build a *local image* on top of a *base image* downloaded from [*DockerHub*](https://hub.docker.com). The *local image* is what is running so there is no way for the `pull` to sense when a newer version becomes available.

The only way to know when an update to Mosquitto is available is to check the [eclipse-mosquitto tags page](https://hub.docker.com/_/eclipse-mosquitto?tab=tags&page=1&ordering=last_updated) on *DockerHub*.

Once a new version appears on *DockerHub*, you can upgrade Mosquitto like this:

```console
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull mosquitto
$ docker-compose up -d mosquitto
$ docker system prune
$ docker system prune
```

Breaking it down into parts:

* `build` causes the named container to be rebuilt;
* `--no-cache` tells the *Dockerfile* process that it must not take any shortcuts. It really **must** rebuild the *local image*;
* `--pull` tells the *Dockerfile* process to actually check with [*DockerHub*](https://hub.docker.com) to see if there is a later version of the *base image* and, if so, to download it before starting the build;
* `mosquitto` is the named container argument required by the `build` command.

Your existing Mosquitto container continues to run while the rebuild proceeds. Once the freshly-built *local image* is ready, the `up` tells `docker-compose` to do a new-for-old swap. There is barely any downtime for your MQTT broker service.

The `prune` is the simplest way of cleaning up. The first call removes the old *local image*. The second call cleans up the old *base image*. Whether an old *base image* exists depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

### Mosquitto version pinning { #versionPinning }

If an update to Mosquitto introduces a breaking change, you can revert to an earlier know-good version by pinning to that version. Here's how:

1. Use your favourite text editor to open:

	```
	~/IOTstack/docker-compose.yml
	```

2. Find the Mosquitto service definition. If your service definition contains this line:

	```yaml
	build: ./.templates/mosquitto/.
	```

	then replace that line with the following four lines:

	```yaml
	build:
	  context: ./.templates/mosquitto/.
	  args:
	    - MOSQUITTO_BASE=eclipse-mosquitto:latest
	```

	Notes:

	* The four-line form of the `build` directive is now the default for Mosquitto so those lines may already be present in your compose file.
	* Remember to use spaces, not tabs, when editing compose files.

3. Replace `latest` with the version you wish to pin to. For example, to pin to version 2.0.13:

	```yaml
	    - MOSQUITTO_BASE=eclipse-mosquitto:2.0.13
	```

4. Save the file and tell `docker-compose` to rebuild the local image:

	```console
	$ cd ~/IOTstack
	$ docker-compose build --no-cache --pull mosquitto
	$ docker-compose up -d mosquitto
	$ docker system prune
	``` 

	The new *local image* is built, then the new container is instantiated based on that image. The `prune` deletes the old *local image*.

5. Images built in this way will always be tagged with "latest", as in:

	```console
	$ docker images iotstack_mosquitto
	REPOSITORY           TAG       IMAGE ID       CREATED              SIZE
	iotstack_mosquitto   latest    8c0543149b9b   About a minute ago   16.2MB
	```

	You may find it useful to assign an explicit tag to help you remember the version number used for the build. For example:

	```console
	$ docker tag iotstack_mosquitto:latest iotstack_mosquitto:2.0.13
	$ docker images iotstack_mosquitto
	REPOSITORY           TAG       IMAGE ID       CREATED              SIZE
	iotstack_mosquitto   2.0.13    8c0543149b9b   About a minute ago   16.2MB
	iotstack_mosquitto   latest    8c0543149b9b   About a minute ago   16.2MB
	```

	You can also query the image metadata to discover version information:

	```console
	$ docker image inspect iotstack_mosquitto:latest | jq .[0].Config.Labels
	{
	  "com.github.SensorsIot.IOTstack.Dockerfile.based-on": "https://github.com/eclipse/mosquitto",
	  "com.github.SensorsIot.IOTstack.Dockerfile.build-args": "eclipse-mosquitto:2.0.13",
	  "description": "Eclipse Mosquitto MQTT Broker",
	  "maintainer": "Roger Light <roger@atchoo.org>"
	}
	```

## About Port 9001

Earlier versions of the IOTstack service definition for Mosquitto included two port mappings:

```yaml
ports:
  - "1883:1883"
  - "9001:9001"
```

[Issue 67](https://github.com/SensorsIot/IOTstack/issues/67) explored the topic of port 9001 and showed that:

* The base image for Mosquitto did not expose port 9001; and
* The running container was not listening to port 9001.

On that basis, the mapping for port 9001 was removed from `service.yml`.

If you have a use-case that needs port 9001, you can re-enable support by:

1. Inserting the port mapping under the `mosquitto` definition in `docker-compose.yml`:

	```yaml
	- "9001:9001"
	```

2. Inserting the additional listener in `mosquitto.conf`:

	```apacheconf
	listener 1883
	listener 9001
	```

	You need **both** lines. If you omit 1883 then Mosquitto will stop listening to port 1883 and will only listen to port 9001.

3. Restarting the container:

	```console
	$ cd ~/IOTstack
	$ docker-compose restart mosquitto
	```

Please consider raising an issue to document your use-case. If you think your use-case has general application then please also consider creating a pull request to make the changes permanent.
