# IOTstack

IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi.

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
