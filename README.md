# IOT Stack
IOTstack is a builder for docker-compose to easily make and maintain IoT stacks on the Raspberry Pi.

## Documentation for the project: 

https://sensorsiot.github.io/IOTstack/

## Video
https://youtu.be/a6mjt8tWUws

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
