#!/bin/bash

# This script runs any prebackup commands you may need

if [ -f "./pre_backup.sh" ]; then
  echo "./pre_backup.sh file found, executing:"
  bash ./pre_backup.sh
fi
