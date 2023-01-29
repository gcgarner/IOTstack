# InfluxDB

InfluxDB is a time series database. What that means is *time* is the primary key of each table.

Another feature of InfluxDB is the separation of *attributes* into:

* *fields:* which are intended to hold variable data (data that is likely to be different in each row, such as a temperature reading from a sensor); and
* *tags:* which are intended to hold metadata (data that is unlikely to be different in each row, such as the name of the sensor).

InfluxDB has configurable aggregation and retention policies allowing measurement resolution reduction, storing all added data points for recent data and only aggregated values for older data.

## References { #references }

- [DockerHub](https://hub.docker.com/_/influxdb/tags)
- [GitHub home page](https://github.com/influxdata/influxdata-docker) (for the container)
- [InfluxDB 1.8 documentation](https://docs.influxdata.com/influxdb/v1.8/)
- [InfluxDB 1.8 configuration reference](https://docs.influxdata.com/influxdb/v1.8/administration/config)

Note:

* 	IOTstack uses the `influxdb:1.8` image. Substituting the `:latest` tag will get you InfluxDB version 2 and *will* create a mess.

## Configuration { #configuration }

All InfluxDB [settings](https://docs.influxdata.com/influxdb/v1.8/administration/config) can be applied using environment variables. Environment variables override any settings in the [InfluxDB configuration file](#configFile):

* Under "new menu" (master branch), environment variables are stored inline in

	```
	~IOTstack/docker-compose.yml
	```

* Under "old menu", environment variables are stored in:

	```
	~/IOTstack/services/influxdb/influxdb.env
	```

Whenever you change an environment variable, you activate it like this:

``` console
$ cd ~/IOTstack
$ docker-compose up -d influxdb
```

The default service definition provided with IOTstack exposes the following environment variables:

- `TZ=Etc/UTC` set this to your local timezone. Do **not** use quote marks!
- `INFLUXDB_HTTP_FLUX_ENABLED=false` set this `true` if you wish to use Flux queries rather than InfluxQL:

	> At the time of writing, Grafana queries use InfluxQL.
	 
- `INFLUXDB_REPORTING_DISABLED=false` InfluxDB activates *phone-home* reporting by default. This variable disables it for IOTstack. You can activate it if you want your InfluxDB instance to send reports to the InfluxDB developers.
- `INFLUXDB_MONITOR_STORE_ENABLED=FALSE` disables automatic creation of the `_internal` database. This database stores metrics about InfluxDB itself. The database is *incredibly* busy. Side-effects of enabling this feature include increased wear and tear on SD cards and, occasionally, driving CPU utilisation through the roof and generally making your IOTstack unstable.

	> To state the problem in a nutshell: *do you want Influx self-metrics, or do you want a usable IOTstack?* You really can't have both. See also [issue 19543](https://github.com/influxdata/influxdb/issues/19543).

- Authentication variables:
 
	- `INFLUXDB_HTTP_AUTH_ENABLED=false`
	- `INFLUX_USERNAME=dba`
	- `INFLUX_PASSWORD=supremo`

	Misunderstanding the purpose and scope of these variables is a common mistake made by new users. Please do not guess! Please read [Authentication](#authentication) **before** you enable or change any of these variables. In particular, `dba` and `supremo` are **not** defaults for database access.

- UDP data acquisition variables:

	- `INFLUXDB_UDP_ENABLED=false`
	- `INFLUXDB_UDP_BIND_ADDRESS=0.0.0.0:8086`
	- `INFLUXDB_UDP_DATABASE=udp`

	Read [UDP support](#udpSupport) before making any decisions on these variables.

### about `influxdb.conf` { #configFile }

A lot of InfluxDB documentation and help material on the web refers to the `influxdb.conf` configuration file. Such instructions are only appropriate when InfluxDB is installed *natively*.

When InfluxDB runs in a *container*, changing `influxdb.conf` is neither necessary nor recommended. Anything that you can do with `influxdb.conf` can be done with environment variables.

However, if you believe that you have a use case that absolutely demands the use of `influxdb.conf` then you can set it up like this:

1. Make sure the InfluxDB container is running!
2. Execute the following commands:

	``` console
	$ cd ~/IOTstack
	$ docker cp influxdb:/etc/influxdb/influxdb.conf .
	```

3. Edit `docker-compose.yml`, find the `influxdb` service definition, and add the following line to the `volumes:` directive:

	``` yaml
	- ./volumes/influxdb/config:/etc/influxdb
	```

4. Execute the following commands:

	``` console
	$ docker-compose up -d influxdb
	$ sudo mv influxdb.conf ./volumes/influxdb/config/
	$ docker-compose restart influxdb
	```

At this point, you can start making changes to:

```
~/IOTstack/volumes/influxdb/config/influxdb.conf
```

You can apply changes by sending a `restart` to the container (as above). However, from time to time you may find that your settings disappear or revert to defaults. Make sure you keep good backups.

## Connecting to InfluxDB { #connecting }

By default, InfluxDB runs in non-host mode and respects the following port-mapping directive in its service definition:

``` yaml
ports:
  - "8086:8086"
```

If you are connecting from:

* another container (eg Node-RED or Grafana) that is also running in non-host mode, use:

	```
	http://influxdb:8086
	```

	In this context, `8086` is the *internal* (right hand side) port number.

* either the Raspberry Pi itself or from another container running in host mode, use:

	```
	http://localhost:8086
	```
 
	In this context, `8086` is the *external* (left hand side) port number.

* a different host, you use either the IP address of the Raspberry Pi or its fully-qualified domain name. Examples:

	```
	http://192.168.1.10:8086
	http://raspberrypi.local:8086
	http://iot-hub.mydomain.com:8086
	```

	In this context, `8086` is the *external* (left hand side) port number.

## Interacting with the Influx CLI { #influxCLI }

You can open the `influx` CLI interactive shell by:

``` console
$ docker exec -it influxdb influx
Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
>
```

The command prompt in the CLI is `>`. While in the CLI you can type commands such as:

``` console
> help
> create database MYTESTDATABASE
> show databases
> USE MYTESTDATABASE
> show measurements
> show series
> select * from «someMeasurement» where «someCriterion»
```

You may also wish to set retention policies on your databases. This is an example of creating a database named "mydb" where any data older than 52 weeks is deleted:

``` console
> create database mydb

> show retention policies on mydb
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        true

> alter retention policy "autogen" on "mydb" duration 52w shard duration 1w replication 1 default

> show retention policies on mydb
name    duration  shardGroupDuration replicaN default
----    --------  ------------------ -------- -------
autogen 8736h0m0s 168h0m0s           1        true
```

To exit the CLI, either press <kbd>Control</kbd>+<kbd>d</kbd> or type:

``` console
> exit
$
```

### useful alias { #usefulAlias }

Consider adding the following alias to your `.bashrc`:

``` console
alias influx='docker exec -it influxdb influx -precision=rfc3339'
```

With that alias installed, typing `influx` and pressing <kbd>return</kbd>, gets you straight into the influx CLI. The `-precision` argument tells the influx CLI to display dates in human-readable form. Omitting that argument displays dates as integer nanoseconds since 1970-01-01.

Note:

* This alias is installed by [IOTstackAliases](https://github.com/Paraphraser/IOTstackAliases).

## Authentication { #authentication }

### warning { #authWarning }

This tutorial also assumes that you do not have any existing databases so it starts by creating two. One database will be provided with access controls but the other will be left alone so that the behaviour can be compared.

However, you need to understand that enabling authentication in InfluxDB is *all-or-nothing*. If you have any existing InfluxDB databases, you will need to:

* define access rights for **all** of your databases; and
* provide credentials to processes like Node-Red and Grafana that access your databases.

If you do not do this, your existing Node-Red flows, Grafana dashboards and other processes that write to or query your databases will stop working as soon as you [activate authentication](#authStep4) below.

### create two test databases { #authStep1 }

Create two databases named "mydatabase1" and "mydatabase2":

``` console
$ influx
> CREATE DATABASE "mydatabase1"
> CREATE DATABASE "mydatabase2"
```

> Typing `influx` didn't work? See [useful alias](#usefulAlias) above. 

### define users { #authStep2 }

Define an administrative user. In this example, that user is "dba" (database administrator) with the password "supremo":

``` console
> CREATE USER "dba" WITH PASSWORD 'supremo' WITH ALL PRIVILEGES
```

* Key point: the mixture of "double" and 'single' quotes is **intentional** and **required**.

Define some garden-variety users:

``` console
> CREATE USER "nodered_user" WITH PASSWORD 'nodered_user_pw'
> CREATE USER "grafana_user" WITH PASSWORD 'grafana_user_pw'
```

You can define any usernames you like. The reason for using "nodered\_" and "grafana\_" prefixes in these examples is because those are common candidates in an IOTstack environment. The reason for the "\_user" suffixes is to make it clear that a *username* is separate and distinct from a *container* name.

### assign access rights { #authStep3 }

The user "dba" already has access to everything but, for all other users, you need to state which database(s) the user can access, and whether that access is:

* READ (aka read-only)
* WRITE (aka write-only)
* ALL (implies both READ and WRITE)

``` console
> GRANT WRITE ON "mydatabase1" TO "nodered_user"
> GRANT READ ON "mydatabase1" TO "grafana_user"
```

* Key point: you CREATE a user *once* but you need to GRANT access to every database to which that user needs access.

Once you have finished defining users and assigning access rights, drop out of the influx CLI:

``` console
> exit
$
```

### activate authentication { #authStep4 }

Make sure you read the [warning](#authWarning) above, then edit the InfluxDB environment variables to enable this key:

``` yaml
- INFLUXDB_HTTP_AUTH_ENABLED=true
```

Put the change into effect by "upping" the container:

``` console
$ cd ~/IOTstack
$ docker-compose up -d influxdb

Recreating influxdb ... done
```

The `up` causes `docker-compose` to notice that the environment has changed, and to rebuild the container with the new settings.

* Note: You should always wait for 30 seconds after a rebuild for InfluxDB to become available. Any time you see a message like this:

	```
	Failed to connect to http://localhost:8086: Get http://localhost:8086/ping: dial tcp 127.0.0.1:8086: connect: connection refused
	Please check your connection settings and ensure 'influxd' is running.
	```

	it simply means that you did not wait long enough. Be patient!

### experiments { #authStep5 }

Start the influx CLI:

``` console
$ influx
```

Unless you have also set up the `INFLUX_USERNAME` and `INFLUX_PASSWORD` environment variables (described later under [Authentication Hints](#authHints)), your session will not be authenticated as any user so you will not be able to access either database:

``` console
> USE mydatabase1
ERR: unable to parse authentication credentials
DB does not exist!
> USE mydatabase2
ERR: unable to parse authentication credentials
DB does not exist!
```

* Key point: This is what will happen to any of your pre-existing databases if you enable authentication without a lot of care. You **must** define users and access rights for **all** of your databases, and you **must** provide those credentials to the relevant processes like Node-Red and Grafana.

Authenticate as "nodered_user" and try again:

``` console
> AUTH
username: nodered_user
password: 
> USE mydatabase1
Using database mydatabase1
> USE mydatabase2
ERR: Database mydatabase2 doesn't exist. Run SHOW DATABASES for a list of existing databases.
DB does not exist!
```

The "nodered_user" can access "mydatabase1" but not "mydatabase2". You will get similar behaviour for the "grafana_user" (try it).

Authenticate as the "dba" and try again:

``` console
> AUTH
username: dba
password: 
> USE mydatabase1
Using database mydatabase1
> USE mydatabase2
Using database mydatabase2
```

The super-user can access both databases.

To get a list of users:

``` console
> SHOW USERS
user         admin
----         -----
dba          true
nodered_user false
grafana_user false
```

* Key point: you must be authenticated as the "dba" to run SHOW USERS.

To find out what privileges a user has on a database:

``` console
> SHOW GRANTS FOR "nodered_user"
database    privilege
--------    ---------
mydatabase1 WRITE
```

* Key point: you must be authenticated as the "dba" to run SHOW GRANTS.

To test grants, you can try things like this:

``` console
AUTH
username: nodered_user
password: 
> USE "mydatabase1"
Using database mydatabase1
> INSERT example somefield=123
```

"nodered_user" has WRITE access to "mydatabase1".

``` console
> SELECT * FROM example
ERR: error authorizing query: nodered_user not authorized to execute statement 'SELECT * FROM example', requires READ on mydatabase1
```

"nodered_user" does not have READ access to "mydatabase1".

Authenticate as "grafana_user" and try the query again:

``` console
> AUTH
username: grafana_user
password: 
> SELECT * FROM example
name: example
time                         somefield
----                         ---------
2020-09-19T01:41:09.6390883Z 123
```

"grafana_user" has READ access to "mydatabase1". Try an insertion as "grafana_user":

``` console
> INSERT example somefield=456
ERR: {"error":"\"grafana_user\" user is not authorized to write to database \"mydatabase1\""}
```

"grafana_user" does not have WRITE access to "mydatabase1".

Change the privileges for "nodered_user" to ALL then try both an insertion and a query. Note that changing privileges requires first authenticating as "dba":

``` console
> AUTH
username: dba
password: 
> GRANT ALL ON "mydatabase1" TO "nodered_user"
> AUTH
username: nodered_user
password: 
> INSERT example somefield=456
> SELECT * FROM example
name: example
time                          somefield
----                          ---------
2020-09-19T01:41:09.6390883Z  123
2020-09-19T01:42:36.85766382Z 456
```

"nodered_user" has both READ and WRITE access to "mydatabase1".

### notes { #authNotes }

1. Some inferences to draw from the above:

	* user definitions are **global** rather than per-database. Grants are what tie users to particular databases.
	* setting `INFLUXDB_HTTP_AUTH_ENABLED=true` is how authentication is activated and enforced. If it is false, all enforcement goes away (a handy thing to know if you lose passwords or need to recover from a mess).
	* as the "HTTP" in `INFLUXDB_HTTP_AUTH_ENABLED` suggests, it applies to access via HTTP. This includes the influx CLI and processes like Node-Red and Grafana.

2. Always keep in mind that the InfluxDB log is your friend:

	``` console
	$ docker logs influxdb
	```

### hints { #authHints }

After you enable authentication, there are a couple of ways of speeding-up your daily activities. You can pass the dba username and password on the end of the influx alias:

``` console
$ influx -database mydatabase1 -username dba -password supremo
```

but this is probably sub-optimal because of the temptation to hard-code your dba password into scripts. An alternative is to enable these environment variables:

``` yaml
- INFLUX_USERNAME=dba
- INFLUX_PASSWORD=supremo
```

and then "up" the container as explained above to apply the changes.

Misunderstandings about the scope and purpose of `INFLUX_USERNAME` and `INFLUX_PASSWORD` are quite common so make sure you realise that the variables:

* do **not** "set" any username or password within InfluxDB;
* **only** apply to starting the influx CLI&nbsp;–&nbsp;they are just synonyms for the `-username` and `-password` parameters on the `influx` CLI command; and
* are **not** some kind of general-access credentials that apply to everything. They will not work from Node-RED or Grafana!

In other words, with `INFLUX_USERNAME` and `INFLUX_PASSWORD` added to the environment, the following two commands are identical:

``` console
$ influx -database mydatabase1 -username dba -password supremo
$ influx -database mydatabase1
```

The `INFLUX_USERNAME` and `INFLUX_PASSWORD` variables also work if you start a shell into the InfluxDB container and then invoke the influx CLI from there:

``` console
$ docker exec -it influxdb bash
# influx
>
```

That is **all** the `INFLUX_USERNAME` and `INFLUX_PASSWORD` variables do.

### cleaning up { #authCleanup }

To undo the steps in this tutorial, first set `INFLUXDB_HTTP_AUTH_ENABLED=false` and then "up" influxdb. Then:

``` console
$ influx
> DROP USER "dba"
> DROP USER "nodered_user"
> DROP USER "grafana_user"
> DROP DATABASE "mydatabase1"
> DROP DATABASE "mydatabase2"
> exit
```

## UDP support { #udpSupport }

Assumptions:

* you want to enable UDP support; and
* your goal is to log traffic arriving on UDP port 8086 into an InfluxDB database named "udp".

### aliases { #udpAliases }

This tutorial uses the following aliases:

* `influx` - explained earlier - see [useful alias](#usefulAlias).
* `DPS` which is the equivalent of:

	``` console
	$ docker ps --format "table {{.Names}}\t{{.RunningFor}}\t{{.Status}}"
	```

	The focus is: *what containers are running?*

* `DNET` which is the equivalent of:

	``` console
	$ docker ps --format "table {{.Names}}\t{{.Ports}}"
	```

	The focus is: *what ports are containers using?*
	
	> Any container where no ports are listed is either exposing no ports and/or is running in host mode.

Although both `DPS` & `DNET` invoke `docker ps`, the formatting means the output usually fits on your screen without line wrapping.

All three aliases are installed by [IOTstackAliases](https://github.com/Paraphraser/IOTstackAliases).

### confirm that UDP is not enabled  { #udpStep1 }

``` console
$ DNET
NAMES      PORTS
influxdb   0.0.0.0:8086->8086/tcp
```

Interpretation: Docker is listening on TCP port 8086, and is routing the traffic to the same port on the influxdb container. There is no mention of UDP.

### create a database to receive the traffic  { #udpStep2 }

This tutorial uses the database name of "udp".

``` console
$ influx
> create database udp
> exit
> $
```

### define a UDP port mapping  { #udpStep3 }

Edit `docker-compose.yml` to define a UDP port mapping (the second line in the `ports` grouping below):

``` yaml
influxdb:
  …
  ports:
    - "8086:8086"
    - "8086:8086/udp"
  …
```

### enable UDP support  { #udpStep4 }

Edit your `docker-compose.yml` and change the InfluxDB environment variables to glue it all together:

``` yaml
environment:
  - INFLUXDB_UDP_DATABASE=udp
  - INFLUXDB_UDP_ENABLED=true
  - INFLUXDB_UDP_BIND_ADDRESS=0.0.0.0:8086
```

In this context, the IP address "0.0.0.0" means "this host" (analogous to the way "255.255.255.255" means "all hosts").

### rebuild the container  { #udpStep5 }

``` console
$ cd ~/IOTstack
$ docker-compose up -d influxdb

Recreating influxdb ... done
```

The `up` causes `docker-compose` to notice that the environment has changed, and to rebuild the container with the new settings.

### confirm that UDP is enabled  { #udpStep6 }

``` console
$ DNET
NAMES      PORTS
influxdb   0.0.0.0:8086->8086/tcp, 0.0.0.0:8086->8086/udp
```

Interpretation: In addition to the TCP port, Docker is now listening on UDP port 8086, and is routing the traffic to the same port on the influxdb container.

### check your work  { #udpStep7 }

Check the log: 

``` console
$ docker logs influxdb
```

If you see a line like this:

```
ts=2020-09-18T03:09:26.154478Z lvl=info msg="Started listening on UDP" log_id=0PJnqbK0000 service=udp addr=0.0.0.0:8086
```

then everything is probably working correctly. If you see anything that looks like an error message then you will need to follow your nose.

### start sending traffic  { #udpStep8 }

Although the how-to is beyond the scope of this tutorial, you will need a process that can send "line format" payloads to InfluxDB using UDP port 8086.

Once that is set up, you can inspect the results like this:

``` console
$ influx -database udp
> show measurements
```

If data is being received, you will get at least one measurement name. An empty list implies no data is being received.

If you get at least one measurement name then you can inspect the data using:

``` console
> select * from «measurement»
```

where `«measurement»` is one of the names in the `show measurements` list.

## Reducing flash wear-out { #flashWear }

SSD-drives have pretty good controllers spreading out writes, so this isn't a this isn't really a concern for them.  But if you store data on an SD-card, flash wear may cause the card to fail prematurely. Flash memory has a limited number of erase-write cycles per physical block. These blocks may be multiple megabytes. You can use `sudo lsblk -D` to see how big the erase granularity is on your card. The goal is to avoid writing lots of small changes targeting the same physical blocks. Here are some tips to mitigate SD-card wear:

* Don't use short retention policies. This may mask heavy disk IO without increasing disk space usage. Depending on the flash card and file system used, new data may be re-written to the same blocks that were freed by the expiration, wearing them out.
* Take care not to add measurements too often. If possible no more often than once a minute. Add all measurements in one operation. Even a small write will physically write a whole new block and erase the previously used block.
* Adding measurements directly to Influxdb will cause a write on every operation. If your client code can't aggregate multiple measurements into one write, consider routing them via Telegraf. It has the `flush_interval`-option, which will combine the measurements into one write.
* All InfluxDB queries are logged by default and logs are written to the SD-card. To disable this, add into docker-compose.yml, next to the other INFLUXDB_\* entries:

  ```yaml
      - INFLUXDB_DATA_QUERY_LOG_ENABLED=false
      - INFLUXDB_HTTP_LOG_ENABLED=false
  ```

  This is especially important if you plan on having Grafana or Chronograf displaying up-to-date data on a dashboard, making queries all the time.

### Debugging { #debugging }

### Container won't start { #debugInspection }

Sometimes you need start the container without starting influxdb to access its maintenance tools. Usually when influx crashes on startup.

Add a new line below `influxdb:` to your docker-compose.yml:

```yaml
influxdb:
  …
  entrypoint: sleep infinity
```

Recreate the container using the new entrypoint:

``` console
$ docker-compose up -d influxdb
Recreating influxdb ... done
```

Now the container should start and you can get a shell to poke around and try the `influx_inspect` command:

``` console
$ docker exec -it influxdb bash
# influx_inspect
Usage: influx_inspect [[command] [arguments]]
```

Once you have finished poking around, you should undo the change by removing the custom entrypoint and `up -d` again to return to normal container behaviour where you can then test to see if your fixes worked.

### Adding packages { #debugPackages }

The container is pretty bare-bones by default. It is OK to install additional tools. Start by running:

``` console
# apt update
```

and then use `apt install` to add whatever you need. Packages you add will persist until the next time the container is re-created.  

### Sniffing traffic { #debugSniff }

If you need to see the actual packets being sent to Influx for insertion into your database, you can set it up like this:

``` console
$ docker exec influxdb bash -c 'apt update && apt install tcpdump -y'
```

That adds `tcpdump` to the running container and, as noted above, that will persist until you re-create the container.

To capture traffic:

``` console
$ docker exec influxdb tcpdump -i eth0 -s 0 -n -c 100 -w /var/lib/influxdb/capture.pcap dst port 8086
```

Breaking that down:

* `-i eth0` is the container's internal virtual Ethernet network interface (attached to the internal bridged network)
* `-s 0` means "capture entire packets"
* `-n` means "do not try to resolve IP addresses to domain names
* `-c 100` is optional and means "capture 100 packets then stop". If you omit this option, `tcpdump` will capture packets until you press <kbd>control</kbd>+<kbd>C</kbd>.
* `-w /var/lib/influxdb/capture.pcap` is the internal path to the file where captured packets are written. You can, of course, substitute any filename you like for `capture.pcap`.
* `dst port 8086` captures all packets where the destination port field is 8086, which is the InfluxDB internal port number.

The internal path:

```
/var/lib/influxdb/capture.pcap
```

maps to the external path:

```
~/IOTstack/volumes/influxdb/data/capture.pcap
```

You can copy that file to another system where you have a tool like WireShark installed. WireShark will open the file and you can inspect packets and verify that the information being sent to InfluxDB is what you expect.

Do not forget to clean-up any packet capture files:

```
$ cd ~/IOTstack/volumes/influxdb/data
$ sudo rm capture.pcap
```
