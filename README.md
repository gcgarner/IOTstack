# IOT Stack

IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi.

## Getting started

See [Getting Started](https://sensorsiot.github.io/IOTstack/Getting-Started) in the Wiki. It includes:

* A link to Andreas Spiess video #295.
* How to download the project (including constraints you need to observe).
* Running the menu to install Docker and set up your containers.
* Useful Docker commands (start \& stop the stack, manage containers).

See also the [documentation home page](https://sensorsiot.github.io/IOTstack/).

## Migrating from the old repo?

If you have been running IOTstack from [gcgarner/IOTstack](https://github.com/gcgarner/IOTstack) and want to migrate to this repository (SensorsIot/IOTstack), do the following:

```
$ cd ~/IOTstack
$ git remote set-url origin https://github.com/SensorsIot/IOTstack.git
$ git pull origin master
$ git checkout master
$ docker-compose down
$ ./menu.sh
$ docker-compose up -d
```

## Experimental Features

Want to have the latest and greatest features? Switch to the experimental branch:

```
$ cd ~/IOTstack
$ git pull origin master
$ git checkout experimental
$ ./menu.sh
```

Do note that the experimental branch may be broken, or may break your setup, so ensure you have a good backup, and please report any issues. The way back is:

```
$ cd ~/IOTstack
$ git pull origin master
$ git checkout master
$ ./menu.sh
```

## Contributions

Please use the [issues](https://github.com/SensorsIot/IOTstack/issues) tab to report issues.

Join the [IOTstack Discord channel](https://discord.gg/W45tD83) if you want to comment on features, suggest new container types, or ask the IOTstack community for help.

If you use some of the tools in the project please consider donating or contributing on their projects. It doesn't have to be monetary. Reporting bugs and creating Pull Requests helps improve the projects for everyone.
