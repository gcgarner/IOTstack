# IOT Stack
IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi.


## Documentation for the project: 

https://sensorsiot.github.io/IOTstack/


## Video
https://youtu.be/a6mjt8tWUws


## Installation
### Automatic
1. Run the following command:
```
curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | sh
```

### Manual
1. Install git
```
sudo apt-get install git -y
```

2. Download the repository with:
```
git clone https://github.com/SensorsIot/IOTstack.git ~/IOTstack
```

## Running
1. To enter the directory and run menu for installation options:
```
cd ~/IOTstack
bash ./menu.sh
```

2. Install docker with the menu, restart your system.

3. Run menu again to select your build options, then start docker-compose with
```
docker-compose up -d
```

## Experimental Features
Want to have the latest and greatest features? Switch to the experimental branch:
```
git pull && git checkout experimental
./menu.sh
```

Do note that the experimental branch may be broken, or may break your setup, so ensure you have a good backup, and please report any issues.

## Migrating from the old repo?
```
cd ~/IOTstack/
git remote set-url origin https://github.com/SensorsIot/IOTstack.git
git pull origin master
docker-compose down
./menu.sh
docker-compose up -d
```

## Need help? Have a feature suggestion? Discovered a bug?
We have a Discord server setup for discussions: https://discord.gg/ZpKHnks

You can also report bugs or suggestions to our Github: https://github.com/SensorsIot/IOTstack/issues
