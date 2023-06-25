# Home Assistant

Home Assistant is a home automation platform. It is able to track and control all devices at your home and offer a platform for automating control.

## References { #references }

- [Home Assistant home page](https://www.home-assistant.io/)

	- [Raspberry Pi installation](https://www.home-assistant.io/installation/raspberrypi/)
	- [General installation](https://www.home-assistant.io/installation) (may be useful if you are trying to run on other hardware).

- [GitHub repository](https://github.com/home-assistant/core)
- [DockerHub](https://hub.docker.com/r/homeassistant/home-assistant/)


## Home Assistant: two versions { #twoVersions }

There are two versions of Home Assistant:

* Home Assistant Container; and
* Supervised Home Assistant (also known as both "Hass.io" and "Home Assistant Core").

Each version:

* provides a web-based management interface on port 8123; and
* runs in "host mode" in order to discover devices on your LAN, including devices communicating via multicast traffic.

Home Assistant Container runs as a **single** Docker container, and doesn't support all the features that Supervised Home Assistant does (such as add-ons). Supervised Home Assistant runs as a **collection** of Docker containers under its own orchestration.

The **only** method supported by IOTstack is Home Assistant Container.

> To understand why, see [about Supervised Home Assistant](#hassioBackground).

If Home Assistant Container will not do what you want then, basically, you will need two Raspberry Pis:

* One running Raspberry Pi OS ("Raspbian") hosting IOTstack; and
* Another dedicated to running [Home Assistant Operating System](https://www.home-assistant.io/installation/raspberrypi).

## Installing Home Assistant Container { #installHAContainer }

Home Assistant (Container) can be found in the `Build Stack` menu. Selecting it in this menu results in a service definition being added to:

```
~/IOTstack/docker-compose.yml
```

The normal IOTstack commands apply to Home Assistant Container such as:

```console
$ cd ~/IOTstack
$ docker-compose up -d
```

## Using bluetooth from the container { #usingBluetooth }

In order to be able to use BT & BLE devices from HA integrations, make sure that Bluetooth is enabled:

```console
$ hciconfig
hci0:	Type: Primary  Bus: UART
	BD Address: DC:89:FB:A6:32:4B  ACL MTU: 1021:8  SCO MTU: 64:1
	UP RUNNING 
	RX bytes:2003 acl:0 sco:0 events:159 errors:0
	TX bytes:11583 acl:0 sco:0 commands:159 errors:0
```

The "UP" in the third line of output indicates that Bluetooth is enabled. If Bluetooth is not enabled, check:

```console
$ grep "^AutoEnable" /etc/bluetooth/main.conf
AutoEnable=true
```

If `AutoEnable` is either missing or not set to `true`, then:

1. Use `sudo` to and your favouring text editor to open:

	```
	/etc/bluetooth/main.conf
	```

2. Find `AutoEnable` and make it `true`.

	> If `AutoEnable` is missing, it needs to be added to the `[Policy]` section.
	
3. Reboot your Raspberry Pi.
4. Check that the Bluetooth interface is enabled.

See also: [Scribles: Auto Power On Bluetooth Adapter on Boot-up](https://scribles.net/auto-power-on-bluetooth-adapter-on-boot-up/).

### Possible service definition changes { #serviceDefinition }

Although the [Home Assistant documentation](https://www.home-assistant.io/installation/raspberrypi#docker-compose) does not mention this, it is *possible* that you may also need to make the following changes to the Home Assistant service definition in your `docker-compose.yml`:

* Add the following mapping to the `volumes:` clause:

	```yaml
	- /var/run/dbus/system_bus_socket:/var/run/dbus/system_bus_socket
	```

* Add the following `devices:` clause:

	```yaml
	devices:
	  - "/dev/serial1:/dev/ttyAMA0"
	  - "/dev/vcio:/dev/vcio"
	  - "/dev/gpiomem:/dev/gpiomem"
	```

Notes:

* These changes are *specific* to the Raspberry Pi. If you need Bluetooth support on non-Pi hardware, you will need to figure out the details for your chosen platform.
* Historically, `/dev/ttyAMA0` meant "the serial interface" on Raspberry Pis. Subsequently, it came to mean "the Bluetooth interface" where Bluetooth support was present. Now, `/dev/serial1` is used to mean "the Raspberry Pi's Bluetooth interface". The example above maps that to the internal device `/dev/ttyAMA0` because that is **probably** what the container expects. There are no guarantees and you may need to experiment with internal device names.

## HTTPS with a valid SSL certificate { #httpsWithSSLcert }

Some HA integrations (e.g google assistant) require your HA API to be
accessible via https with a valid certificate. You can configure HA to do this:
[docs](https://www.home-assistant.io/docs/configuration/remote/) /
[guide](https://www.home-assistant.io/docs/ecosystem/certificates/lets_encrypt/)
or use a reverse proxy container, as described below.

The linuxserver Secure Web Access Gateway container
([swag](https://docs.linuxserver.io/general/swag)) ([Docker hub
docs](https://hub.docker.com/r/linuxserver/swag)) will automatically generate a
SSL-certificate, update the SSL certificate before it expires and act as a
reverse proxy.

1. First test your HA is working correctly: `http://raspberrypi.local:8123/` (assuming
your RPi hostname is raspberrypi)
2. Make sure you have duckdns working.
3. On your internet router, forward public port 443 to the RPi port 443
4. Add swag to ~/IOTstack/docker-compose.yml beneath the `services:`-line:

	```yaml
	  swag:
	    image: ghcr.io/linuxserver/swag
	    cap_add:
	      - NET_ADMIN
	    environment:
	      - PUID=1000
	      - PGID=1000
	      - TZ=${TZ:-Etc/UTC}
	      - URL=<yourdomain>.duckdns.org
	      - SUBDOMAINS=wildcard
	      - VALIDATION=duckdns
	      - DUCKDNSTOKEN=<token>
	      - CERTPROVIDER=zerossl
	      - EMAIL=<e-mail> # required when using zerossl
	    volumes:
	      - ./volumes/swag/config:/config
	    ports:
	      - 443:443
	    restart: unless-stopped
	```

	Replace the bracketed values. Do NOT use any "-characters to enclose the values.

5. Start the swag container, this creates the file to be edited in the next step:

	```console
	$ cd ~/IOTstack
	$ docker-compose up -d
	```

	Check it starts up OK: `docker-compose logs -f swag`. It will take a minute or two before it finally logs "Server ready".

6. Enable reverse proxy for `raspberrypi.local`. `homassistant.*` is already by default. and fix homeassistant container name ("upstream_app"):

	```console
	$ cd ~/IOTstack
	$ sed -e 's/server_name/server_name *.local/' \
	  volumes/swag/config/nginx/proxy-confs/homeassistant.subdomain.conf.sample \
	  > volumes/swag/config/nginx/proxy-confs/homeassistant.subdomain.conf
	```

7. Forward to correct IP when target is a container running in "network_mode:
   host" (like Home Assistant does):

    <!-- Note to documentation writers: using the console-highlighter would
    make the '#!/bin/sh'-line an unselectable "prompt". -->
	``` bash title="Note: in order for copy-paste to work properly, the usual $-prompts are omitted"
	cd ~/IOTstack
	cat << 'EOF' | sudo tee volumes/swag/config/custom-cont-init.d/add-host.docker.internal.sh
	#!/bin/sh
	DOCKER_GW=$(ip route | awk 'NR==1 {print $3}')
	
	sed -i -e "s/upstream_app .*/upstream_app ${DOCKER_GW};/" \
	   /config/nginx/proxy-confs/homeassistant.subdomain.conf
	EOF
	sudo chmod u+x volumes/swag/config/custom-cont-init.d/add-host.docker.internal.sh
	```

    (This needs to be copy-pasted/entered as-is, ignore any "> "-prefixes printed
    by bash)

8. (optional) Add reverse proxy password protection if you don't want to rely
   on the HA login for security, doesn't affect API-access:

	```console
	$ cd ~/IOTstack
	$ sed -i -e 's/#auth_basic/auth_basic/' \
		volumes/swag/config/nginx/proxy-confs/homeassistant.subdomain.conf
	$ docker-compose exec swag htpasswd -c /config/nginx/.htpasswd anyusername
	```

9. Add `use_x_forwarded_for` and `trusted_proxies` to your homeassistant [http
   config](https://www.home-assistant.io/integrations/http). The configuration
   file is at `volumes/home_assistant/configuration.yaml` For a default install
   the resulting http-section should be:

    ```yaml
    http:
       use_x_forwarded_for: true
       trusted_proxies:
         - 192.168.0.0/16
         - 172.16.0.0/12
         - 10.77.0.0/16
    ```

10. Refresh the stack: `cd ~/IOTstack && docker-compose stop && docker-compose
    up -d` (again may take 1-3 minutes for swag to start if it recreates
    certificates)
11. Test homeassistant is still working correctly:
    `http://raspberrypi.local:8123/` (assuming your RPi hostname is
    raspberrypi)
12. Test the reverse proxy https is working correctly:
    `https://raspberrypi.local/` (browser will issue a warning about wrong
    certificate domain, as the certificate is issued for you duckdns-domain, we
    are just testing)

    Or from the command line in the RPi:

    ```console
    $ curl --resolve homeassistant.<yourdomain>.duckdns.org:443:127.0.0.1 \
        https://homeassistant.<yourdomain>.duckdns.org/
    ```

    (output should end in `if (!window.latestJS) { }</script></body></html>`)

13. And finally test your router forwards correctly by accessing it from
    outside your LAN(e.g. using a mobile phone):
    `https://homeassistant.<yourdomain>.duckdns.org/` Now the certificate
    should work without any warnings.

## about Supervised Home Assistant { #hassioBackground }

IOTstack used to offer a menu entry leading to a convenience script that could install Supervised Home Assistant. That script stopped working when Home Assistant changed their approach. The script's author [made it clear](https://github.com/Kanga-Who/home-assistant/blob/master/Supervised%20on%20Raspberry%20Pi%20with%20Debian.md) that script's future was bleak so the affordance was [removed from IOTstack](https://github.com/SensorsIot/IOTstack/pull/493).

For a time, you could manually install Supervised Home Assistant using their [installation instructions for advanced users](https://github.com/home-assistant/supervised-installer). Once you got HA working, you could install IOTstack, and the two would (mostly) happily coexist.

The direction being taken by the Home Assistant folks is to supply a [ready-to-run image for your Raspberry Pi](https://www.home-assistant.io/installation/raspberrypi). They still support the installation instructions for advanced users but the [requirements](https://github.com/home-assistant/architecture/blob/master/adr/0014-home-assistant-supervised.md#supported-operating-system-system-dependencies-and-versions) are very specific. In particular:

> Debian Linux Debian 11 aka Bullseye (no derivatives)

Raspberry Pi OS is a Debian *derivative* and it is becoming increasingly clear that the "no derivatives" part of that requirement must be taken literally and seriously. Recent examples of significant incompatibilities include:

* [introducing a dependency on `grub` (GRand Unified Bootloader)](https://github.com/home-assistant/supervised-installer/pull/201). The Raspberry Pi does not use `grub` but the change is actually about forcing Control Groups version 1 when the Raspberry Pi uses version 2.
* [unilaterally starting `systemd-resolved`](https://github.com/home-assistant/supervised-installer/pull/202). This is a DNS resolver which claims port 53. That means you can't run your own DNS service like PiHole, AdGuardHome or BIND9 as an IOTstack container. 

Because of the self-updating nature of Supervised Home Assistant, your Raspberry Pi might be happily running Supervised Home Assistant plus IOTstack one day, and suddenly start misbehaving the next day, simply because Supervised Home Assistant assumed it was in total control of your Raspberry Pi.

If you want Supervised Home Assistant to work, reliably, it really needs to be its own dedicated appliance. If you want IOTstack to work, reliably, it really needs to be kept well away from Supervised Home Assistant. If you want both Supervised Home Assistant and IOTstack, you really need two Raspberry Pis.
