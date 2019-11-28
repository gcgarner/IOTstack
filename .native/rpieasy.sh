#!/bin/bash

echo "Updating and installing requirements"
sudo apt-get update && sudo apt-get install -y python3-pip screen alsa-utils wireless-tools wpasupplicant zip unzip git

sudo pip3 install jsonpickle

if [ -d ~/rpieasy ]; then
    pushd ~/rpieasy
    echo "Detected RPIEasy directory, updating project" 
    git pull origin master
    popd
else
    git clone https://github.com/enesbcs/rpieasy.git ~/rpieasy
fi

echo "RPIEasy has been installed or updated"
echo "You can run with 'sudo ~/rpieasy/RPIEasy.py'"