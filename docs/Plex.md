# Plex
## References 
* [Homepage](https://www.plex.tv/)
* [Docker](https://hub.docker.com/r/linuxserver/plex/)

## Web interface
The web UI can be found on `"your_ip":32400/web`

## Mounting an external drive by UUID to the home directory
[official mounting guide](https://www.raspberrypi.org/documentation/configuration/external-storage.md)

Create a directory in you home directory called `mnt` with a subdirectory `HDD`. Follow the instruction above to mount your external drive to `/home/pi/mnt/HDD` in you `fstab` edit your docker-compose.yml file under plex and uncomment the volumes for tv series and movies (modify the path to point to your media locations). Run `docker-compose up -d` to rebuild plex with the new volumes 