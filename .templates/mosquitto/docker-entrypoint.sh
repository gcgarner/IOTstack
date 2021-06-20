#!/bin/ash
set -e

# Set permissions
user="$(id -u)"
if [ "$user" = '0' -a -d "/mosquitto" ]; then

   rsync -arp --ignore-existing /${IOTSTACK_DEFAULTS_DIR}/ "/mosquitto"

   chown -R mosquitto:mosquitto /mosquitto
   
fi

exec "$@"

