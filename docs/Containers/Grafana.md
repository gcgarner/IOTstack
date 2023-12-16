# Grafana

## References

- [Docker](https://hub.docker.com/r/grafana/grafana)
- [Website](https://grafana.com/)

## Adding InfluxDB datasource

When you have logged into Grafana (default user/pass: admin/admin), you have
to add a data source to be used for the graphs.

Select `Data Sources` -> `Add data source` -> `InfluxDB`.

Set options:

* HTTP / URL: `http://influxdb:8086`
* InfluxDB Details / Database: `telegraf`
* InfluxDB Details / User: `nodered`
* InfluxDB Details / Password: `nodered`

## Overriding configuration variables

Grafana documentation contains [a list of
settings](https://grafana.com/docs/grafana/latest/administration/configuration/).
Settings are described in terms of how they appear in ".ini" files.

Grafana configuration is usually done in *grafana.ini*, but when used via
docker as the IOTstack does, it should be configured using [environment
variables](https://grafana.com/docs/grafana/latest/administration/configuration/#override-configuration-with-environment-variables).

Edit `docker-compose.yml` and find `grafana:` and under it
`environment:` this is where you can place the ini-options, but formatted as:
```yaml
    - GF_<SectionName>_<KeyName>=<value>
```
If you are using old-menu edit `~/IOTstack/services/grafana/grafana.env`
instead and add the lines directly there, but without the leading dash:
`GF_<SectionName>_<KeyName>=<value>`

For any changes to take effect you need recreate the Grafana container:

``` console
$ docker-compose up -d grafana
```

### Setting your time-zone

Change the right hand side to [your own
timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones):

```yaml
    - TZ=Etc/UTC
```

### Anonymous login

To allow anonymous logins add:

```yaml
    - GF_AUTH_ANONYMOUS_ENABLED=true
```

### Custom admin user and password (not recommended)

If you do not change anything then, when you bring up the stack and use a browser to connect to your Raspberry Pi on port 3000, Grafana will:

* Expect you to login as user "admin" with password "admin"; and then
* Force you to change the default password to something else.

Thereafter, you will login as "admin" with whatever password you chose. You can change the administrator's password as often as you like via the web UI (*profile* button, *change password* tab).

This default operation can be changed by configuration options.  They will have
any effect only if Grafana has just been added to the stack, but has **never**
been launched. Thus, if the folder *~/IOTstack/volumes/grafana* exists, Grafana
has already been started, and adding and changing these options **will not**
have any effect.

To customize, editing the file as describe above, add the following lines under
the `environment:` clause. For example, to set the administrative username to be "maestro" with password "123456":

```yaml
    - GF_SECURITY_ADMIN_USER=maestro
    - GF_SECURITY_ADMIN_PASSWORD=123456
```

If you change the default password, Grafana will not force you to change the
password on first login but you will still be able to change it via the web UI.

As a summary, the environment variables only take effect if you set them up **before** Grafana is launched for the first time:

* `GF_SECURITY_ADMIN_USER` has a default value of "admin". You *can* explicitly set it to "admin" or some other value. Whatever option you choose then that's the account name of Grafana's administrative user. But choosing any value other than "admin" is probably a bad idea.
* `GF_SECURITY_ADMIN_PASSWORD` has a default value of "admin". You can explicitly set it to "admin" or some other value. If its value is "admin" then you will be forced to change it the first time you login to Grafana. If its value is something other than "admin" then that will be the password until you change it via the web UI.

### Options with spaces

To set an options with a space, you must enclose the whole value in quotes:

```yaml
    - "GF_AUTH_ANONYMOUS_ORG_NAME=Main Org."
```

## HELP – I forgot my Grafana admin password!

Assuming Grafana is started, run:

```
$ docker exec grafana grafana cli admin reset-admin-password «NEWPASSWORD»
```

where `«NEWPASSWORD»` is the value of your choice.

Note:

* If you have customized `GF_SECURITY_ADMIN_USER` to be something other than "admin", the password change will be applied to that username. In other words, in the `docker exec` command above, the two references to "admin" are referring to the administrator's account, not the username of the administrator's account. Run the command "as is". Do **not** replace "admin" with the username of the administrator's account.

## HELP - Resetting to a clean slate

"I made a bit of a mess with Grafana. First time user. Steep learning curve. False starts, many. Mistakes, unavoidable. Been there, done that. But now I **really** need to start from a clean slate. And, yes, I understand there is no *undo* for this."

Begin by stopping Grafana:

``` console
$ cd ~/IOTstack
$ docker-compose down grafana
```

> see also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)

You have two options:

1. Destroy your settings and dashboards but retain any plugins you may have installed:

	``` console
	$ sudo rm ~/IOTstack/volumes/grafana/data/grafana.db
	```

2. Nuke everything (triple-check this command **before** you hit return):

	``` console
	$ sudo rm -rf ~/IOTstack/volumes/grafana/data
	```

This is where you should edit *docker-compose.yml* or
*~/IOTstack/services/grafana/grafana.env* to correct any problems (such as
choosing an administrative username other than "admin").

When you are ready, bring Grafana back up again:

``` console
$ cd ~/IOTstack
$ docker-compose up -d grafana
```

Grafana will automatically recreate everything it needs. You will be able to login as "admin/admin" (or the credentials you set using `GF_SECURITY_ADMIN_USER` and `GF_SECURITY_ADMIN_PASSWORD`).

