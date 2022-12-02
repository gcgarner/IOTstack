#!/usr/bin/env bash

# support user renaming of script
SCRIPT=$(basename "$0")

# dependency check
if [ -z "$(which rsync)" -o -z "$(which jq)" ] ; then
   echo "This script depends on jq and rsync. Please run"
   echo "   sudo apt update && sudo apt install jq rsync"
   exit -1
fi

# useful function
isContainerRunning() {
   if STATUS=$(curl -s --unix-socket /var/run/docker.sock http://localhost/containers/$1/json | jq .State.Status) ; then
      if [ "$STATUS" = "\"running\"" ] ; then
         return 0
      fi
   fi
   return 1
}


# should not run as root
[ "$EUID" -eq 0 ] && echo "$SCRIPT should NOT be run using sudo" && exit -1

# dependency check
if [ -z "$(which rsync)" -o -z "$(which jq)" ] ; then
   echo "This script depends on jq and rsync. Please run"
   echo "   sudo apt update && sudo apt install jq rsync"
   exit -1
fi

read -r -d '' RUNNINGNOTES <<-EOM
\n
===============================================================================

Error: The WireGuard container can't be running during the migration.
       Please stop the container like this:

          $ cd ~/IOTstack
          $ docker-compose rm --force --stop -v wireguard

       Do not start the container again until the migration is complete and
       you have followed the instructions for modifying WireGuard's service
       definition in your docker-compose.yml

===============================================================================
\n
EOM

# wireguard can't be running
isContainerRunning "wireguard" && echo -e "$RUNNINGNOTES" && exit -1

# source directory is
WIREGUARD="$HOME/IOTstack/volumes/wireguard"

# source directory must exist
[ ! -d "$WIREGUARD" ] && echo "Error: $WIREGUARD does not exist" && exit -1

# the backup directory is
BACKUP="$WIREGUARD.bak"

read -r -d '' REPEATNOTES <<-EOM
\n
===============================================================================

Error: It looks like you might be trying to migrate twice! You can't do that.

       If you need to start over, you can try resetting like this:

          $ cd ~/IOTstack/volumes
          $ sudo rm -rf wireguard
          $ sudo mv wireguard.bak wireguard

       Alternatively, restore ~/IOTstack/volumes/wireguard from a backup.

===============================================================================
\n
EOM

# required sub-directories are
CONFIGD="config"
INITD="custom-cont-init.d"
SERVICESD="custom-services.d"

# backup directory must not exist
[ -d "$BACKUP" ] && echo -e "$REPEATNOTES" && exit -1

# required sub-directories must not exist
[ -d "$WIREGUARD/$CONFIGD" ] && echo -e "$REPEATNOTES" && exit -1
[ -d "$WIREGUARD/$INITD" ] && echo -e "$REPEATNOTES" && exit -1
[ -d "$WIREGUARD/$SERVICESD" ] && echo -e "$REPEATNOTES" && exit -1

# rename source to backup
echo "Renaming $WIREGUARD to $BACKUP"
sudo mv "$WIREGUARD" "$BACKUP"

# create the required directories
echo "creating required sub-folders"
sudo mkdir -p "$WIREGUARD/$CONFIGD" "$WIREGUARD/$INITD" "$WIREGUARD/$SERVICESD"

# for now, set ownership to the current user
echo "setting ownership on $WIREGUARD to $USER"
sudo chown -R "$USER":"$USER" "$WIREGUARD"

# migrate config directory components
echo "migrating user-configuration components"
rsync -r --ignore-existing --exclude="${INITD}*" --exclude="${SERVICESD}*" "$BACKUP"/ "$WIREGUARD/$CONFIGD"

# migrate special cases and change ownership to root
echo "migrating custom configuration options"
for C in "$INITD" "$SERVICESD" ; do
   for D in "$BACKUP/$C"* ; do
      echo "   merging $D into $WIREGUARD/$C"
      rsync -r --ignore-existing --exclude="README.txt" "$D"/ "$WIREGUARD/$C"
      echo "   changing ownership to root"
      sudo chown -R root:root "$WIREGUARD/$C"
   done
done

# force correct mode for wg0.conf
echo "Setting mode 600 on $WIREGUARD/$CONFIGD/wg0.conf"
chmod 600 "$WIREGUARD/$CONFIGD/wg0.conf"

read -r -d '' COMPOSENOTES <<-EOM
\n
===============================================================================

Migration seems to have been successful. Do NOT start the WireGuard container
until you have updated WireGuard's service definition:

Old:

  volumes:
  - ./volumes/wireguard:/config
  - /lib/modules:/lib/modules:ro

New:

  volumes:
  - ./volumes/wireguard/config:/config
  - ./volumes/wireguard/custom-cont-init.d:/custom-cont-init.d
  - ./volumes/wireguard/custom-services.d:/custom-services.d
  - /lib/modules:/lib/modules:ro

Pay careful attention to the lines starting with "- ./volumes". Do NOT
just copy and paste the middle two lines. The first line has changed too.

===============================================================================
\n
EOM

# all done - display the happy news
echo -e "$COMPOSENOTES"
