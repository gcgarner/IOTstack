# InfluxDB
A time series database.

InfluxDB has configurable aggregation and retention policies allowing
measurement resolution reduction, storing all added data points for recent data
and only aggregated values for older data.

To connect use:

| Field     | Default    |
| --------- | ---------- |
| User      | nodered    |
| Password  | nodered    |
| URL (from other services) | http://influxdb:8086   |
| URL (on the host machine) | http://localhost:8086   |

Open the CLI interactive shell by:

``` console
$ docker exec -it influxdb influx
```

## References
- [InfluxDB documentation](https://docs.influxdata.com/influxdb/v1.8/)
- [Using the InfluxDB image (Docker Hub)](https://hub.docker.com/_/influxdb)

## Configuration

Most
[settings](https://docs.influxdata.com/influxdb/v1.8/administration/config) can
be set using environment variables in `~IOTstack/docker-compose.yml`. These
will override settings in the configuration file.

For instance, if you plan on having lots of data or tags, to prevent influxdb
from using up all your RAM for indexes, add:
```yaml
    - INFLUXDB_DATA_INDEX_VERSION=tsi1
```

It's not recommended that you change the `influxdb.conf`-configuration file.
But if you absolutely need to, you should to export it as a persistent volume
(otherwise every update/recreate will undo your changes). To do this, edit
`docker-compose.yml` and under influxdb's `volumes:` add:

```yaml
    - ./volumes/influxdb/config:/etc/influxdb
```
And then recreate the container: `docker-compose up -d influxdb`

## Setup

To install helper alias `influx` that opens the influx console and displays
times as human-readable:

``` console
$ echo "alias iotstack_influx='docker-compose -f ~/IOTstack/docker-compose.yml \
    exec influxdb influx -precision=rfc3339'" >> ~/.profile
$ source ~/.profile
```

To access the influx console, show current databases and database measurements:
```
pi@raspberrypi:~ $ iotstack_influx
Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
> show databases
name: databases
name
----
_internal
telegraf
> use telegraf
Using database telegraf
> show measurements
name: measurements
name
----
cpu
cpu_temperature
disk
diskio
etc...
```

To create a new database and set a limited retention policy, here for instance
any data older than 52 weeks is deleted:

```
$ iotstack_influx
Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
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

Aggregation, on the other hand, is where you keep your relevant statistics, but
decrease their time-resolution and lose individual data-points. This is a much
more complicated topic and harder to configure. As such it is well outside the
scope of this guide.


## Reducing flash wear-out

SSD-drives have pretty good controllers spreading out writes, so this isn't a
this isn't really a concern for them.  But if you store data on a SD-card,
flash wear may cause the card to fail prematurely. Flash memory has a limited
number of erase-write cycles per physical block. These blocks may be multiple
megabytes. You can use `sudo lsblk -D` to see how big the erase granularity is
on your card. The goal is to avoid writing lots of small changes targeting the
same physical blocks. Here are some tips to mitigate SD-card wear:

* Don't use short retention policies. This may mask heavy disk IO without
  increasing disk space usage. Depending on the flash card and file system
  used, new data may be re-written to the same blocks that were freed by the
  expiration, wearing them out.
* Take care not to add measurements too often. If possible no more often than
  once a minute. Add all measurements in one operation. Even a small write
  will physically write a whole new block and erase the previously used block.
* Adding measurements directly to Influxdb will cause a write on every
  operation. If your client code can't aggregate multiple measurements into one
  write, consider routing them via Telegraf. It has the
  `flush_interval`-option, which will combine the measurements into one write.
* All InfluxDB queries are logged by default and logs are written to the
  SD-card. To disable this, add into docker-compose.yml, next to the other
  INFLUXDB_\* entries:
  ```yaml
      - INFLUXDB_DATA_QUERY_LOG_ENABLED=false
      - INFLUXDB_HTTP_LOG_ENABLED=false
  ```
  This is especially important if you plan on having Grafana or Chronograf
  displaying up-to-date data on a dashboard, making queries all the time.

## Maintanance when container refuses to start

Sometimes you need start the container without starting influxdb to access
its maintenance tools. Usually when influx crashes on startup.

Add a new line below `influxdb:` to your docker-compose.yml:
```yaml
  influxdb:
    entrypoint: sleep infinity
```

Recreate the container using the new entrypoint:
``` console
pi@raspberrypi:~/IOTstack $ docker-compose up -d influxdb
Recreating influxdb ... done
```

Now it should start and you can get a shell to poke around and try the
influx_inspect:
``` console
$ docker exec -it influxdb bash
root@5ecc8536174f:/# influx_inspect
Usage: influx_inspect [[command] [arguments]]
```
You may need to do `apt-get update` and `apt-get install` some tools you need.
The container is pretty bare-bones by default.

Of course remove the custom entrypoint and "up -d" again to test if your fixes
worked.

## Old-menu branch
The credentials and default database name for influxdb are stored in the file called influxdb/influx.env . The default username and password is set to "nodered" for both. It is HIGHLY recommended that you change them. The environment file contains several commented out options allowing you to set several access options such as default admin user credentials as well as the default database name. Any change to the environment file will require a restart of the service.

To access the terminal for influxdb execute `./services/influxdb/terminal.sh`. Here you can set additional parameters or create other databases.
