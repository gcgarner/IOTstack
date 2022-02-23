# Prometheus

## <a name="references"> References </a>

* [*Prometheus* home](https://prometheus.io)
* *GitHub*:

	- [*Prometheus*](https://github.com/prometheus/prometheus)
	- [*CAdvisor*](https://github.com/google/cadvisor)
	- [*Node Exporter*](https://github.com/prometheus/node_exporter)

* *DockerHub*:

	- [*Prometheus*](https://hub.docker.com/r/prom/prometheus)
	- [*CAdvisor*](https://hub.docker.com/r/zcube/cadvisor)
	- [*Node Exporter*](https://hub.docker.com/r/prom/node-exporter)

## <a name="overview"> Overview </a>

Prometheus is a collection of three containers:

* *Prometheus*
* *CAdvisor*
* *Node Exporter*

The [default configuration](#activeConfig) for *Prometheus* supplied with IOTstack scrapes information from all three containers.

## <a name="installProm"> Installing Prometheus </a>

### <a name="installPromNewMenu"> *if you are running New Menu …* </a>

When you select *Prometheus* in the IOTstack menu, you must also select:

*	*prometheus-cadvisor;* and
* 	*prometheus-nodeexporter*.

If you do not select all three containers, Prometheus will not start.

### <a name="installPromOldMenu"> *if you are running Old Menu …* </a>

When you select *Prometheus* in the IOTstack menu, the service definition includes the three containers:

*	*prometheus*
*	*prometheus-cadvisor;* and
* 	*prometheus-nodeexporter*.

## <a name="significantFiles"> Significant directories and files </a>

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

## <a name="howPrometheusIOTstackGetsBuilt"> How *Prometheus* gets built for IOTstack </a>

### <a name="githubSourceCode"> *Prometheus* source code ([*GitHub*](https://github.com)) </a>

The source code for *Prometheus* lives at [*GitHub* prometheus/prometheus](https://github.com/prometheus/prometheus).

### <a name="dockerHubImages"> *Prometheus* images ([*DockerHub*](https://hub.docker.com)) </a>

Periodically, the source code is recompiled and the resulting image is pushed to [prom/prometheus](https://hub.docker.com/r/prom/prometheus) on *DockerHub*.
 
### <a name="iotstackMenu"> IOTstack menu </a>

When you select *Prometheus* in the IOTstack menu, the *template service definition* is copied into the *Compose* file.

> Under old menu, it is also copied to the *working service definition* and then not really used.

### <a name="iotstackFirstRun"> IOTstack first run </a>

On a first install of IOTstack, you run the menu, choose *Prometheus* as one of your containers, and are told to do this:

```bash
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

```bash
$ docker images
REPOSITORY           TAG         IMAGE ID       CREATED          SIZE
iotstack_prometheus  latest      1815f63da5f0   23 minutes ago   169MB
prom/prometheus      latest      3f9575991a6c   3 days ago       169MB
```

* `prom/prometheus` is the *base image*; and
* `iotstack_prometheus`  is the *local image*.

You *may* see the same pattern in Portainer, which reports the *base image* as "unused". You should not remove the *base* image, even though it appears to be unused.

> Whether you see one or two rows depends on the version of `docker-compose` you are using and how your version of `docker-compose` builds local images.

### <a name="dependencies"> Dependencies: *CAdvisor* and *Node Exporter* </a>

The *CAdvisor* and *Node Exporter* are included in the *Prometheus* service definition as dependent containers. What that means is that each time you start *Prometheus*, `docker-compose` ensures that *CAdvisor* and *Node Exporter* are already running, and keeps them running.

The [default configuration](#activeConfig) for *Prometheus* assumes *CAdvisor* and *Node Exporter* are running and starts scraping information from those targets as soon as it launches.

## <a name="configuringPrometheus"> Configuring **Prometheus** </a>

### <a name="configDir"> Configuration directory </a>

The configuration directory for the IOTstack implementation of *Prometheus* is at the path:

```
~/IOTstack/volumes/prometheus/data/config
```

That directory contains two files:

* `config.yml`; and
* `prometheus.yml`.

If you delete either file, *Prometheus* will replace it with a default the next time the container starts. This "self-repair" function is intended to provide reasonable assurance that *Prometheus* will at least **start** instead of going into a restart loop.

Unless you [decide to change it](#environmentVars), the `config` folder and its contents are owned by "pi:pi". This means you can edit the files in the configuration directory without needing the `sudo` command. Ownership is enforced each time the container restarts.

#### <a name="activeConfig"> Active configuration file </a>

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

```bash
$ cd ~/IOTstack
$ docker-compose restart prometheus
$ docker logs prometheus
```

Note:

* The YAML parser used by *Prometheus* seems to be ***exceptionally*** sensitive to syntax errors (far less tolerant than `docker-compose`). For this reason, you should **always** check the *Prometheus* log after any configuration change.

#### <a name="referenceConfig"> Reference configuration file </a>

The file named `prometheus.yml` is a reference configuration. It is a **copy** of the original configuration file that ships inside the *Prometheus* container at the path:

```
/etc/prometheus/prometheus.yml
```

Editing `prometheus.yml` has no effect. It is provided as a convenience to help you follow examples on the web. If you want to make the contents of `prometheus.yml` the active configuration, you need to do this:

```bash
$ cd ~/IOTstack/volumes/prometheus/data/config
$ cp prometheus.yml config.yml
$ cd ~/IOTstack
$ docker-compose restart prometheus
$ docker logs prometheus
```

### <a name="environmentVars"> Environment variables </a>

The IOTstack implementation of *Prometheus* supports two environment variables:

```yaml
environment:
  - IOTSTACK_UID=1000
  - IOTSTACK_GID=1000
```

Those variables control ownership of the [Configuration directory](#configDir) and its contents. Those environment variables are present in the standard IOTstack service definition for *Prometheus* and have the effect of assigning ownership to "pi:pi".

If you delete those environment variables from your *Compose* file, the [Configuration directory](#configDir) will be owned by "nobody:nobody"; otherwise the directory and its contents will be owned by whatever values you pass for those variables.

### <a name="migration"> Migration considerations </a>

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

```bash
$ docker-compose restart prometheus
$ docker logs prometheus
```

Note:

* The YAML parser used by *Prometheus* is very sensitive to syntax errors. Always check the *Prometheus* log after any configuration change.

## <a name="upgradingPrometheus"> Upgrading *Prometheus* </a>

You can update `cadvisor` and `nodeexporter` like this:

```bash
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

```bash
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

### <a name="versionPinning"> *Prometheus* version pinning </a>

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

	```bash
	$ cd ~/IOTstack
	$ docker-compose up -d --build prometheus
	$ docker system prune
	``` 

	The new *local image* is built, then the new container is instantiated based on that image. The `prune` deletes the old *local image*.

Note:

* As well as preventing Docker from updating the *base image*, pinning will also block incoming updates to the *Dockerfile* from a `git pull`. Nothing will change until you decide to remove the pin.
