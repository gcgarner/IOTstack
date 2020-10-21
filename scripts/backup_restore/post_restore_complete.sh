#!/bin/bash

# This script runs any post restore commands you may need

if [ -f "./post_restore.sh" ]; then
  echo "./post_restore.sh file found, executing:"
  bash ./post_restore.sh
fi
