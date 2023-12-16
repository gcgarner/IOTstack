#!/bin/bash

set -e

# sensible defaults for supported variables
export MJPG_STREAMER_SIZE=${MJPG_STREAMER_SIZE:-640x480}
export MJPG_STREAMER_FPS=${MJPG_STREAMER_FPS:-5}
export MJPG_STREAMER_INTERNAL_DEVICE=${MJPG_STREAMER_INTERNAL_DEVICE:-/dev/video0}

# form credential string (if the user does not pass a username, the
# username will be the container name - change on each recreate; if
# the user does not pass a password, the password will be a uuid and
# will change on every launch).
MJPG_STREAMER_USERNAME=${MJPG_STREAMER_USERNAME:-$(hostname -s)}
MJPG_STREAMER_PASSWORD=${MJPG_STREAMER_PASSWORD:-$(uuidgen)}
export MJPG_STREAMER_CREDENTIALS="-c ${MJPG_STREAMER_USERNAME}:${MJPG_STREAMER_PASSWORD}"

# are we running as root?
if [ "$(id -u)" = '0' ] ; then

	echo "MJPG Streamer launched at $(date)"

	# any self-repair code goes here - there is no persistent storage
	# at the moment so this is irrelevant.

fi

# away we go
exec "$@"
