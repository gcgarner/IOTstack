#!/bin/bash

# Usage:
# ./scripts/restore.sh [FILENAME=backup.tar.gz] {noask}

# Examples:
#   ./scripts/restore.sh
#     Will restore from the backup file "./backups/backup.tar.gz"
#
#   ./scripts/restore.sh some_other_backup.tar.gz
#     Will restore from the backup file "./backups/some_other_backup.tar.gz"
#
#   ./scripts/restore.sh some_other_backup.tar.gz noask
#     Will restore from the backup file "./backups/some_other_backup.tar.gz" and will not warn that data will be deleted.
#

if [ -d "./menu.sh" ]; then
  echo "./menu.sh file was not found. Ensure that you are running this from IOTstack's directory."
  exit 1
fi

echo "Restoring from a backup will erase all existing data."
read -p "Continue [y/N]? " -n 1 -r PROCEED_WITH_RESTORE
echo ""
if [[ ! $PROCEED_WITH_RESTORE =~ ^[Yy]$ ]]; then
  echo "Restore Cancelled."
  exit 0
fi

RESTOREFILENAME="backup.tar.gz"
RESTOREFILENAME=${1:-$RESTOREFILENAME}

BASEDIR=./backups
TMPDIR=./.tmp
BASERESTOREFILE="$(date +"%Y-%m-%d_%H%M")"
RESTOREFILE="$BASEDIR/$RESTOREFILENAME"
LOGFILE="$BASEDIR/logs/restore_$BASERESTOREFILE.log"
BACKUPFILE="$BASEDIR/backup/backup_$BASERESTOREFILE.tar.gz"

[ -d ./backups ] || mkdir -p ./backups
[ -d ./backups/logs ] || mkdir -p ./backups/logs

[ -d ./.tmp ] || sudo rm -rf ./.tmp
[ -d ./tmp ] || mkdir -p ./tmp

touch $LOGFILE
echo ""  > $LOGFILE
echo "### IOTstack restore generator log ###" >> $LOGFILE
echo "Started At: $(date +"%Y-%m-%dT%H-%M-%S")" >> $LOGFILE
echo "Current Directory: $(pwd)" >> $LOGFILE
echo "Restore Type: Full" >> $LOGFILE

if [ ! -f $RESTOREFILE ]; then
  echo "File: '$RESTOREFILE' doesn't exist. Cancelling restore."
  echo "Finished At: $(date +"%Y-%m-%dT%H-%M-%S")" >> $LOGFILE
  echo "" >> $LOGFILE

  echo "" >> $LOGFILE
  echo "### End of log ###" >> $LOGFILE
  exit 2
fi

# Remove old files and folders
sudo rm -rf ./services/ >> $LOGFILE 2>&1
sudo rm -rf ./volumes/ >> $LOGFILE 2>&1
sudo rm -rf ./compose-override.yml >> $LOGFILE 2>&1
sudo rm -rf ./docker-compose.yml >> $LOGFILE 2>&1
sudo rm -rf ./extra/ >> $LOGFILE 2>&1
sudo rm -rf ./postbuild.sh >> $LOGFILE 2>&1
sudo rm -rf ./pre_backup.sh >> $LOGFILE 2>&1
sudo rm -rf ./post_backup.sh >> $LOGFILE 2>&1
sudo rm -rf ./post_restore.sh >> $LOGFILE 2>&1
sudo rm -rf ./post_restore.sh >> $LOGFILE 2>&1

sudo tar -zxvf \
	$RESTOREFILE >> $LOGFILE 2>&1

echo "" >> $LOGFILE

echo "Executing post restore scripts" >> $LOGFILE
bash ./scripts/backup_restore/post_restore_complete.sh >> $LOGFILE 2>&1
echo "" > $LOGFILE

echo "Finished At: $(date +"%Y-%m-%dT%H-%M-%S")" >> $LOGFILE
echo "" >> $LOGFILE

echo "" >> $LOGFILE
echo "### End of log ###" >> $LOGFILE
echo "" >> $LOGFILE

cat $LOGFILE
