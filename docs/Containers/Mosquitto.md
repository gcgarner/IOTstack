# Mosquitto

This document discusses an IOTstack-specific version of Mosquitto built on top of [Eclipse/Mosquitto](https://github.com/eclipse/mosquitto) using a *Dockerfile*.

> If you want the documentation for the original implementation of Mosquitto (just "as it comes" from *DockerHub*) please see [Mosquitto.md](https://github.com/SensorsIot/IOTstack/blob/old-menu/docs/Containers/Mosquitto.md) on the old-menu branch.
 
<hr>

## <a name="references"> References </a>

- [*Eclipse Mosquitto* home](https://mosquitto.org)
- [*GitHub*: eclipse/mosquitto](https://github.com/eclipse/mosquitto)
- [*DockerHub*: eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)
- [Setting up passwords](https://www.youtube.com/watch?v=1msiFQT_flo) (video)
- [Tutorial: from MQTT to InfluxDB via Node-Red](https://gist.github.com/Paraphraser/c9db25d131dd4c09848ffb353b69038f)

## <a name="significantFiles"> Significant directories and files </a>

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

## <a name="howMosquittoIOTstackGetsBuilt"> How Mosquitto gets built for IOTstack </a>

### <a name="githubSourceCode"> Mosquitto source code ([*GitHub*](https://github.com)) </a>

The source code for Mosquitto lives at [*GitHub* eclipse/mosquitto](https://github.com/eclipse/mosquitto).

### <a name="dockerHubImages"> Mosquitto images ([*DockerHub*](https://hub.docker.com)) </a>

Periodically, the source code is recompiled and the resulting image is pushed to [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto?tab=tags&page=1&ordering=last_updated) on *DockerHub*.
 
### <a name="iotstackMenu"> IOTstack menu </a>

When you select Mosquitto in the IOTstack menu, the *template service definition* is copied into the *Compose* file.

> Under old menu, it is also copied to the *working service definition* and then not really used.

### <a name="iotstackFirstRun"> IOTstack first run </a>

On a first install of IOTstack, you run the menu, choose Mosquitto as one of your containers, and are told to do this:

```bash
$ cd ~/IOTstack
$ docker-compose up -d
```

> See also the [Migration considerations](#migration) (below).

`docker-compose` reads the *Compose* file. When it arrives at the `mosquitto` fragment, it finds:

```
  mosquitto:
    container_name: mosquitto
    build: ./.templates/mosquitto/.
    …
```

The `build` statement tells `docker-compose` to look for:

```
~/IOTstack/.templates/mosquitto/Dockerfile
```

> The *Dockerfile* is in the `.templates` directory because it is intended to be a common build for **all** IOTstack users. This is different to the arrangement for Node-RED where the *Dockerfile* is in the `services` directory because it is how each individual IOTstack user's version of Node-RED is customised.

The *Dockerfile* begins with:

```
FROM eclipse-mosquitto:latest
```

> If you need to pin to a particular version of Mosquitto, the *Dockerfile* is the place to do it. See [Mosquitto version pinning](#versionPinning).

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

When you run the `docker images` command after Mosquitto has been built, you will see two rows for Mosquitto:

```bash
$ docker images
REPOSITORY                      TAG         IMAGE ID       CREATED        SIZE
iotstack_mosquitto              latest      cf0bfe1a34d6   4 weeks ago    11.6MB
eclipse-mosquitto               latest      46ad1893f049   4 weeks ago    8.31MB
```

* `eclipse-mosquitto` is the *base image*; and
* `iotstack_mosquitto` is the *local image*.

You will see the same pattern in Portainer, which reports the *base image* as "unused". You should not remove the *base* image, even though it appears to be unused.

### <a name="migration"> Migration considerations </a>

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

```bash
$ cd ~/IOTstack
$ diff ./services/mosquitto/mosquitto.conf ./volumes/mosquitto/config/mosquitto.conf 
```

> You can also use the `-y` option on the `diff` command to see a side-by-side comparison of the two files.

Using `mosquitto.conf` as the example, assume you wish to use your existing file instead of the default:

1. To move your existing file into the new location:

	```bash
	$ cd ~/IOTstack
	$ sudo mv ./services/mosquitto/mosquitto.conf ./volumes/mosquitto/config/mosquitto.conf
	```
	
	> The move overwrites the default. At this point, the moved file will probably be owned by user "pi" but that does not matter.
	
2. Mosquitto will always enforce correct ownership (1883:1883) on any restart but it will not overwrite permissions. If in doubt, use mode 644 as your default for permissions:

	```bash
	$ sudo chmod 644 ./services/mosquitto/mosquitto.conf
	```

3. Restart Mosquitto:

	```bash
	$ docker-compose restart mosquitto
	```
	
4. Check your work:

	```bash
	$ ls -l ./volumes/mosquitto/config/mosquitto.conf
	-rw-r--r-- 1 1883 1883 ssss mmm dd hh:mm ./volumes/mosquitto/config/mosquitto.conf
	```

5. If necessary, repeat these steps with `filter.acl`.

## <a name="logging"> Logging </a>

Mosquitto logging is controlled by `mosquitto.conf`. This is the default configuration:

```
#log_dest file /mosquitto/log/mosquitto.log
log_dest stdout
log_timestamp_format %Y-%m-%dT%H:%M:%S
```

When `log_dest` is set to 	`stdout`, you inspect Mosquitto's logs like this:

```
$ docker logs mosquitto
```

Logs written to `stdout` are ephemeral and will disappear when your Mosquitto container is rebuilt, but this type of configuration reduces wear and tear on your SD card.

The alternative, which *may* be more appropriate if you are running on an SSD or HD, is to change `mosquitto.conf` to be like this:

```
log_dest file /mosquitto/log/mosquitto.log
#log_dest stdout
log_timestamp_format %Y-%m-%dT%H:%M:%S
```

and then restart Mosquitto:

```
$ cd ~/IOTstack
$ docker-compose restart mosquitto
```

The path `/mosquitto/log/mosquitto.log` is an **internal** path. When this style of logging is active, you inspect Mosquitto's logs using the **external** path like this:

```
$ sudo tail ~/IOTstack/volumes/mosquitto/log/mosquitto.log
```

> You need to use `sudo` because the log is owned by userID 1883 and Mosquitto creates it without "world" read permission.

Logs written to `mosquitto.log` do not disappear when your IOTstack is restarted. They persist until you take action to prune the file.

## <a name="security"> Security </a>

### <a name="securityConfiguration"> Configuring security </a>

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


### <a name="passwordManagement"> Password file management </a>

The password file for Mosquitto is part of a mapped volume:

* The **internal** path is `/mosquitto/pwfile/pwfile`
* The **external** path is `~/IOTstack/volumes/mosquitto/pwfile/pwfile`

A common problem with the previous version of Mosquitto for IOTstack occurred when the `password_file` directive was enabled but the `pwfile` was not present. Mosquitto went into a restart loop.

The Mosquitto container performs self-repair each time the container is brought up or restarts. If `pwfile` is missing, an empty file is created as a placeholder. This prevents the restart loop. What happens next depends on `allow_anonymous`:

* If `true` then:
	
	- Any MQTT request *without* credentials will be permitted;
	- Any MQTT request *with* credentials will be rejected (because `pwfile` is empty so there is nothing to match on).

* If `false` then **all** MQTT requests will be rejected.

#### <a name="passwordCreation"> create username and password </a>

To create a username and password, use the following as a template.
 
```
$ docker exec mosquitto mosquitto_passwd -b /mosquitto/pwfile/pwfile «username» «password» 
```
		
Replace «username» and «password» with appropriate values, then execute the command. For example, to create the username "hello" with password "world":
	
```
$ docker exec mosquitto mosquitto_passwd -b /mosquitto/pwfile/pwfile hello world
```
	
#### <a name="checkPasswordFile"> check password file </a>

There are two ways to verify that the password file exists and has the expected content:

1. View the file using its **external** path: 

	```bash
	$ sudo cat ~/IOTstack/volumes/mosquitto/pwfile/pwfile 
	```
	
	> `sudo` is needed because the file is neither owned nor readable by `pi`.

2. View the file using its **internal** path:

	```bash
	$ docker exec mosquitto cat /mosquitto/pwfile/pwfile
	```

Each credential starts with the username and occupies one line in the file: 

```
hello:$7$101$ZFOHHVJLp2bcgX+h$MdHsc4rfOAhmGG+65NpIEJkxY0beNeFUyfjNAGx1ILDmI498o4cVOaD9vDmXqlGUH9g6AgHki8RPDEgjWZMkDA==
```

#### <a name="deletePassword"> remove entry from password file </a>

To remove an entry from the password file:

```
$ docker exec mosquitto mosquitto_passwd -D /mosquitto/pwfile/pwfile «username»
```

#### <a name="resetPasswordFile"> reset the password file </a>

There are several ways to reset the password file. Your options are:

1. Remove the password file and restart Mosquitto:

	```bash
	$ cd ~/IOTstack
	$ sudo rm ./volumes/mosquitto/pwfile/pwfile
	$ docker-compose restart mosquitto 
	```
	
	The result is an empty password file.
	
2. Clear all existing passwords while adding a new password:

	```bash
	$ docker exec mosquitto mosquitto_passwd -c -b /mosquitto/pwfile/pwfile «username» «password»
	```
	
	The result is a password file with a single entry.
	
3. Clear all existing passwords in favour of a single dummy password which is then removed:

	```bash
	$ docker exec mosquitto mosquitto_passwd -c -b /mosquitto/pwfile/pwfile dummy dummy
	$ docker exec mosquitto mosquitto_passwd -D /mosquitto/pwfile/pwfile dummy
	```
	
	The result is an empty password file.

### <a name="activateSecurity"> Activate Mosquitto security </a>

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

	```bash
	$ cd ~/IOTstack
	$ docker-compose restart mosquitto
	```

### <a name="testSecurity"> Testing Mosquitto security </a>

#### <a name="testAssumptions"> assumptions </a>

1. You have created at least one username ("hello") and password ("world").
2. `password_file` is enabled.
3. `allow_anonymous` is `false`.

#### <a name="installTestTools"> install testing tools </a>

If you do not have the Mosquitto clients installed on your Raspberry Pi (ie `$ which mosquitto_pub` does not return a path), install them using:

```
$ sudo apt install -y mosquitto-clients
```

#### <a name="anonymousDenied"> test: *anonymous access is prohibited* </a>

Test **without** providing credentials:

```
$ mosquitto_pub -h 127.0.0.1 -p 1883 -t "/password/test" -m "up up and away"
Connection Refused: not authorised.
Error: The connection was refused.
```

Note:

* The error is the expected result and shows that Mosquitto will not allow anonymous access.

#### <a name="pubPermitted"> test: *access with credentials is permitted* </a>

Test with credentials

```
$ mosquitto_pub -h 127.0.0.1 -p 1883 -t "/password/test" -m "up up and away" -u hello -P world
$ 
```

Note:

* The absence of any error message means the message was sent. Silence = success!

#### <a name="pubSubPermitted"> test: *round-trip with credentials is permitted* </a>

Prove round-trip connectivity will succeed when credentials are provided. First, set up a subscriber as a background process. This mimics the role of a process like Node-Red:

```
$ mosquitto_sub -v -h 127.0.0.1 -p 1883 -t "/password/test" -F "%I %t %p" -u hello -P world &
[1] 25996
```

Repeat the earlier test:
	
```
$ mosquitto_pub -h 127.0.0.1 -p 1883 -t "/password/test" -m "up up and away" -u hello -P world
2021-02-16T14:40:51+1100 /password/test up up and away
```

Note:

* the second line above is coming from the `mosquitto_sub` running in the background.
	
When you have finished testing you can kill the background process (press return twice after you enter the `kill` command):

```
$ kill %1
$
[1]+  Terminated              mosquitto_sub -v -h 127.0.0.1 -p 1883 -t "/password/test" -F "%I %t %p" -u hello -P world
```

## <a name="upgradingMosquitto"> Upgrading Mosquitto </a>

You can update most containers like this:

```bash
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

```bash
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

The `prune` is the simplest way of cleaning up. The first call removes the old *local image*. The second call cleans up the old *base image*.

### <a name="versionPinning"> Mosquitto version pinning </a>

If you need to pin Mosquitto to a particular version:

1. Use your favourite text editor to open the following file:

	```
	~/IOTstack/.templates/mosquitto/Dockerfile
	```

2. Find the line:

	```
	FROM eclipse-mosquitto:latest
	```

3. Replace `latest` with the version you wish to pin to. For example, to pin to version 2.0.10:

	```
	FROM eclipse-mosquitto:2.0.10
	```

4. Save the file and tell `docker-compose` to rebuild the local image:

	```bash
	$ cd ~/IOTstack
	$ docker-compose up -d --build mosquitto
	$ docker system prune
	``` 

	The new *local image* is built, then the new container is instantiated based on that image. The `prune` deletes the old *local image*.
	
Note:

* As well as preventing Docker from updating the *base image*, pinning will also block incoming updates to the *Dockerfile* from a `git pull`. Nothing will change until you decide to remove the pin.

## <a name="aboutPort9001"> About Port 9001 </a>

Earlier versions of the IOTstack service definition for Mosquitto included two port mappings:

```
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

	```
	- "9001:9001"
	```

2. Inserting the additional listener in `mosquitto.conf`:

	```
	listener 1883
	listener 9001
	```
	
	You need **both** lines. If you omit 1883 then Mosquitto will stop listening to port 1883 and will only listen to port 9001.

3. Restarting the container:

	```
	$ cd ~/IOTstack
	$ docker-compose restart mosquitto
	```

Please consider raising an issue to document your use-case. If you think your use-case has general application then please also consider creating a pull request to make the changes permanent.
