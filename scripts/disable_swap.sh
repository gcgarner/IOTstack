#!/bin/bash

if [ $1 = "uninstallswap" ]; then
  echo "Uninstalling swapfile..."
  sudo dphys-swapfile swapoff
  sudo dphys-swapfile uninstall
  sudo update-rc.d dphys-swapfile remove
  sudo systemctl disable dphys-swapfile
  echo "Swap file has been removed"
elif [ $1 = "disableswap" ]; then
  echo "Disabling swapfile..."
  if [ $(grep -c swappiness /etc/sysctl.conf) -eq 0 ]; then
    echo "vm.swappiness=0" | sudo tee -a /etc/sysctl.conf
    echo "updated /etc/sysctl.conf with vm.swappiness=0"
  else
    sudo sed -i "/vm.swappiness/c\vm.swappiness=0" /etc/sysctl.conf
    echo "vm.swappiness found in /etc/sysctl.conf update to 0"
  fi

  sudo sysctl vm.swappiness=0
  echo "set swappiness to 0 for immediate effect"
else
  echo "Param not set, pass either 'uninstallswap' or 'disableswap'"
fi
