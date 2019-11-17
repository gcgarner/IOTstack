#!/bin/bash
sudo touch /etc/modprobe.d/blacklist-rtl.conf
[ $(grep -c rtl28xxu /etc/modprobe.d/blacklist-rtl.conf) -eq 0 ] && sudo echo "blacklist dvb_usb_rtl28xxu" >>/etc/modprobe.d/blacklist-rtl.conf

sudo touch /etc/modprobe.d/blacklist-rtl8xxxu.conf
[ $(grep -c rtl8xxxu /etc/modprobe.d/blacklist-rtl8xxxu.conf) -eq 0 ] && sudo echo "blacklist rtl8xxxu" >>/etc/modprobe.d/blacklist-rtl8xxxu.conf

sudo apt-get update
sudo apt-get install -y libtool \
	libusb-1.0.0-dev \
	librtlsdr-dev \
	rtl-sdr \
	doxygen \
	cmake \
	automake

git clone https://github.com/merbanan/rtl_433.git ~/rtl_433
cd ~/rtl_433/
mkdir build
cd build
cmake ../
make
sudo make install

echo "you should reboot for changes to take effect"