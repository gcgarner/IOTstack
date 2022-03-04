# Backing up and restoring IOTstack
This page explains how to use the backup and restore functionality of IOTstack.

## Backup
The backup command can be executed from IOTstack's menu, or from a cronjob.

### Running backup
To ensure that all your data is saved correctly, the stack should be brought down. This is mainly due to databases potentially being in a state that could cause data loss.

There are 2 ways to run backups:

* From the menu: `Backup and Restore` > `Run backup`
* Running the following command: `bash ./scripts/backup.sh`

The command that's run from the command line can also be executed from a cronjob:

```0 2 * * * cd /home/pi/IOTstack && /bin/bash ./scripts/backup.sh```

The current directory of bash must be in IOTstack's directory, to ensure that it can find the relative paths of the files it's meant to back up. In the example above, it's assume that it's inside the `pi` user's home directory.

### Arguments
```
./scripts/backup.sh {TYPE=3} {USER=$(whoami)}
```

* Types:
  * 1 = Backup with Date
    * A tarball file will be created that contains the date and time the backup was started, in the filename.
  * 2 = Rolling Date
    * A tarball file will be created that contains the day of the week (0-6) the backup was started, in the filename.
    * If a tarball already exists with the same name, it will be overwritten.
  * 3 = Both
* User:
    This parameter only becomes active if run as root. This script will default to the current logged in user
      If this parameter is not supplied when run as root, the script will ask for the username as input

Backups:

  * You can find the backups in the ./backups/ folder. With rolling being in ./backups/rolling/ and date backups in ./backups/backup/
  * Log files can also be found in the ./backups/logs/ directory.

### Examples:

  * `./scripts/backup.sh`
  * `./scripts/backup.sh 3`

Either of these will run both backups.

  * `./scripts/backup.sh 2`

This will only produce a backup in the rollowing folder. It will be called 'backup_XX.tar.gz' where XX is the current day of the week (as an int)

  * `sudo bash ./scripts/backup.sh 2 pi`

This will only produce a backup in the rollowing folder and change all the permissions to the 'pi' user.

## Restore
There are 2 ways to run a restore:

* From the menu: `Backup and Restore` > `Restore from backup`
* Running the following command: `bash ./scripts/restore.sh`

**Important**: The restore script assumes that the IOTstack directory is fresh, as if it was just cloned. If it is not fresh, errors may occur, or your data may not correctly be restored even if no errors are apparent.

*Note*: It is suggested that you test that your backups can be restored after initially setting up, and anytime you add or remove a service. Major updates to services can also break backups.

### Arguments
```
./scripts/restore.sh {FILENAME=backup.tar.gz} {noask}
```
The restore script takes 2 arguments:

* Filename: The name of the backup file. The file must be present in the `./backups/` directory, or a subfolder in it. That means it should be moved from `./backups/backup` to `./backups/`, or that you need to specify the `backup` portion of the directory (see examples)
* NoAsk: If a second parameter is present, is acts as setting the no ask flag to true. 

## Pre and post script hooks
The script checks if there are any pre and post back up hooks to execute commands. Both of these files will be included in the backup, and have also been added to the `.gitignore` file, so that they will not be touched when IOTstack updates.

### Prebackup script hook
The prebackup hook script is executed before any compression happens and before anything is written to the temporary backup manifest file (`./.tmp/backup-list_{{NAME}}.txt`). It can be used to prepare any services (such as databases that IOTstack isn't aware of) for backing up.

To use it, simple create a `./pre_backup.sh` file in IOTstack's main directory. It will be executed next time a backup runs.

### Postbackup script hook
The postbackup hook script is executed after the tarball file has been written to disk, and before the final backup log information is written to disk.

To use it, simple create a `./post_backup.sh` file in IOTstack's main directory. It will be executed after the next time a backup runs.

### Post restore script hook
The post restore hook script is executed after all files have been extracted and written to disk. It can be used to apply permissions that your custom services may require.

To use it, simple create a `./post_restore.sh` file in IOTstack's main directory. It will be executed after a restore happens.

## Third party integration
This section explains how to backup your files with 3rd party software.

### Dropbox
Coming soon.

### Google Drive
Coming soon.

### rsync
Coming soon.

### Duplicati
Coming soon.

### SFTP
Coming soon.
