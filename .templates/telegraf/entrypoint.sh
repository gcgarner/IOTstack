#!/bin/bash
set -e

if [ "${1:0:1}" = '-' ]; then
    set -- telegraf "$@"
fi

# perform IOTstack self-repair
U="$(id -u)"
T="/etc/telegraf"
if [ "$U" = '0' -a -d "$T" ]; then
   rsync -arp --ignore-existing /${IOTSTACK_DEFAULTS_DIR}/ "$T"
   chown -R "$U:$U" "$T"
fi

exec "$@"


