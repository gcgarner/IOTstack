# Postbuild BASH Script
The postbuild bash script allows for executing arbitrary execution of bash commands after the stack has been build.

## How to use
Place a file in the main directory called `postbuild.sh`. When the buildstack [build logic](../Developers/Menu-System.md) finishes, it'll execute the `postbuild.sh` script, passing in each service selected from the buildstack menu as a parameter. This script is run each time the buildstack logic runs.

## Updates
The `postbuild.sh` file has been added to gitignore, so it won't be updated by IOTstack when IOTstack is updated. It has also been added to the backup script so that it will be backed up with your personal IOTstack backups.

## Example `postbuild.sh` script
The following script will print out each of the services built, and a custom message for nodered. If it was the first time the script was executed, it'll also output "Fresh Install" at the end, using a `.install_tainted` file for knowing.
```
#!/bin/bash

for iotstackService in "$@"
do
  echo "$iotstackService"
  if [ "$iotstackService" == "nodered" ]; then
    echo "NodeRed Installed!"
  fi
done

if [ ! -f .install_tainted ]; then
  echo "Fresh Install!"
  touch .install_tainted
fi
```

## What is my purpose?
The postbuild script can be used to run custom bash commands, such as moving files, or issuing commands that your services expect to be completed before running.
