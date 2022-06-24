# IOTstack

IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi.

## introduction to IOTstack - videos

These are from 2019 and 2020. Though IOTstack has changed quite a bit, they are
still a great overview

Andreas Spiess Video #295: Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc: IOTstack

[![#295 Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc: IOTstack](http://img.youtube.com/vi/a6mjt8tWUws/0.jpg)](https://www.youtube.com/watch?v=a6mjt8tWUws)

Andreas Spiess Video #352: Raspberry Pi4 Home Automation Server (incl. Docker, OpenHAB, HASSIO, NextCloud)

[![#352 Raspberry Pi4 Home Automation Server (incl. Docker, OpenHAB, HASSIO, NextCloud)](http://img.youtube.com/vi/KJRMjUzlHI8/0.jpg)](https://www.youtube.com/watch?v=KJRMjUzlHI8)

### getting started

See [Getting Started](https://sensorsiot.github.io/IOTstack/Getting-Started) in the [IOTstack Wiki](https://sensorsiot.github.io/IOTstack/). It includes:

* A link to Andreas Spiess videos #295 and #352.
* How to download the project (including constraints you need to observe).
* How to migrate from the older gcgarner/IOTstack repository.
* Running the menu to install Docker and set up your containers.
* Useful Docker commands (start \& stop the stack, manage containers).
* Stack maintenance.

### significant change to networking

After 2022-01-18 the menu has changed to use Docker networks differently. Users from before this need to do [migration](https://sensorsiot.github.io/IOTstack/Updates/migration-network-change/) in order to add new services. In essence, just re-select all your services using the menu. If not done, docker-compose will give you an error like:

```
ERROR: Service "influxdb" uses an undefined network "iotstack_nw"
```

### contributions

Please use the [issues](https://github.com/SensorsIot/IOTstack/issues) tab to report issues.

### Need help? Have a feature suggestion? Discovered a bug?

We have a Discord server setup for discussions: [IOTstack Discord channel](https://discord.gg/ZpKHnks) if you want to comment on features, suggest new container types, or ask the IOTstack community for help.

If you use some of the tools in the project please consider donating or contributing on their projects. It doesn't have to be monetary. Reporting bugs and [creating Pull Requests](https://gist.github.com/Paraphraser/818bf54faf5d3b3ed08d16281f32297d) helps improve the projects for everyone.
