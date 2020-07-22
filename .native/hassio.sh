echo "install requirements for hass.io"
	sudo apt install -y bash jq curl avahi-daemon dbus
	hassio_machine=$(whiptail --title "Machine type" --menu \
		"Please select you device type" 20 78 12 -- \
		"raspberrypi4" " " \
		"raspberrypi3" " " \
		"raspberrypi2" " " \
		"raspberrypi4-64" " " \
		"raspberrypi3-64" " " \
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
  curl -sL https://raw.githubusercontent.com/home-assistant/supervised-installer/master/installer.sh | sudo bash -s -- -m $hassio_machine
else
  echo "no selection"
  exit
fi