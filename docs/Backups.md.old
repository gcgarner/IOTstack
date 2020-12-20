# Backups
Because containers can easily be rebuilt from docker hub we only have to back up the data in the "volumes" directory.

## Cloud Backups
### Dropbox-Uploader
This a great utility to easily upload data from your Pi to the cloud. https://magpi.raspberrypi.org/articles/dropbox-raspberry-pi. It can be installed from the Menu under Backups.
### rclone (Google Drive)
This is a service to upload to Google Drive. The config is described [here]( https://medium.com/@artur.klauser/mounting-google-drive-on-raspberry-pi-f5002c7095c2). Install it from the menu then follow the link for these sections:
* Getting a Google Drive Client ID
* Setting up the Rclone Configuration

When naming the service in `rclone config` ensure to call it "gdrive"

**The Auto-mounting instructions for the drive in the link don't work on Rasbian**. Auto-mounting of the drive isn't necessary for the backup script.

If you want your Google Drive to mount on every boot then follow the instructions at the bottom of the wiki page


## Influxdb
`~/IOTstack/scripts/backup_influxdb.sh` does a database snapshot and stores it in ~/IOTstack/backups/influxdb/db . This can be restored with the help a script (that I still need to write)

## Docker backups
The script `~/IOTstack/scripts/docker_backup.sh` performs the master backup for the stack. 

This script can be placed in a cron job to backup on a schedule.
Edit the crontab with`crontab -e`
Then add `0 23 * * * ~/IOTstack/scripts/docker_backup.sh >/dev/null 2>&1` to have a backup every night at 23:00.

This script cheats by copying the volume folder live. The correct way would be to stop the stack first then copy the volumes and restart. The cheating method shouldn't be a problem unless you have fast changing data like in influxdb. This is why the script makes a database export of influxdb and ignores its volume. 

### Cloud integration
The docker_backup.sh script now no longer requires modification to enable cloud backups. It now tests for the presence of and enable file in the backups folder
#### Drobox-Uploader
The backup tests for a file called `~/IOTstack/backups/dropbox`, if it is present it will upload to dropbox. To disable dropbox upload delete the file. To enable run `sudo touch ~/IOTstack/backups/dropbox`
#### rclone
The backup tests for a file called `~/IOTstack/backups/rclone`, if it is present it will upload to google drive. To disable rclone upload delete the file. To enable run `sudo touch ~/IOTstack/backups/rclone`

#### Pruning online backups
@877dev has added functionality to prune both local and cloud backups. For dropbox make sure you dont have any files that contain spaces in your backup directory as the script cannot handle it at this time.

### Restoring a backup
The "volumes" directory contains all the persistent data necessary to recreate the container. The docker-compose.yml and the environment files are optional as they can be regenerated with the menu. Simply copy the volumes directory into the IOTstack directory, Rebuild the stack and start. 

## Added your Dropbox token incorrectly or aborted the install at the token screen

Make sure you are running the latest version of the project [link](https://sensorsiot.github.io/IOTstack/Updating-the-Project/).

Run `~/Dropbox-Uploader/dropbox_uploader.sh unlink` and if you have added it key then it will prompt you to confirm its removal. If no key was found it will ask you for a new key.

Confirm by running `~/Dropbox-Uploader/dropbox_uploader.sh` it should ask you for your key if you removed it or show you the following prompt if it has the key:

```
 $ ~/Dropbox-Uploader/dropbox_uploader.sh
Dropbox Uploader v1.0
Andrea Fabrizi - andrea.fabrizi@gmail.com

Usage: /home/pi/Dropbox-Uploader/dropbox_uploader.sh [PARAMETERS] COMMAND...

Commands:
	 upload   <LOCAL_FILE/DIR ...>  <REMOTE_FILE/DIR>
	 download <REMOTE_FILE/DIR> [LOCAL_FILE/DIR]
	 delete   <REMOTE_FILE/DIR>
	 move     <REMOTE_FILE/DIR> <REMOTE_FILE/DIR>
	 copy     <REMOTE_FILE/DIR> <REMOTE_FILE/DIR>
	 mkdir    <REMOTE_DIR>
....

```

Ensure you **are not** running as sudo as this will store your api in the /root directory as `/root/.dropbox_uploader`

If you ran the command with sudo the remove the old token file if it exists with either `sudo rm /root/.dropbox_uploader` or `sudo ~/Dropbox-Uploader/dropbox_uploader.sh unlink`

## Auto-mount Gdrive with rclone

To enable rclone to mount on boot you will need to make a user service. Run the following commands

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/gdrive.service
```
Copy the following code into the editor, save and exit

```
[Unit]
Description=rclone: Remote FUSE filesystem for cloud storage
Documentation=man:rclone(1)

[Service]
Type=notify
ExecStartPre=/bin/mkdir -p %h/mnt/gdrive
ExecStart= \
  /usr/bin/rclone mount \
  --fast-list \
  --vfs-cache-mode writes \
  gdrive: %h/mnt/gdrive

[Install]
WantedBy=default.target
```
enable it to start on boot with: (no sudo)
```bash
systemctl --user enable gdrive.service
```
start with 
```bash
systemctl --user start gdrive.service
```
if you no longer want it to start on boot then type:
```bash
systemctl --user disable gdrive.service
```

