#!/usr/bin/env bash

INTERNAL="/usr/src/node-red/node_modules"
EXTERNAL="$HOME/IOTstack/volumes/nodered/data/node_modules"

echo -e "\nNodes installed by Dockerfile INSIDE the container at $INTERNAL"

CANDIDATES=$(docker exec nodered bash -c "ls -1d $INTERNAL/node-red-*")

for C in $CANDIDATES; do

   NODE=$(basename "$C")

   # is a node of the same name also present externally
   if [ -d "$EXTERNAL/$NODE" ] ; then

      # yes! the internal node is blocked by the external node
      echo " BLOCKED: $NODE"

   else

      # no! so that means it's active
      echo "  ACTIVE: $NODE"

   fi

done

echo -e "\nNodes installed by Manage Palette OUTSIDE the container at $EXTERNAL"

CANDIDATES=$(ls -1d "$EXTERNAL/node-red-"*)

for C in $CANDIDATES; do

   NODE=$(basename "$C")

   echo " $NODE"

done

echo ""
