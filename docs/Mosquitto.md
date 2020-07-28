# Mosquitto

## References
- [Docker](https://hub.docker.com/_/eclipse-mosquitto)
- [Website](https://mosquitto.org/)
- [mosquitto.conf](https://mosquitto.org/man/mosquitto-conf-5.html) documentation
- [Setting up passwords](https://www.youtube.com/watch?v=1msiFQT_flo) video

## Definitions

- `docker-compose.yml` ⇒ ~/IOTstack/docker-compose.yml
- `mosquitto.conf` ⇒ ~/IOTstack/services/mosquitto/mosquitto.conf
- `mosquitto.log` ⇒ ~/IOTstack/volumes/mosquitto/log/mosquitto.log
- `service.yml` ⇒ ~/IOTstack/.templates/mosquitto/service.yml
- `volumes/mosquitto` ⇒ ~/IOTstack/volumes/mosquitto/

## Logging

Mosquitto logging is controlled by `mosquitto.conf`. This is the default configuration:

```
#log_dest file /mosquitto/log/mosquitto.log
# To avoid flash wearing
log_dest stdout
```

When `log_dest` is set to 	`stdout`, you inspect Mosquitto's logs like this:

```
$ docker logs mosquitto
```

Logs written to `stdout` are ephemeral and will disappear when your IOTstack is restarted but this configuration reduces wear and tear on your SD card.

The alternative, which *may* be more appropriate if you are running on an SSD or HD, is to change `mosquitto.conf` to be like this:

```
log_dest file /mosquitto/log/mosquitto.log
# To avoid flash wearing
#log_dest stdout
```

and then restart Mosquitto:

```
$ cd ~/IOTstack
$ docker-compose restart mosquitto
```

With this configuration, you inspect Mosquitto's logs like this:

```
$ tail ~/IOTstack/volumes/mosquitto/log/mosquitto.log
```

Logs written to `mosquitto.log` do not disappear when your IOTstack is restarted. They persist until you take action to prune the file.

## Security

By default, the Mosquitto container has no password. You can leave it that way if you like but it's always a good idea to secure your services.

Assuming your IOTstack is running:

1. Open a shell in the mosquitto container:

	```
	$ docker exec -it mosquitto sh
	```

2. In the following, replace «MYUSER» with the username you want to use for controlling access to Mosquitto and then run these commands:

	```
	$ mosquitto_passwd -c /mosquitto/pwfile/pwfile «MYUSER»
	$ exit
	```

	`mosquitto_passwd` will ask you to type a password and confirm it.
	
	The path on the right hand side of:
	
	```
	-c /mosquitto/pwfile/pwfile
	```
	
	is **inside** the container. **Outside** the container, it maps to:
	
	```
	~/IOTstack/volumes/mosquitto/pwfile/pwfile
	```
	
	You should be able to see the result of setting a username and password like this:
	
	```
	$ cat ~/IOTstack/volumes/mosquitto/pwfile/pwfile
	MYUSER:$6$lBYlxjWtLON0fm96$3qgcEyr/nKvxk3C2Jk36kkILJK7nLdIeLhuywVOVkVbJUjBeqUmCLOA/T6qAq2+hyyJdZ52ALTi+onMEEaM0qQ==
	$
	```

3. Open `mosquitto.conf` in a text editor. Find this line:

	```
	#password_file /mosquitto/pwfile/pwfile
	```

	Remove the # in front of password_file. Save.
	
4. Restart Mosquitto:

	```
	$ cd ~/IOTstack
	$ docker-compose restart mosquitto
	```

5. Use the new credentials where necessary (eg Node-Red).

Notes:

* You can revert to password-disabled state by going back to step 3, re-inserting the "#", then restarting Mosquitto as per step 4.
* If mosquitto keeps restarting after you implement password checking, the most likely explanation will be something wrong with the password file. Implement the advice in the previous note.
 
## Running as root

By default, the Mosquitto container is launched as root but then downgrades its privileges to run as user ID 1883.

Mosquitto is unusual because most containers just accept the privileges they were launched with. In most cases, that means containers run as root.

> <small>Don't make the mistake of thinking this means that processes running **inside** containers can do whatever they like to your host system. A process inside a container is **contained**. What a process can affect **outside** its container is governed by the port, device and volume mappings you see in the `docker-compose.yml`.</small>

You can check how mosquitto has been launched like this:

```
$ ps -eo euser,ruser,suser,fuser,comm | grep mosquitto
EUSER    RUSER    SUSER    FUSER    COMMAND
1883     1883     1883     1883     mosquitto
```

If you have a use-case that needs Mosquitto to run with root privileges:

1. Open `docker-compose.yml` in a text editor and find this:

	```
	  mosquitto:
	    … [snip] …
	    user: "1883"
	```
	
	change it to:

	```
	  mosquitto:
	    … [snip] …
	    user: "0"
	```

2. Edit `mosquitto.conf` to add this line:

	```
	user root
	```

3. Apply the change:

	```
	$ cd ~/IOTstack
	$ docker-compose stop mosquitto
	$ docker-compose up -d
	```
	
> <small>A clean install of Mosquitto via the IOTstack menu sets everything in `volumes/mosquitto` to user and group 1883. That permission structure will still work if you change Mosquitto to run with root privileges. However, running as root **may** have the side effect of changing privilege levels within `volumes/mosquitto`. Keep this in mind if you decide to switch back to running Mosquitto as user 1883 because it is less likely to work.</small>

## Port 9001

In earlier versions of IOTstack, `service.yml` included two port mappings which were included in `docker-compose.yml` when Mosquitto was chosen in the menu:

```
    ports:
      - "1883:1883"
      - "9001:9001"
```

[Issue 67](https://github.com/SensorsIot/IOTstack/issues/67) explored the topic of port 9001 and showed that:

* The base image for mosquitto did not expose port 9001; and
* The running container was not listening to port 9001.

On that basis, the mapping for port 9001 was removed from `service.yml`.

If you have a use-case that needs port 9001, you can re-enable support by:

1. Inserting the port mapping under the `mosquitto` definition in `docker-compose.yml`:

	```
	       - "9001:9001"
	```

2. Inserting the following lines in `mosquitto.conf`:

	```
	listener 1883
	listener 9001
	```
	
	You need **both** lines. If you omit 1883 then mosquitto will stop listening to port 1883 and will only listen to port 9001.

3. Restarting the container:

	```
	$ cd ~/IOTstack
	$ docker-compose up -d
	```

Please consider raising an issue to document your use-case. If you think your use-case has general application then please also consider creating a pull request to make the changes permanent.
