# Updating the project

Periodically updates are made to project which include new or modified container template, changes to backups or additional features. As these are released your local copy of this project will become out of date. This section deals with how to bring your project to the latest published state.

Quick instructions:

1. backup your current settings: `cp docker-compose.yml docker-compose.yml.bak`
2. check `git status` for any local changes you may have made to project files. Save and preserve your changes by doing a commit: `git commit -a -m "local customization"`. Or revert them using: `git checkout -- path/to/changed_file`.
3. update project files from github: `git pull origin master -r`
4. get latest images from the web: `docker-compose pull`
5. rebuild localy created images from new Dockerfiles: `docker-compose build --pull --no-cache`
6. update running containers to latest: `docker-compose up --build -d`

*Troubleshooting:* if a container fails to restart after update
* try restarting the whole stack: `docker-compose restart`
* backup your stack settings: `cp docker-compose.yml docker-compose.yml.bak`
* Check log output of the failing service: `docker-compose logs *service-name*`
  * try googling and fixing problems in docker-compose.yml manually. 
* try recreating the failing service definition using menu.sh:
  * `./menu.sh`, select Build Stack, unselect the failing service, press enter
	to build, and then exit.
  * `./menu.sh`, select Build Stack, select the service back again, press enter
	to build, and then exit.
  * Try starting now: `docker-compose up -d`
* Go to the IOTStack Discord and ask for help.

## Details, partly outdated

**If you ran the git checkout -- 'git ls-files -m' as suggested in the old wiki entry then please check your duck.sh because it removed your domain and token**

Git offers build in functionality to fetch the latest changes.

`git pull origin master` will fetch the latest changes from GitHub without overwriting files that you have modified yourself. If you have done a local commit then your project may to handle a merge conflict.

This can be verified by running `git status`. You can ignore if it reports duck.sh as being modified.

![image](https://user-images.githubusercontent.com/46672225/68645804-d42d0000-0521-11ea-842f-fd0b2d22cd0e.png)

Should you have any modified scripts or templates they can be reset to the latest version with `git checkout -- scripts/ .templates/`

With the new latest version of the project you can now use the menu to build your stack. If there is a particular container you would like to update its template then you can select that at the overwrite option for your container. You have the choice to not to overwrite, preserve env files or to completely overwrite any changes (passwords)

![image](https://user-images.githubusercontent.com/46672225/68646024-8fee2f80-0522-11ea-8b6e-f1d439a5be7f.png)

After your stack had been rebuild you can run `docker-compose up -d` to pull in the latest changes. If you have not update your images in a while consider running the `./scripts/update.sh` to get the latest version of the image from Docker hub as well
