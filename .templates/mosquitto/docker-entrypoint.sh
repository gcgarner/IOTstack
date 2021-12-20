#!/bin/ash
set -e

# Set permissions
user="$(id -u)"
if [ "$user" = '0' -a -d "/mosquitto" ]; then

   echo "[IOTstack] begin self-repair"

   rsync -arpv --ignore-existing /${IOTSTACK_DEFAULTS_DIR}/ "/mosquitto"

   chown -Rc mosquitto:mosquitto /mosquitto

   echo "[IOTstack] end self-repair"
   
fi

exec "$@"

