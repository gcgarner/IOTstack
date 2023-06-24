#!/bin/bash
set -e

if [ "${1:0:1}" = '-' ]; then
    set -- telegraf "$@"
fi

# perform IOTstack self-repair
U="$(id -u)"
T="/etc/telegraf"
if [ "$U" = '0' -a -d "$T" ]; then
   echo "Performing IOTstack self repair"
   rsync -arp --ignore-existing /${IOTSTACK_DEFAULTS_DIR}/ "$T"
   chown -R "$U:$U" "$T"
fi

if [ $EUID -eq 0 ]; then

    # Allow telegraf to send ICMP packets and bind to privliged ports
    setcap cap_net_raw,cap_net_bind_service+ep /usr/bin/telegraf || echo "Failed to set additional capabilities on /usr/bin/telegraf"

    # note: at this point, the default version of this file runs:
    #
    #          exec setpriv --reuid telegraf --init-groups "$@"
    #
    #       Inside the container, user "telegraf" is userID 999, which
    #       isn't a member of the "docker" group outside container-space
    #       so the practical effect of downgrading privileges in this
    #       way is to deny access to /var/run/docker.sock, and then you
    #       get a mess. It's not clear whether the setcap is necessary
    #       on a Raspberry Pi but it has been left in place in case it
    #       turns out to be useful in other Docker environments.

fi

exec "$@"
