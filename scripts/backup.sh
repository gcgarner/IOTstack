#!/bin/bash

# Usage:
# ./scripts/backup.sh {TYPE=3} {USER=$(whoami)}
#   Types:
#     1 = Backup with Date
#     2 = Rolling Date
#     3 = Both
#   User:
#     This parameter only becomes active if run as root. This script will default to the current logged in user
#       If this parameter is not supplied when run as root, the script will ask for the username as input
#
#   Backups:
#     You can find the backups in the ./backups/ folder. With rolling being in ./backups/rolling/ and date backups in ./backups/backup/
#     Log files can also be found in the ./backups/logs/ directory.
#
# Examples:
#   ./scripts/backup.sh
#   ./scripts/backup.sh 3
#     Either of these will run both backups.
#
#   ./scripts/backup.sh 2
#     This will only produce a backup in the rollowing folder. It will be called 'backup_XX.tar.gz' where XX is the current day of the week (as an int)
#
#   sudo bash ./scripts/backup.sh 2 pi
#     This will only produce a backup in the rollowing folder and change all the permissions to the 'pi' user.

if [ -d "./menu.sh" ]; then
	echo "./menu.sh file was not found. Ensure that you are running this from IOTstack's directory."
  exit 1
fi

BACKUPTYPE=${1:-"3"}

if [[ "$BACKUPTYPE" -ne "1" && "$BACKUPTYPE" -ne "2" && "$BACKUPTYPE" -ne "3" ]]; then
	echo "Unknown backup type '$BACKUPTYPE', can only be 1, 2 or 3"
  exit 1
fi

if [[ "$EUID" -eq 0 ]]; then
  if [ -z ${2+x} ]; then
    echo "Enter username to chown (change ownership) files to"
    read USER;
  else
    USER=$2
  fi
else
  USER=$(whoami)
fi

BASEDIR=./backups
TMPDIR=./.tmp
DOW=$(date +%u)
BASEBACKUPFILE="$(date +"%Y-%m-%d_%H%M")"
TMPBACKUPFILE="$TMPDIR/backup/backup_$BASEBACKUPFILE.tar.gz"
BACKUPLIST="$TMPDIR/backup-list_$BASEBACKUPFILE.txt"
LOGFILE="$BASEDIR/logs/backup_$BASEBACKUPFILE.log"
BACKUPFILE="$BASEDIR/backup/backup_$BASEBACKUPFILE.tar.gz"
ROLLING="$BASEDIR/rolling/backup_$DOW.tar.gz"

[ -d ./backups ] || mkdir ./backups
[ -d ./backups/logs ] || mkdir -p ./backups/logs
[ -d ./backups/backup ] || mkdir -p ./backups/backup
[ -d ./backups/rolling ] || mkdir -p ./backups/rolling
[ -d ./.tmp ] || mkdir ./.tmp
[ -d ./.tmp/backup ] || mkdir -p ./.tmp/backup
[ -d ./.tmp/databases_backup ] || mkdir -p ./.tmp/databases_backup

touch $LOGFILE
echo ""  > $LOGFILE
echo "### IOTstack backup generator log ###" >> $LOGFILE
echo "Started At: $(date +"%Y-%m-%dT%H-%M-%S")" >> $LOGFILE
echo "Current Directory: $(pwd)" >> $LOGFILE
echo "Backup Type: $BACKUPTYPE" >> $LOGFILE

if [[ "$BACKUPTYPE" -eq "1" || "$BACKUPTYPE" -eq "3" ]]; then
  echo "Backup File: $BACKUPFILE" >> $LOGFILE
fi

if [[ "$BACKUPTYPE" -eq "2" || "$BACKUPTYPE" -eq "3" ]]; then
  echo "Rolling File: $ROLLING" >> $LOGFILE
fi

echo "" >> $BACKUPLIST

echo "" >> $LOGFILE
echo "Executing prebackup scripts" >> $LOGFILE
bash ./scripts/backup_restore/pre_backup_complete.sh >> $LOGFILE 2>&1

echo "./services/" >> $BACKUPLIST
echo "./volumes/" >> $BACKUPLIST
[ -f "./docker-compose.yml" ] && echo "./docker-compose.yml" >> $BACKUPLIST
[ -f "./docker-compose.override.yml" ] && echo "./docker-compose.yml" >> $BACKUPLIST
[ -f "./compose-override.yml" ] && echo "./compose-override.yml" >> $BACKUPLIST
[ -f "./extra" ] && echo "./extra" >> $BACKUPLIST
[ -f "./.tmp/databases_backup" ] && echo "./.tmp/databases_backup" >> $BACKUPLIST
[ -f "./postbuild.sh" ] && echo "./postbuild.sh" >> $BACKUPLIST
[ -f "./post_backup.sh" ] && echo "./post_backup.sh" >> $BACKUPLIST
[ -f "./pre_backup.sh" ] && echo "./pre_backup.sh" >> $BACKUPLIST

sudo tar -czf $TMPBACKUPFILE -T $BACKUPLIST >> $LOGFILE 2>&1

[ -f "$ROLLING" ] && ROLLINGOVERWRITTEN=1 && rm -rf $ROLLING

sudo chown -R $USER:$USER $TMPDIR/backup* >> $LOGFILE 2>&1

if [[ "$BACKUPTYPE" -eq "1" || "$BACKUPTYPE" -eq "3" ]]; then
  cp $TMPBACKUPFILE $BACKUPFILE
fi
if [[ "$BACKUPTYPE" -eq "2" || "$BACKUPTYPE" -eq "3" ]]; then
  cp $TMPBACKUPFILE $ROLLING
fi

if [[ "$BACKUPTYPE" -eq "2" || "$BACKUPTYPE" -eq "3" ]]; then
  if [[ "$ROLLINGOVERWRITTEN" -eq 1 ]]; then
    echo "Rolling Overwritten: True" >> $LOGFILE
  else
    echo "Rolling Overwritten: False" >> $LOGFILE
  fi
fi

echo "Backup Size (bytes): $(stat --printf="%s" $TMPBACKUPFILE)" >> $LOGFILE
echo "" >> $LOGFILE

echo "Executing postbackup scripts" >> $LOGFILE
bash ./scripts/backup_restore/post_backup_complete.sh >> $LOGFILE 2>&1
echo "" >> $LOGFILE

echo "Finished At: $(date +"%Y-%m-%dT%H-%M-%S")" >> $LOGFILE
echo "" >> $LOGFILE

if [[ -f "$TMPBACKUPFILE" ]]; then
  echo "Items backed up:" >> $LOGFILE
  cat $BACKUPLIST >> $LOGFILE 2>&1
  echo "" >> $LOGFILE
  echo "Items Excluded:" >> $LOGFILE
  echo " - No items" >> $LOGFILE 2>&1
  rm -rf $BACKUPLIST >> $LOGFILE 2>&1
  rm -rf $TMPBACKUPFILE >> $LOGFILE 2>&1
else
  echo "Something went wrong backing up. The temporary backup file doesn't exist. No temporary files were removed"
  echo "Files: "
  echo "  $BACKUPLIST"
fi

echo "" >> $LOGFILE
echo "### End of log ###" >> $LOGFILE
echo "" >> $LOGFILE

cat $LOGFILE
