#!/bin/bash
set -e

# does the working directory exist (something is badly wrong if it does not)
if [ -d "$PYTHON_WORKDIR" ] ; then

   # are self-healing defaults available?
   if [ -d "$PYTHON_DEFAULTS" ] ; then

      # yes! replace anything that has gone missing
      cp -an "$PYTHON_DEFAULTS"/* "$PYTHON_WORKDIR"

   fi

   # set appropriate ownership throughout
   chown -R "$IOTSTACK_UID:$IOTSTACK_GID" "$PYTHON_WORKDIR"

fi

# start python
exec "$@"
