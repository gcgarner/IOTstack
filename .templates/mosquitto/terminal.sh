#!/bin/bash

echo "you are about to enter the shell for mosquitto"
echo "to add a password: mosquitto_passwd -c /mosquitto/config/pwfile MYUSER"
echo "the command will ask for you password and confirm"
echo "to exit: exit"

docker exec -it mosquitto sh
