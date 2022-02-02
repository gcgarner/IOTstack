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

## References
- [Docker](https://hub.docker.com/_/influxdb)
- [Website](https://www.influxdata.com/)

## Setup

To access the influx console, show current databases and database measurements:
```
pi@raspberrypi:~/IOTstack $ docker-compose exec influxdb bash
root@6bca535a945f:/# influx
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
  increasing disk space usage. Depending on the file system used, new data may
  be written to the same flash blocks that were freed by expiration, wearing
  them out.
* Take care not to add measurements too often. If possible no more often than
  once a minute. Add all measurements in one operation.
* Adding measurements directly to Influxdb will cause a write on every
  operation. If your client code can't aggregate multiple measurements into one
  write, consider routing them via Telegraf. It has the
  `flush_interval`-option, which will combine the measurements into one write.
* All InfluxDB queries are logged by default and logs are written to the
  SD-card. To disable this, add to docker-compose.yml, next to the other
  INFLUXDB_\* entries:
  ```
      - INFLUXDB_DATA_QUERY_LOG_ENABLED=false
      - INFLUXDB_HTTP_LOG_ENABLED=false
  ```
  This is especially important if you plan on having Grafana or Chronograf
  displaying up-to-date data on a dashboard.

## Old-menu branch
The credentials and default database name for influxdb are stored in the file called influxdb/influx.env . The default username and password is set to "nodered" for both. It is HIGHLY recommended that you change them. The environment file contains several commented out options allowing you to set several access options such as default admin user credentials as well as the default database name. Any change to the environment file will require a restart of the service.

To access the terminal for influxdb execute `./services/influxdb/terminal.sh`. Here you can set additional parameters or create other databases.
