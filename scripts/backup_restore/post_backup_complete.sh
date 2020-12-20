#!/bin/bash

# This script runs any postbackup commands you may need

if [ -f "./post_backup.sh" ]; then
  echo "./post_backup.sh file found, executing:"
  bash ./post_backup.sh
fi

docker-compose up -d