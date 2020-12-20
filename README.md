# IOT Stack

IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi.

## Getting started

See [Getting Started](https://sensorsiot.github.io/IOTstack/Getting-Started) in the Wiki. It includes:

* A link to Andreas Spiess video #295 and #352.
* How to download the project (including constraints you need to observe).
* Running the menu to install Docker and set up your containers.
* Useful Docker commands (start \& stop the stack, manage containers).

See also the [documentation home page](https://sensorsiot.github.io/IOTstack/).

## New Installation
### Automatic
1. Run the following command:
```
curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | bash
```

### Manual
1. Install git
```
$ cd ~/IOTstack
$ git remote set-url origin https://github.com/SensorsIot/IOTstack.git
$ git pull origin master
$ git checkout master
$ docker-compose down
$ ./menu.sh
$ docker-compose up -d
```

## Need the old menu back?
```
cd ~/IOTstack/
git pull
git checkout old-menu
```

## Experimental Features

## Running
1. To enter the directory and run menu for installation options:
```
cd ~/IOTstack
bash ./menu.sh
```

2. Install docker with the menu, restart your system.

3. Run menu again to select your build options, then start docker-compose with
```
$ cd ~/IOTstack
$ git pull origin master
$ git checkout master
$ ./menu.sh
```

Want to have the latest and greatest features? Switch to the experimental branch:

```
$ cd ~/IOTstack
$ git pull origin master
$ git checkout experimental
$ ./menu.sh
```

Do note that the experimental branch may be broken, or may break your setup, so ensure you have a good backup, and please report any issues. The way back is:


## Contributions

Please use the [issues](https://github.com/SensorsIot/IOTstack/issues) tab to report issues.

## Need help? Have a feature suggestion? Discovered a bug?
We have a Discord server setup for discussions: [IOTstack Discord channel](https://discord.gg/ZpKHnks) if you want to comment on features, suggest new container types, or ask the IOTstack community for help.

You can also report bugs or suggestions to our Github: https://github.com/SensorsIot/IOTstack/issues

If you use some of the tools in the project please consider donating or contributing on their projects. It doesn't have to be monetary. Reporting bugs and creating Pull Requests helps improve the projects for everyone.
