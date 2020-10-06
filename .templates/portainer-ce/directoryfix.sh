#!/bin/bash

# This script is intended as a simplistic one-time migration aid. The
# script checks for:
#
# 1. the PRESENCE of the (old) portainer (assumed 1.24.1) persistent
#    storage directory; and
# 2. the ABSENCE of the (new) portainer-ce (assumed 2.0.0) persistent
#    storage directory.
#
# If both conditions are met, the old persistent storage directory
# is copied to become the new persistent storage directory.
#
# The first time portainer-ce runs it is then in the same situation as
# if docker-compose.yml had been changed from:
#
#   image: portainer/portainer
#
# to:
#
#   image: portainer/portainer-ce
#
# portainer-ce can then perform any first-launch migration steps while
# preserving the admin password and the like.

OLD="./volumes/portainer"
NEW="./volumes/portainer-ce"

if [ -d "$OLD" -a ! -d "$NEW" ] ; then

   echo "$OLD exists but $NEW does not - auto-cloning"

   sudo cp -Rp "$OLD" "$NEW"

fi

