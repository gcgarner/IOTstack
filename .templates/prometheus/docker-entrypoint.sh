#!/bin/ash
set -e

# set defaults for config structure ownership
UID="${IOTSTACK_UID:-nobody}"
GID="${IOTSTACK_GID:-nobody}"

# were we launched as root?
if [ "$(id -u)" = "0" -a -d /"$IOTSTACK_DEFAULTS_DIR" ]; then

   # yes! ensure that the IOTSTACK_CONFIG_DIR exists
   mkdir -p "$IOTSTACK_CONFIG_DIR"
   
   # populate runtime directory from the defaults
   for P in /"$IOTSTACK_DEFAULTS_DIR"/* ; do

      C=$(basename "$P")

      if [ ! -e "$IOTSTACK_CONFIG_DIR/$C" ] ; then

         cp -a "$P" "$IOTSTACK_CONFIG_DIR/$C"

      fi

   done

   # enforce correct ownership
   chown -R "$UID":"$GID" "$IOTSTACK_CONFIG_DIR"
   
fi

# launch prometheus with supplied arguments
exec /bin/prometheus "$@"
