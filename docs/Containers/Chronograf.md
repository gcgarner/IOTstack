# Chronograf
 
## References

- [*influxdata Chronograf* documentation](https://docs.influxdata.com/chronograf/)
- [*GitHub*: influxdata/influxdata-docker/chronograf](https://github.com/influxdata/influxdata-docker/tree/master/chronograf)
- [*DockerHub*: influxdata Chronograf](https://hub.docker.com/_/chronograf)

## Kapacitor integration

If you selected Kapacitor in the menu and want Chronograf to be able to interact with it, you need to edit `docker-compose.yml` to un-comment the lines which are commented-out in the following:

```yaml
chronograf:
  …
  environment:
  …
  # - KAPACITOR_URL=http://kapacitor:9092
  depends_on:
  …
  # - kapacitor
```

If the Chronograf container is already running when you make this change, run:

``` console
$ cd ~IOTstack
$ docker-compose up -d chronograf
```

## Upgrading Chronograf

You can update the container via:

``` console
$ cd ~/IOTstack
$ docker-compose pull
$ docker-compose up -d
$ docker system prune
```

In words:

* `docker-compose pull` downloads any newer images;
* `docker-compose up -d` causes any newly-downloaded images to be instantiated as containers (replacing the old containers); and
* the `prune` gets rid of the outdated images.

### Chronograf version pinning

If you need to pin to a particular version:

1. Use your favourite text editor to open `docker-compose.yml`.
2. Find the line:

	``` yaml
	image: chronograf:latest
	```

3. Replace `latest` with the version you wish to pin to. For example, to pin to version 1.9.0:

	``` yaml
	image: chronograf:1.9.0
	```

4. Save the file and tell `docker-compose` to bring up the container:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d chronograf
	$ docker system prune
	```
