#!/bin/bash

if [ ! -d ~/log2ram ]; then
  git clone https://github.com/azlux/log2ram.git ~/log2ram
  chmod +x ~/log2ram/install.sh
  pushd ~/log2ram
  sudo ./install.sh
  popd
else
  echo "Log2RAM is already installed. You can reinstall by running: 'sudo ./install.sh' from ~/log2ram "
  sleep 1
fi
