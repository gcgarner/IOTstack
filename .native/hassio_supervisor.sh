#!/bin/bash

echo " "
echo "Ensure that you have read the documentation on installing Hass.io before continuing."
echo "Not following the installation instructions may render you system to be unable to connect to the internet."
echo "Hass.io Documentation: "
echo "  https://sensorsiot.github.io/IOTstack/Containers/Home-Assistant/"

echo " "
sleep 1

read -r -n 1 -p "Press Y to continue, any other key to cancel " response;

if [[ $response == "y" || $response == "Y" ]]; then
	echo "Install requirements for Hass.io"
	sudo apt install -y bash jq curl avahi-daemon dbus
	hassio_machine=$(whiptail --title "Machine type" --menu \
		"Please select you device type" 20 78 12 -- \
		"raspberrypi4-64" " " \
		"raspberrypi4" " " \
		"raspberrypi3-64" " " \
		"raspberrypi3" " " \
		"raspberrypi2" " " \
		"qemux86" " " \
		"qemux86-64" " " \
		"qemuarm" " " \
		"qemuarm-64" " " \
		"orangepi-prime" " " \
		"odroid-xu" " " \
		"odroid-c2" " " \
		"intel-nuc" " " \
		"tinker" " " \
		3>&1 1>&2 2>&3)

	if [ -n "$hassio_machine" ]; then
		sudo systemctl disable ModemManager
		sudo systemctl stop ModemManager
		curl -sL "https://raw.githubusercontent.com/Kanga-Who/home-assistant/master/supervised-installer.sh" | sudo bash -s -- -m $hassio_machine
		clear
		exit 0
	else
		clear
		echo "No selection"
		exit 4
	fi
	clear
	exit 3
else
	clear
	exit 5
fi