#!/usr/bin/env bash

# the name of this script is
SCRIPT=$(basename "$0")

# default image is
DEFAULTIMAGE="iotstack-nodered:latest"

# zero or one arguments supported
if [ "$#" -gt 1 ]; then
    echo "Usage: $SCRIPT {image:tag}"
    echo "   eg: $SCRIPT $DEFAULTIMAGE"
    exit -1
fi

# image can be passed as first argument, else default
IMAGE=${1:-"$DEFAULTIMAGE"}

# fetch latest version details from GitHub
LATEST=$(wget -O - -q https://raw.githubusercontent.com/node-red/node-red-docker/master/package.json | jq -r .version)

# figure out the version in the local image
INSTALLED=$(docker image inspect "$IMAGE" | jq -r .[0].Config.Labels[\"org.label-schema.version\"])

# compare versions and report result
if [ "$INSTALLED" = "$LATEST" ] ; then 

   echo "Node-Red is up-to-date (version $INSTALLED)"

else

/bin/cat <<-COLLECT_TEXT

	====================================================================
	Node-Red version number has changed on GitHub:

	    Local Version: $INSTALLED
	   GitHub Version: $LATEST
	
	This means a new version MIGHT be available on Dockerhub. Check here:

	   https://hub.docker.com/r/nodered/node-red/tags?page=1&ordering=last_updated

	When an updated version is actually avaliable, proceed like this:

	   $ REBUILD nodered
	   $ UP nodered
	   $ docker system prune
	====================================================================

COLLECT_TEXT

fi

