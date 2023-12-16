# Prometheus

## References { #references }

* [*Prometheus* home](https://prometheus.io)
* *GitHub*:

	- [*Prometheus*](https://github.com/prometheus/prometheus)
	- [*CAdvisor*](https://github.com/google/cadvisor)
	- [*Node Exporter*](https://github.com/prometheus/node_exporter)

* *DockerHub*:

	- [*Prometheus*](https://hub.docker.com/r/prom/prometheus)
	- [*CAdvisor*](https://hub.docker.com/r/zcube/cadvisor)
	- [*Node Exporter*](https://hub.docker.com/r/prom/node-exporter)


## Special note 2022-11-08 { #configUpdate }

[Issue 620](https://github.com/SensorsIot/IOTstack/issues/620) pointed out there was an error in the default configuration file. That has been fixed. To adopt it, please do the following:

1. If Prometheus and/or any of its associated containers are running, take them down:

	```
	$ cd ~/IOTstack
	$ docker-compose down prometheus prometheus-cadvisor prometheus-nodeexporter
	```
	
	> see also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)

2. Move the existing active configuration out of the way:

	```
	$ cd ~/IOTstack/volumes/prometheus/data/config
	$ mv config.yml config.yml.old
	```

3. Make sure that the service definitions in your `docker-compose.yml` are up-to-date by comparing them with the template versions:

	- `~/IOTstack/.templates/prometheus/service.yml`
	- `~/IOTstack/.templates/prometheus-cadvisor/service.yml`
	- `~/IOTstack/.templates/prometheus-nodeexporter/service.yml`

	Your service definitions and those in the templates do not need to be *identical*, but you should be able to explain any differences.

4. Rebuild your Prometheus container by following the instructions in [Upgrading *Prometheus*](#upgradingPrometheus). Rebuilding will import the updated *default* configuration into the container's image.

5. Start the service:

	```
	$ cd ~/IOTstack
	$ docker-compose up -d prometheus
	```

	Starting `prometheus` should start `prometheus-cadvisor` and `prometheus-nodeexporter` automatically. Because the old configuration has been moved out of the way, the container will supply a new version as a default.

6. Compare the configurations:

	```
	$ cd ~/IOTstack/volumes/prometheus/data/config
	$ diff -y config.yml.old config.yml
	global:                          global:
	  scrape_interval: 10s             scrape_interval: 10s
	  evaluation_interval: 10s         evaluation_interval: 10s

	scrape_configs:                  scrape_configs:
	  - job_name: "iotstack"           - job_name: "iotstack"
	    static_configs:                  static_configs:
	      - targets:                       - targets:
	        - localhost:9090                 - localhost:9090
	        - cadvisor:8080        |         - prometheus-cadvisor:8080
	        - nodeexporter:9100    |         - prometheus-nodeexporter:9100
	```

	In the output above, the vertical bars (`|`) in the last two lines indicate that those lines have changed. The "old" version is on the left, "new" on the right.

	If you have made other alterations to your config then you should see other change indicators including `<`, `|` and `>`. If so, you should hand-merge your own changes from `config.yml.old` into `config.yml` and then restart the container:

	```
	$ cd ~/IOTstack
	$ docker-compose restart prometheus
	```

## Overview { #overview }

Prometheus is a collection of three containers:

* *Prometheus*
* *CAdvisor*
* *Node Exporter*

The [default configuration](#activeConfig) for *Prometheus* supplied with IOTstack scrapes information from all three containers.

## Installing Prometheus { #installProm }

### *if you are running New Menu …* { #installPromNewMenu }

When you select *Prometheus* in the IOTstack menu, you must also select:

*	*prometheus-cadvisor;* and
* 	*prometheus-nodeexporter*.

If you do not select all three containers, Prometheus will not start.

### *if you are running Old Menu …* { #installPromOldMenu }

When you select *Prometheus* in the IOTstack menu, the service definition includes the three containers:

*	*prometheus*
*	*prometheus-cadvisor;* and
* 	*prometheus-nodeexporter*.

## Significant directories and files { #significantFiles }

```
~/IOTstack
├── .templates
│   └── prometheus
│       ├── service.yml ❶
│       ├── Dockerfile ❷
│       ├── docker-entrypoint.sh ❸
│       └── iotstack_defaults ❹
│           └── config.yml
├── services
│   └── prometheus
│       └── service.yml ❺
├── docker-compose.yml ❻
└── volumes
    └── prometheus ❼
        └── data
            ├── config ❽
            │   ├── config.yml
            │   └── prometheus.yml
            └── data
```

1. The *template service definition*.
2. The *Dockerfile* used to customise *Prometheus* for IOTstack.
3. A pre-launch script to handle container self-repair before launching the *Prometheus* service.
4. Defaults for IOTstack, used to initialise on first run, and for container self-repair.
5. The *working service definition* (only relevant to old-menu, copied from ❶).
6. The *Compose* file (includes ❶).
7. The *persistent storage area*.
8. The [configuration directory](#configDir).

## How *Prometheus* gets built for IOTstack { #howPrometheusIOTstackGetsBuilt }

### *Prometheus* source code ([*GitHub*](https://github.com)) { #githubSourceCode }

The source code for *Prometheus* lives at [*GitHub* prometheus/prometheus](https://github.com/prometheus/prometheus).

### *Prometheus* images ([*DockerHub*](https://hub.docker.com)) { #dockerHubImages }

Periodically, the source code is recompiled and the resulting image is pushed to [prom/prometheus](https://hub.docker.com/r/prom/prometheus) on *DockerHub*.
 
### IOTstack menu { #iotstackMenu }

When you select *Prometheus* in the IOTstack menu, the *template service definition* is copied into the *Compose* file.

> Under old menu, it is also copied to the *working service definition* and then not really used.

### IOTstack first run { #iotstackFirstRun }

On a first install of IOTstack, you run the menu, choose *Prometheus* as one of your containers, and are told to do this:

``` console
$ cd ~/IOTstack
$ docker-compose up -d
```

`docker-compose` reads the *Compose* file. When it arrives at the `prometheus` fragment, it finds:

```yaml
prometheus:
  container_name: prometheus
  build: ./.templates/prometheus/.
```

The `build` statement tells `docker-compose` to look for:

```
~/IOTstack/.templates/prometheus/Dockerfile
```

> The *Dockerfile* is in the `.templates` directory because it is intended to be a common build for **all** IOTstack users. This is different to the arrangement for Node-RED where the *Dockerfile* is in the `services` directory because it is how each individual IOTstack user's version of Node-RED is customised.

The *Dockerfile* begins with:

```dockerfile
FROM prom/prometheus:latest
```

> If you need to pin to a particular version of *Prometheus*, the *Dockerfile* is the place to do it. See [*Prometheus* version pinning](#versionPinning).

The `FROM` statement tells the build process to pull down the ***base image*** from [*DockerHub*](https://hub.docker.com).

> It is a ***base*** image in the sense that it never actually runs as a container on your Raspberry Pi.

The remaining instructions in the *Dockerfile* customise the *base image* to produce a ***local image***. The customisations are:

1. Add configuration defaults appropriate for IOTstack.
2. Add `docker-entrypoint.sh` which:

	* Ensures the *internal* directory `/prometheus/config/` exists;
	* Copies any configuration files that have gone missing into that directory.
	* Enforces "pi:pi" ownership in `~/IOTstack/volumes/prometheus/data/config`.
	* Launches the *Prometheus* service.

The *local image* is instantiated to become your running container.

When you run the `docker images` command after *Prometheus* has been built, you *may* see two rows for *Prometheus*:

``` console
$ docker images
REPOSITORY           TAG         IMAGE ID       CREATED          SIZE
iotstack_prometheus  latest      1815f63da5f0   23 minutes ago   169MB
prom/prometheus      latest      3f9575991a6c   3 days ago       169MB
```

* `prom/prometheus` is the *base image*; and
* `iotstack_prometheus`  is the *local image*.

You *may* see the same pattern in Portainer, which reports the *base image* as "unused". You should not remove the *base* image, even though it appears to be unused.

> Whether you see one or two rows depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

### Dependencies: *CAdvisor* and *Node Exporter* { #dependencies }

The *CAdvisor* and *Node Exporter* are included in the *Prometheus* service definition as dependent containers. What that means is that each time you start *Prometheus*, `docker-compose` ensures that *CAdvisor* and *Node Exporter* are already running, and keeps them running.

The [default configuration](#activeConfig) for *Prometheus* assumes *CAdvisor* and *Node Exporter* are running and starts scraping information from those targets as soon as it launches.

## Configuring **Prometheus** { #configuringPrometheus }

### Configuration directory { #configDir }

The configuration directory for the IOTstack implementation of *Prometheus* is at the path:

```
~/IOTstack/volumes/prometheus/data/config
```

That directory contains two files:

* `config.yml`; and
* `prometheus.yml`.

If you delete either file, *Prometheus* will replace it with a default the next time the container starts. This "self-repair" function is intended to provide reasonable assurance that *Prometheus* will at least **start** instead of going into a restart loop.

Unless you [decide to change it](#environmentVars), the `config` folder and its contents are owned by "pi:pi". This means you can edit the files in the configuration directory without needing the `sudo` command. Ownership is enforced each time the container restarts.

#### Active configuration file { #activeConfig }

The file named `config.yml` is the active configuration. This is the file you should edit if you want to make changes. The default structure of the file is:

```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s

scrape_configs:
  - job_name: "iotstack"
    static_configs:
      - targets:
        - localhost:9090
        - cadvisor:8080
        - nodeexporter:9100
```

To cause a running instance of *Prometheus* to notice a change to this file:

``` console
$ cd ~/IOTstack
$ docker-compose restart prometheus
$ docker logs prometheus
```

Note:

* The YAML parser used by *Prometheus* seems to be ***exceptionally*** sensitive to syntax errors (far less tolerant than `docker-compose`). For this reason, you should **always** check the *Prometheus* log after any configuration change.

#### Reference configuration file { #referenceConfig }

The file named `prometheus.yml` is a reference configuration. It is a **copy** of the original configuration file that ships inside the *Prometheus* container at the path:

```
/etc/prometheus/prometheus.yml
```

Editing `prometheus.yml` has no effect. It is provided as a convenience to help you follow examples on the web. If you want to make the contents of `prometheus.yml` the active configuration, you need to do this:

``` console
$ cd ~/IOTstack/volumes/prometheus/data/config
$ cp prometheus.yml config.yml
$ cd ~/IOTstack
$ docker-compose restart prometheus
$ docker logs prometheus
```

### Environment variables { #environmentVars }

The IOTstack implementation of *Prometheus* supports two environment variables:

```yaml
environment:
  - IOTSTACK_UID=1000
  - IOTSTACK_GID=1000
```

Those variables control ownership of the [Configuration directory](#configDir) and its contents. Those environment variables are present in the standard IOTstack service definition for *Prometheus* and have the effect of assigning ownership to "pi:pi".

If you delete those environment variables from your *Compose* file, the [Configuration directory](#configDir) will be owned by "nobody:nobody"; otherwise the directory and its contents will be owned by whatever values you pass for those variables.

### Migration considerations { #migration }

Under the original IOTstack implementation of *Prometheus* (just "as it comes" from *DockerHub*), the service definition expected the configuration file to be at:

```
~/IOTstack/services/prometheus/config.yml
```

Under this implementation of *Prometheus*, the configuration file has moved to:

```
~/IOTstack/volumes/prometheus/data/config/config.yml
```

> The change of location is one of the things that allows self-repair to work properly. 

Some of the assumptions behind the default configuration file have changed. In particular, instead of the entire `scrape_configs` block being commented-out, it is active and defines `localhost`, `cadvisor` and `nodeexporter` as targets.

You should compare the old and new versions and decide which settings need to be migrated into the new configuration file.

If you change the configuration file, restart *Prometheus* and then check the log for errors:

``` console
$ docker-compose restart prometheus
$ docker logs prometheus
```

Note:

* The YAML parser used by *Prometheus* is very sensitive to syntax errors. Always check the *Prometheus* log after any configuration change.

## Upgrading *Prometheus* { #upgradingPrometheus }

You can update `cadvisor` and `nodeexporter` like this:

``` console
$ cd ~/IOTstack
$ docker-compose pull cadvisor nodeexporter
$ docker-compose up -d
$ docker system prune
```

In words:

* `docker-compose pull` downloads any newer images;
* `docker-compose up -d` causes any newly-downloaded images to be instantiated as containers (replacing the old containers); and
* the `prune` gets rid of the outdated images.

This "simple pull" strategy doesn't work when a *Dockerfile* is used to build a *local image* on top of a *base image* downloaded from [*DockerHub*](https://hub.docker.com). The *local image* is what is running so there is no way for the `pull` to sense when a newer version becomes available.

The only way to know when an update to *Prometheus* is available is to check the [prom/prometheus tags page](https://hub.docker.com/r/prom/prometheus/tags?page=1&ordering=last_updated) on *DockerHub*.

Once a new version appears on *DockerHub*, you can upgrade *Prometheus* like this:

``` console
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull prometheus
$ docker-compose up -d prometheus
$ docker system prune
$ docker system prune
```

Breaking it down into parts:

* `build` causes the named container to be rebuilt;
* `--no-cache` tells the *Dockerfile* process that it must not take any shortcuts. It really **must** rebuild the *local image*;
* `--pull` tells the *Dockerfile* process to actually check with [*DockerHub*](https://hub.docker.com) to see if there is a later version of the *base image* and, if so, to download it before starting the build;
* `prometheus ` is the named container argument required by the `build` command.

Your existing *Prometheus* container continues to run while the rebuild proceeds. Once the freshly-built *local image* is ready, the `up` tells `docker-compose` to do a new-for-old swap. There is barely any downtime for your service.

The `prune` is the simplest way of cleaning up. The first call removes the old *local image*. The second call cleans up the old *base image*.

> Whether an old *base image* exists depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

### *Prometheus* version pinning { #versionPinning }

If you need to pin *Prometheus* to a particular version:

1. Use your favourite text editor to open the following file:

	```
	~/IOTstack/.templates/prometheus/Dockerfile
	```

2. Find the line:

	```dockerfile
	FROM prom/prometheus:latest
	```

3. Replace `latest` with the version you wish to pin to. For example, to pin to version 2.30.2:

	```dockerfile
	FROM prom/prometheus:2.30.2
	```

4. Save the file and tell `docker-compose` to rebuild the local image:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d --build prometheus
	$ docker system prune
	``` 

	The new *local image* is built, then the new container is instantiated based on that image. The `prune` deletes the old *local image*.

Note:

* As well as preventing Docker from updating the *base image*, pinning will also block incoming updates to the *Dockerfile* from a `git pull`. Nothing will change until you decide to remove the pin.
