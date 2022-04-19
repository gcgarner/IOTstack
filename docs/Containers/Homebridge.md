# Homebridge

## References 

* [GitHub home](https://github.com/oznu/docker-homebridge)
* [Configuration Guide](https://github.com/oznu/docker-homebridge/wiki/Homebridge-on-Raspberry-Pi)
* [DockerHub](https://hub.docker.com/r/oznu/homebridge)

## Configuration

Homebridge documentation has a comprehensive [configuration guide](https://github.com/oznu/docker-homebridge/wiki/Homebridge-on-Raspberry-Pi) which you are encouraged to read.

Homebridge is configured using environment variables. In IOTstack:

* If you are running new menu (master branch, the default), environment variables are kept inline in `docker-compose.yml`.
* If you are running old menu (old-menu branch), environment variables are at the path:

	```
	~/IOTstack/services/homebridge/homebridge.env
	```

In either case, you apply changes by editing the relevant file (`docker-compose.yml` or `homebridge.env`) and then:

```console
$ cd ~/IOTstack
$ docker-compose up -d homebridge
```

### About "avahi"

"avahi", "multicast DNS", "Rendezvous", "Bonjour" and "ZeroConf" are synonyms.

Current Homebridge images disable avahi services by default. The Homebridge container runs in "host mode" which means it can participate in multicast traffic flows. If you have a plugin that requires avahi, it can enabled by setting the environment variable:

```yaml
ENABLE_AVAHI=1
```  

## Web Interface

The web UI for Homebridge can be found on `"your_ip":8581`. You can change the port by adjusting the environment variable:

```
HOMEBRIDGE_CONFIG_UI_PORT=8581
```
