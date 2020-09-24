# IOT Stack
IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi.


## Documentation for the project: 

https://sensorsiot.github.io/IOTstack/


## Video
[![#295 Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc.](http://img.youtube.com/vi/a6mjt8tWUws/0.jpg)](https://www.youtube.com/watch?v=a6mjt8tWUws "#295 Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc.")
**Andreas Spiess | #295 Raspberry Pi Server based on Docker, with VPN, Dropbox backup, Influx, Grafana, etc.**


## Installation
1. On the (RPi) lite image you will need to install git first

```
sudo apt-get install git -y
```

2. Download the repository with:
```
git clone https://github.com/SensorsIot/IOTstack.git ~/IOTstack
```

Due to some script restraints, this project needs to be stored in ~/IOTstack

3. To enter the directory and run menu for installation options:
```
cd ~/IOTstack && bash ./menu.sh
```

4. Install docker with the menu, restart your system.

5. Run menu again to select your build options, then start docker-compose with
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
## Add to the project

Feel free to add your comments on features or images that you think should be added.

## Contributions

If you use some of the tools in the project please consider donating or contributing on their projects. It doesn't have to be monetary, reporting bugs and PRs help improve the projects for everyone.