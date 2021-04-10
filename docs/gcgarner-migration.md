# Migrating from gcgarner to SensorsIot

These instructions explain how to migrate from [gcgarner/IOTstack](https://github.com/gcgarner/IOTstack) to [SensorsIot/IOTstack](https://github.com/SensorsIot/IOTstack).

Migrating to SensorsIot/IOTstack was fairly easy when this repository was first forked from gcgarner/IOTstack. Unfortunately, what was a fairly simple switching procedure no longer works properly because conflicts have emerged.

The probability of conflicts developing increases as a function of time since the fork. Conflicts were and are pretty much inevitable so a more involved procedure is needed.

## <a name="migrationSteps"> Migration Steps </a>

### <a name="checkAssumptions"> Step 1 – Check your assumptions </a>

Make sure that you are, *actually*, on gcgarner. Don't assume!

```
$ git remote -v
origin	https://github.com/gcgarner/IOTstack.git (fetch)
origin	https://github.com/gcgarner/IOTstack.git (push)
```

Do not proceed if you don't see those URLs!

### <a name="downStack"> Step 2 – Take IOTstack down </a>

Take your stack down. This is not *strictly* necessary but we'll be moving the goalposts a bit so it's better to be on the safe side.

```
$ cd ~/IOTstack
$ docker-compose down
```

### <a name="chooseMigrationMethod"> Step 3 – Choose your migration method </a>

There are two basic approaches to switching from gcgarner/IOTstack to SensorsIot/IOTstack:

- [Migration by changing upstream repository](#migrateChangeUpstream)
- [Migration by clone and merge](#migrateCloneMerge)

You can think of the first as "working *with* git" while the second is "using brute force".

The first approach will work if you haven't tried any other migration steps and/or have not made too many changes to items in your gcgarner/IOTstack that are under git control.

If you are already stuck or you try the first approach and get a mess, or it all looks far too hard to sort out, then try the [Migration by clone and merge](#migrateCloneMerge) approach.

#### <a name="migrateChangeUpstream"> Migration Option 1 – change upstream repository </a>

##### <a name="checkLocalChanges"> Check for local changes </a>

Make sure you are on the master branch (you probably are so this is just a precaution), and then see if Git thinks you have made any local changes:

```
$ cd ~/IOTstack
$ git checkout master
$ git status
```

If Git reports any "modified" files, those will probably get in the way of a successful migration so it's a good idea to get those out of the way.

For example, suppose you edited `menu.sh` at some point. Git would report that as:

```
	modified:   menu.sh
```

The simplest way to deal with modified files is to rename them to move them out of the way, and then restore the original:

1. Rename your customised version by adding your initials to the end of the filename. Later, you can come back and compare your customised version with the version from GitHub and see if you want to preserve any changes.

	Here I'm assuming your initials are "jqh":

	```
	$ mv menu.sh menu.sh.jqh
	```
	
2. Tell git to restore the unmodified version:

	```
	$ git checkout -- menu.sh
	```
	
3. Now, repeat the Git command that complained about the file:

	```
	$ git status
	```
	
	The modified file will show up as "untracked" which is OK (ignore it)
	
	```
	Untracked files:
	  (use "git add <file>..." to include in what will be committed)
	
		menu.sh.jqh
	```

##### <a name="synchroniseGcgarner"> Synchronise with gcgarner on GitHub </a>

Make sure your local copy of gcgarner is in sync with GitHub.

```
$ git pull
```

##### <a name="removeUpstream"> Get rid of any upstream reference </a>

There may or may not be any "upstream" set. The most likely reason for this to happen is if you used your local copy as the basis of a Pull Request.

The next command will probably return an error, which you should ignore. It's just a precaution.

```
$ git remote remove upstream
```

##### <a name="pointToSensorsIoT"> Point to SensorsIot </a>

Change your local repository to point to SensorsIot.

```
$ git remote set-url origin https://github.com/SensorsIot/IOTstack.git
```

##### <a name="syncSensorsIoT"> Synchronise with SensorsIot on GitHub </a>

This is where things can get a bit tricky so please read these instructions carefully **before** you proceed.

When you run the next command, it will probably give you a small fright by opening a text-editor window. Don't panic - just keep reading. Now, run this command:

```
$ git pull -X theirs origin master
```

The text editor window will look something like this:

```
Merge branch 'master' of https://github.com/SensorsIot/IOTstack

# Please enter a commit message to explain why this merge is necessary,
# especially if it merges an updated upstream into a topic branch.
#
# Lines starting with '#' will be ignored, and an empty message aborts
# the commit.
```

The first line is a pre-prepared commit message, the remainder is boilerplate instructions which you can ignore.

Exactly which text editor opens is a function of your `EDITOR` environment variable and the `core.editor` set in your global Git configuration. If you:

* remember changing `EDITOR` and/or `core.editor` then, presumably, you will know how to interact with your chosen text editor. You don't need to make any changes to this file. All you need to do is save the file and exit;

* **don't** remember changing either `EDITOR` or `core.editor` then the editor will probably be the default `vi` (aka `vim`). You need to type ":wq" (without the quotes) and then press return. The ":" puts `vi` into command mode, the "w" says "save the file" and "q" means "quit `vi`". Pressing return runs the commands.  

Git will display a long list of stuff. It's very tempting to ignore it but it's a good idea to take a closer look, particularly for signs of error or any lines beginning with:

```
Auto-merging
```

At the time of writing, you can expect Git to mention these two files:

```
Auto-merging menu.sh
Auto-merging .templates/zigbee2mqtt/service.yml
```

Those are known issues and the merge strategy `-X theirs` on the `git pull` command you have just executed deals with both, correctly, by preferring the SensorsIot version.

Similar conflicts may emerge in future and those will **probably** be dealt with, correctly, by the same merge strategy. Nevertheless, you should still check the output very carefully for other signs of merge conflict so that you can at least be alive to the possibility that the affected files may warrant closer inspection.

For example, suppose you saw:

```
Auto-merging .templates/someRandomService/service.yml
```

If you don't use `someRandomService` then you could safely ignore this on the basis that it was "probably right". However, if you did use that service and it started to misbehave after migration, you would know that the `service.yml` file was a good place to start looking for explanations.

##### <a name="finishWithPull"> Finish with a pull </a>

At this point, only the migrated master branch is present on your local copy of the repository. The next command brings you fully in-sync with GitHub:

```
$ git pull
```

#### <a name="migrateCloneMerge"> Migration Option 2 – clone and merge </a>

If you have been following the process correctly, your IOTstack will already be down.

##### <a name="renameOldIOTstack"> Rename your existing IOTstack folder </a>

Move your old IOTstack folder out of the way, like this:

```
$ cd ~
$ mv IOTstack IOTstack.old
```

Note:

* You should not need `sudo` for the `mv` command but it is OK to use it if necessary.

##### <a name="fetchCleanClone"> Fetch a clean clone of SensorsIot/IOTstack </a>

```
$ git clone https://github.com/SensorsIot/IOTstack.git ~/IOTstack
```

Explore the result:

```
$ tree -aFL 1 --noreport ~/IOTstack
/home/pi/IOTstack
├── .bash_aliases
├── .git/
├── .github/
├── .gitignore
├── .native/
├── .templates/
├── .tmp/
├── LICENSE
├── README.md
├── docs/
├── duck/
├── install.sh*
├── menu.sh*
├── mkdocs.yml
└── scripts/
```

Note:

* If the `tree` command is not installed for some reason, use `ls -A1F ~/IOTstack`.

Observe what is **not** there:

* There is no `docker-compose.yml`
* There is no `backups` directory
* There is no `services` directory
* There is no `volumes` directory

From this, it should be self-evident that a clean checkout from GitHub is the factory for *all* IOTstack installations, while the contents of `backups`, `services`, `volumes` and `docker-compose.yml` represent each user's individual choices, configuration options and data.

##### <a name="mergeOldWithNew"> Merge old into new </a>

Execute the following commands:

```
$ mv ~/IOTstack.old/docker-compose.yml ~/IOTstack
$ mv ~/IOTstack.old/services ~/IOTstack
$ sudo mv ~/IOTstack.old/volumes ~/IOTstack 
```

You should not need to use `sudo` for the first two commands. However, if you get a permissions conflict on either, you should proceed like this:

* docker-compose.yml

	```
	$ sudo mv ~/IOTstack.old/docker-compose.yml ~/IOTstack
	$ sudo chown pi:pi ~/IOTstack/docker-compose.yml
	```

* services

	```
	$ sudo mv ~/IOTstack.old/services ~/IOTstack
	$ sudo chown -R pi:pi ~/IOTstack/services
	```

There is no need to migrate the `backups` directory. You are better off creating it by hand:

```
$ mkdir ~/IOTstack/backups
```

### <a name="chooseMenu"> Step 4 – Choose your menu </a>

If you have reached this point, you have migrated to SensorsIot/IOTstack where you are on the "master" branch. This implies "new menu".

The choice of menu is entirely up to you. Differences include:

1. New menu takes a **lot** more screen real-estate than old menu. If you do a fair bit of work on small screens (eg iPad) you might find it hard to work with new menu.
2. New menu creates a large number of internal Docker networks whereas old menu has *one internal network to rule them all*. The practical consequence is that most users see error messages for networks being defined but not used, and occasionally run into problems where two containers can't talk to each other without tinkering with the networks. Neither of those happen under old menu. See [Issue 245](https://github.com/SensorsIot/IOTstack/issues/245) if you want more information on this.
3. New menu has moved the definition of environment variables into `docker-compose.yml`. Old menu keeps environment variables in "environment files" in `~/IOTstack/services`. There is no "right" or "better" about either approach. It's just something to be aware of.
4. Under new menu, the `service.yml` files in `~/IOTstack/.templates` have all been left-shifted by two spaces. That means you can no longer use copy and paste to test containers - you're stuck with the extra work of re-adding the spaces. Again, this doesn't *matter* but you do need to be aware of it.

What you give up when you choose old menu is summarised in the following. If a container appears on the right hand side but not the left then it is only available in new menu.

```
old-menu                master (new menu)
├── adminer             ├── adminer
├── blynk_server        ├── blynk_server
├── dashmachine         ├── dashmachine
├── deconz              ├── deconz
├── diyhue              ├── diyhue
├── domoticz            ├── domoticz
├── dozzle              ├── dozzle
├── espruinohub         ├── espruinohub
                      > ├── example_template
├── gitea               ├── gitea
├── grafana             ├── grafana
├── heimdall            ├── heimdall
                      > ├── home_assistant
├── homebridge          ├── homebridge
├── homer               ├── homer
├── influxdb            ├── influxdb
├── mariadb             ├── mariadb
├── mosquitto           ├── mosquitto
├── motioneye           ├── motioneye
├── nextcloud           ├── nextcloud
├── nodered             ├── nodered
├── openhab             ├── openhab
├── pihole              ├── pihole
├── plex                ├── plex
├── portainer           ├── portainer
├── portainer_agent     ├── portainer_agent
├── portainer-ce        ├── portainer-ce
├── postgres            ├── postgres
├── prometheus          ├── prometheus
├── python              ├── python
├── qbittorrent         ├── qbittorrent
├── rtl_433             ├── rtl_433
├── tasmoadmin          ├── tasmoadmin
├── telegraf            ├── telegraf
├── timescaledb         ├── timescaledb
├── transmission        ├── transmission
├── webthings_gateway   ├── webthings_gateway
├── wireguard           ├── wireguard
└── zigbee2mqtt         ├── zigbee2mqtt
                      > └── zigbee2mqtt_assistant
```

You also give up the `compose-override.yml` functionality. On the other hand, Docker has its own `docker-compose.override.yml` which works with both menus.

If you want to switch to the old menu:

```
$ git checkout old-menu
```

Any time you want to switch back to the new menu:

```
$ git checkout master
```

You can switch back and forth as much as you like and as often as you like. It's no harm, no foul. The branch you are on just governs what you see when you run:

```
$ ./menu.sh
```

Although you can freely change branches, it's probably not a good idea to try to mix-and-match your menus. Pick one menu and stick to it.

Even so, nothing will change **until** you run your chosen menu to completion and allow it to generate a new `docker-compose.yml`.

### <a name="upStack"> Step 5 – Bring up your stack </a>

Unless you have gotten ahead of yourself and have already run the menu (old or new) then nothing will have changed in the parts of your `~/IOTstack` folder that define your IOTstack implementation. You can safely:

```
$ docker-compose up -d
```

## <a name="seeAlso"> See also </a>

There is another gist [Installing Docker for IOTstack](https://gist.github.com/Paraphraser/d119ae81f9e60a94e1209986d8c9e42f) which explains how to overcome problems with outdated Docker and Docker-Compose installations.

Depending on the age of your gcgarner installation, you **may** run into problems which will be cured by working through that gist. 
