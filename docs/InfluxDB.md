# InfluxDB
## References
- [Docker](https://hub.docker.com/_/influxdb)
- [Website](https://www.influxdata.com/)

## Security
The credentials and default database name for influxdb are stored in the file called influxdb/influx.env . The default username and password is set to "nodered" for both. It is HIGHLY recommended that you change them. The environment file contains several commented out options allowing you to set several access options such as default admin user credentials as well as the default database name. Any change to the environment file will require a restart of the service.

To access the terminal for influxdb execute `./services/influxdb/terminal.sh`. Here you can set additional parameters or create other databases.
