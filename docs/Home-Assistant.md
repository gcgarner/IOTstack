# Home assistant
## References
- [Docker](https://hub.docker.com/r/homeassistant/home-assistant/)
- [Webpage](https://www.home-assistant.io/)

Hass.io is a home automation platform running on Python 3. It is able to track and control all devices at home and offer a platform for automating control. Port binding is `8123`.
Hass.io is exposed to your hosts' network in order to discover devices on your LAN. That means that it does not sit inside docker's network.

## Menu installation
Hass.io now has a seperate installation in the menu. The old version was incorrect and should be removed. Be sure to update you project and install the correct version.

You will be asked to select you device type during the installation. Hass.io is no longer dependant on the IOTstack, it has its own service for maintaining its uptime.

## Installation
The installation of Hass.io takes up to 20 minutes (depending on your internet connection). Refrain from restarting your Pi until it had come online and you are able to create a user account 

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