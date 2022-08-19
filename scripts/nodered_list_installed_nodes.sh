#!/usr/bin/env bash

# where Dockerfile installs components INSIDE the container
DOCKERFILE="/usr/src/node-red"

# paths to the persistent store
PERSISTENT_INTERNAL="/data"
PERSISTENT_EXTERNAL="$HOME/IOTstack/volumes/nodered/data"

# the folder in each case containing node modules
MODULES="node_modules"

# assume no modules are blocked
unset BLOCKED

# start the command hint
UNBLOCK="docker exec -w /data nodered npm uninstall"

# fetch what npm knows about components that form part of the image
echo -e "\nFetching list of candidates installed via Dockerfile"
CANDIDATES=$(docker exec nodered bash -c "cd \"$DOCKERFILE\" ; npm list --depth=0 --parseable 2>/dev/null")

# report
echo -e "\nComponents built into the image (via Dockerfile)"
PARENT=$(basename "$DOCKERFILE")
for CANDIDATE in $CANDIDATES; do
   COMPONENT=$(basename "$CANDIDATE")
   if [ "$COMPONENT" != "$PARENT" ] ; then
      if [ -d "$PERSISTENT_EXTERNAL/$MODULES/$COMPONENT" ] ; then
         # yes! the internal node is blocked by the external node
         echo "  BLOCKED: $COMPONENT"
         BLOCKED=true
         UNBLOCK="$UNBLOCK $COMPONENT"
      else
         # no! so that means it's active
         echo "   ACTIVE: $COMPONENT"
      fi
   fi
done

# fetch what npm knows about components that are in the persistent store
echo -e "\nFetching list of candidates installed via Manage Palette or npm"
CANDIDATES=$(docker exec nodered bash -c "cd \"$PERSISTENT_INTERNAL\" ; npm list --depth=0 --parseable")

# report
echo -e "\nComponents in persistent store at\n $PERSISTENT_EXTERNAL/$MODULES"
PARENT=$(basename "$PERSISTENT_INTERNAL")
for CANDIDATE in $CANDIDATES; do
   COMPONENT=$(basename "$CANDIDATE")
   if [ "$COMPONENT" != "$PARENT" ] ; then
      echo "  $COMPONENT"
   fi
done

echo ""

if [ -n "$BLOCKED" ] ; then
   echo "Blocking nodes can be removed by running the following commands"
   echo "\$ $UNBLOCK"
   echo "\$ docker-compose -f ~/IOTstack/docker-compose.yml restart nodered"
fi
