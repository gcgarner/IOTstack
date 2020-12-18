# Home assistant
## References
- [Docker](https://hub.docker.com/r/homeassistant/home-assistant/)
- [Webpage](https://www.home-assistant.io/)

Hass.io is a home automation platform running on Python 3. It is able to track and control all devices at home and offer a platform for automating control. Port binding is `8123`.
Hass.io is exposed to your hosts' network in order to discover devices on your LAN. That means that it does not sit inside docker's network.

## To avoid confusion
There are 2 versions of Home Assistant: Hass.io and Home Assistant Docker. Hass.io uses its own orchastration with 3 docker images: `hassio_supervisor`, `hassio_dns` and `homeassistant`. Home Assistant Docker runs inside a single docker image, and doesn't support all the features that Hass.io does (such as add-ons). IOTstack allows installing either, but we can only offer limited configuration of Hass.io since it is its own platform. [More info on versions](https://www.home-assistant.io/docs/installation/#recommended)

## Menu installation
Hass.io installation can be found inside the `Native Installs` menu on the main menu. Home Assistant can be found in the `Build Stack` menu.

You will be asked to select you device type during the installation. Hass.io is no longer dependant on the IOTstack, it has its own service for maintaining its uptime.

## Installation
Due to the behaviour of Network Manager, it is strongly recomended to connect the Pi over a wired internet connection, rather than WiFi.
If you ignore the advice about connecting via Ethernet and install Network Manager while your session is connected via WiFi, your connection will freeze part way through the installation (when Network Manager starts running and unconditionally changes your Raspberry Pi's WiFi MAC address).

Ensure your system is up to date with:
```
sudo apt update
```
If not already installed, install the network manager with:
```
sudo apt-get install network-manager apparmor-utils
```
before running the hass.io installation to avoid any potential errors.

The installation of Hass.io takes up to 20 minutes (depending on your internet connection). Refrain from restarting your machine until it has come online and you are able to create a user account.

## Removal

To remove Hass.io you first need to stop the service that controls it. Run the following in the terminal: 

```bash
sudo systemctl stop hassio-supervisor.service
sudo systemctl disable hassio-supervisor.service
```

This should stop the main service however there are two additional container that still need to be address

This will stop the service and disable it from starting on the next boot

Next you need to stop the hassio_dns and hassio_supervisor

```bash
docker stop hassio_supervisor
docker stop hassio_dns
docker stop homeassistant
```

If you want to remove the containers

```bash
docker rm hassio_supervisor
docker rm hassio_dns
docker stop homeassistant
```

After rebooting you should be able to reinstall

The stored file are located in `/usr/share/hassio` which can be removed if you need to

Double check with `docker ps` to see if there are other hassio containers running. They can stopped and removed in the same fashion for the dns and supervisor

You can use Portainer to view what is running and clean up the unused images.
