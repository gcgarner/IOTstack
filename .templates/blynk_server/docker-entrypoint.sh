#!/bin/bash
set -e

# were we launched as root with defaults available?
if [ "$(id -u)" = "0" -a -d /"$IOTSTACK_DEFAULTS_DIR" ]; then

   # yes! ensure that the IOTSTACK_CONF_DIR exists
   mkdir -p "$IOTSTACK_CONF_DIR"

   # populate runtime directory from the defaults
   rsync -arp --ignore-existing "/${IOTSTACK_DEFAULTS_DIR}/" "${IOTSTACK_CONF_DIR}"

   # enforce correct ownership
   chown -R "${IOTSTACK_UID:-nobody}":"${IOTSTACK_GID:-nobody}" "$IOTSTACK_CONF_DIR"

fi

# start the blynk server
exec "$@"
