#!/bin/ash
set -e

PWFILE="/mosquitto/pwfile/pwfile"

# Set permissions
user="$(id -u)"
if [ "$user" = '0' -a -d "/mosquitto" ]; then

   echo "[IOTstack] begin self-repair"

   rsync -arpv --ignore-existing /${IOTSTACK_DEFAULTS_DIR}/ "/mosquitto"

   # general ownership assuming mode as set in template
   chown -Rc mosquitto:mosquitto /mosquitto

   # specific requirements for the password file
   chmod -c 600 "$PWFILE"

   echo "[IOTstack] end self-repair"
   
fi

exec "$@"

