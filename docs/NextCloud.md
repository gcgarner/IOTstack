# Next Cloud
## DO NOT EXPOSE PORT 80 TO THE WEB

It is a very bad idea to expose unencrypted traffic to the web. You will need to use a reverse-proxy to ensure your password is not stolen and your account hacked.

I'm still working on getting a good encrypted reverse proxy working. However in the interim you can use a VPN tunnel like OpenVPN or Zerotier to securely connect to your private cloud

## Backups

Nextcloud has been excluded from the docker_backup script due to its potential size. Once I've found a better way of backing it up I will add a dedicated script for it.

## Setup

Next-Cloud recommends using MySQL/MariaDB for the accounts and file list. The alternative is to use SQLite however they strongly discourage using it

This is the service yml. Notice that there are in fact two containers, one for the db and the other for the cloud itself. You will need to change the passwords **before** starting the stack (remember to change the docker-compose.yml and ./services/nextcloud/service.yml), if you dont you will need to delete the volume directory and start again.

```yml
  nextcloud:
    image: nextcloud
    container_name: nextcloud
    ports:
      - 9321:80
    volumes:
      - ./volumes/nextcloud/html:/var/www/html
    restart: unless-stopped
    depends_on: 
      - nextcloud_db

  nextcloud_db:
    image: linuxserver/mariadb
    container_name: nextcloud_db
    volumes:
      - ./volumes/nextcloud/db:/config
    environment:
      - MYSQL_ROOT_PASSWORD=stronger_password
      - MYSQL_PASSWORD=strong_password
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

```

The port is 9321

![image](https://user-images.githubusercontent.com/46672225/69730546-f2ede200-1130-11ea-97f4-0f4f81d08fad.png)

click on the storage options, select maraiadb/mysql and fill in the details as follows

![image](https://user-images.githubusercontent.com/46672225/69731273-46acfb00-1132-11ea-9b10-579bb8b3dd9a.png)

Note that you data will be stored in `./volumes/nextcloud/html/data/{account}`

![image](https://user-images.githubusercontent.com/46672225/69732101-b1ab0180-1133-11ea-95dc-8a2e6fb80536.png)

Also note that file permissions are "www-data" so you cant simply copy data into this folder directly, you should use the web interface or the app.

It would be a good idea to mount an external drive to store the data in rather than on your sd card. details to follow shortly. Something like:

![image](https://user-images.githubusercontent.com/46672225/69873297-a3d6b700-12c0-11ea-98c9-40f358137b77.png)

The external drive will have to be an ext4 formatted drive because smb, fat32 and NTFS can't handle linux file permissions. If the permissions aren't set to "www-data" then the container wont be able to write to the disk.

Just a warning: If your database gets corrupted then your nextcloud is pretty much stuffed