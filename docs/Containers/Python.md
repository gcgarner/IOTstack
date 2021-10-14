# Python

## <a name="references"> references </a>

* [Python.org](https://www.python.org)
* [Dockerhub image library](https://hub.docker.com/_/python)
* [GitHub docker-library/python](https://github.com/docker-library/python)

## <a name="menuPython"> selecting Python in the IOTstack menu </a>

When you select Python in the menu:

1. The following folder and file structure is created:

	```
	$ tree ~/IOTstack/services/python
	/home/pi/IOTstack/services/python
	├── app
	│   └── app.py
	├── docker-entrypoint.sh
	└── Dockerfile
	```

	Note:

	* Under "old menu" (old-menu branch), the `service.yml` is also copied into the `python` directory but is then not used.

2. This service definition is added to your `docker-compose.yml`:

	```yaml
	python:
	  container_name: python
	  build: ./services/python/.
	  restart: unless-stopped
	  environment:
	  - TZ=Etc/UTC
	  - IOTSTACK_UID=1000
	  - IOTSTACK_GID=1000
	# ports:
	#   - "external:internal"
	  volumes:
	  - ./volumes/python/app:/usr/src/app
	  networks:
	  - iotstack_nw
	```

	Note:

	* This service definition is for "new menu" (master branch). The only difference with "old menu" (old-menu branch) is the omission of the last two lines.

### <a name="customisingPython"> customising your Python service definition </a>

The service definition contains a number of customisation points:

1. `restart: unless-stopped` assumes your Python script will run in an infinite loop. If your script is intended to run once and terminate, you should remove this directive.
2. `TZ=Etc/UTC` should be set to your local time-zone. Never use quote marks on the right hand side of a `TZ=` variable.
3. If you are running as a different user ID, you may want to change both `IOTSTACK_UID` and `IOTSTACK_GID` to appropriate values.

	Notes:

	* Don't use user and group *names* because these variables are applied *inside* the container where those names are (probably) undefined.
	* The only thing these variables affect is the ownership of:

		```
		~/IOTstack/volumes/python/app
		```

		and its contents. If you want everything to be owned by root, set both of these variables to zero (eg `IOTSTACK_UID=0`).

4. If your Python script listens to data-communications traffic, you can set up the port mappings by uncommenting the `ports:` directive.

If your Python container is already running when you make a change to its service definition, you can apply it via:

```bash
$ cd ~/IOTstack
$ docker-compose up -d python
```

## <a name="firstLaunchPython"> Python - first launch </a>

After running the menu, you are told to run the commands:

```
$ cd ~/IOTstack
$ docker-compose up -d
```

This is what happens:

1. *docker-compose* reads your `docker-compose.yml`.
2. When it finds the service definition for Python, it encounters:

	```
	build: ./services/python/.
	```

	The leading period means "the directory containing `docker-compose.yml` while the trailing period means "Dockerfile", so the path expands to:

	```
	~/IOTstack/services/python/Dockerfile
	```

3. The `Dockerfile` is processed. It downloads the **base** image for Python from Dockerhub and then makes changes including:

	* copying the contents of the following directory into the image as a set of defaults:

		```
		/home/pi/IOTstack/services/python/app
		```

	* copying the following file into the image:

		```
		/home/pi/IOTstack/services/python/docker-entrypoint.sh
		```

		The `docker-entrypoint.sh` script runs each time the container launches and performs initialisation and "self repair" functions.

	The output of the Dockerfile run is a new **local** image tagged with the name `iotstack_python`.

4. The `iotstack_python` image is instantiated to become the running container.
5. When the container starts, the `docker-entrypoint.sh` script runs and initialises the container's persistent storage area:

	```bash
	$ tree -pu ~/IOTstack/volumes
	/home/pi/IOTstack/volumes
	└── [drwxr-xr-x root    ]  python
	    └── [drwxr-xr-x pi      ]  app
	        └── [-rwxr-xr-x pi      ]  app.py
	```

	Note:

	* the top-level `python` folder is owned by "root" but the `app` directory and its contents are owned by "pi".

5. The initial `app.py` Python script is a "hello world" placeholder. It runs as an infinite loop emitting messages every 10 seconds until terminated. You can see what it is doing by running:

	```bash
	$ docker logs -f python
	The world is born. Hello World.
	The world is re-born. Hello World.
	The world is re-born. Hello World.
	…
	```

	Pressing <kbd>control</kbd>+<kbd>c</kbd> terminates the log display but does not terminate the running container.

## <a name="stopPython"> stopping the Python service </a>

To stop the container from running, either:

* take down your whole stack:

	```bash
	$ cd ~/IOTstack
	$ docker-compose down
	```

* terminate the python container

	```bash
	$ cd ~/IOTstack
	$ docker-compose rm --force --stop -v python
	```

## <a name="startPython"> starting the Python service </a>

To bring up the container again after you have stopped it, either:

* bring up your whole stack:

	```bash
	$ cd ~/IOTstack
	$ docker-compose up -d
	```

* bring up the python container

	```bash
	$ cd ~/IOTstack
	$ docker-compose up -d python
	```

## <a name="reLaunchPython"> Python - second-and-subsequent launch </a>

Each time you launch the Python container *after* the first launch:

1. The existing local image (`iotstack_python`) is instantiated to become the running container.
2. The `docker-entrypoint.sh` script runs and performs "self-repair" by replacing any files that have gone missing from the persistent storage area. Self-repair does **not** overwrite existing files! 
3. The `app.py` Python script is run.

## <a name="debugging"> when things go wrong - check the log </a>

If the container misbehaves, the log is your friend:

```
$ docker logs python
```

## <a name="yourPythonScript"> project development life-cycle </a>

It is **critical** that you understand that **all** of your project development should occur within the folder:

```
~/IOTstack/volumes/python/app
```

So long as you are performing some sort of routine backup (either with a supplied script or a third party solution like [Paraphraser/IOTstackBackup](https://github.com/Paraphraser/IOTstackBackup)), your work will be protected.

### <a name="gettingStarted"> getting started </a>

Start by editing the file:

```
~/IOTstack/volumes/python/app/app.py
```

If you need other supporting scripts or data files, also add those to the directory:

```
~/IOTstack/volumes/python/app
```

Any time you change something in the `app` folder, tell the running python container to notice the change by:

```bash
$ cd ~/IOTstack
$ docker-compose restart python
```

### <a name="persistentStorage"> reading and writing to disk </a>

Consider this line in the service definition:

```
- ./volumes/python/app:/usr/src/app
```

The leading period means "the directory containing `docker-compose.yml`" so it the same as:

```
- ~/IOTstack/volumes/python/app:/usr/src/app
```

Then, you split the line at the ":", resulting in:

* The *external* directory = `~/IOTstack/volumes/python/app`
* The *internal* directory = `/usr/src/app`

What it means is that:

* Any file you put into the *external* directory (or any sub-directories you create within the *external* directory) will be visible to your Python script running inside the container at the same relative position in the *internal* directory.
* Any file or sub-directory created in the *internal* directory by your Python script running inside the container will be visible outside the container at the same relative position in the *external* directory.
* The contents of *external* directory and, therefore, the *internal* directory will persist across container launches.

If your script writes into any other directory inside the container, the data will be lost when the container re-launches.

### <a name="cleanSlate"> getting a clean slate </a>

If you make a mess of things and need to start from a clean slate, erase the persistent storage area:

```bash
$ cd ~/IOTstack
$ docker-compose rm --force --stop -v python
$ sudo rm -rf ./volumes/python
$ docker-compose up -d python
```

The container will re-initialise the persistent storage area from its defaults.

### <a name="addingPackages"> adding packages </a>

As you develop your project, you may find that you need to add supporting packages. For this example, we will assume you want to add "[Flask](https://pypi.org/project/Flask/)" and "[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)".

If you were developing a project outside of container-space, you would simply run:

```
$ pip3 install -U Flask beautifulsoup4
```

You *can* do the same thing with the running container:

```
$ docker exec python pip3 install -U Flask beautifulsoup4
```

and that will work&nbsp;—&nbsp;until the container is re-launched, at which point the added packages will disappear.

To make *Flask* and *beautifulsoup4* a permanent part of your container:

1. Change your working directory:

	```
	$ cd ~/IOTstack/services/python/app
	```

2. Use your favourite text editor to create the file `requirements.txt` in that directory. Each package you want to add should be on a line by itself:

	```
	Flask
	beautifulsoup4
	``` 

3. Tell Docker to rebuild the local Python image:

	```
	$ cd ~/IOTstack
	$ docker-compose build --force-rm python
	$ docker-compose up -d --force-recreate python
	$ docker system prune -f
	```

	Note:

	* You will see a warning about running pip as root - ignore it.

4. Confirm that the packages have been added:

	```
	$ docker exec python pip3 freeze | grep -e "Flask" -e "beautifulsoup4"
	beautifulsoup4==4.10.0
	Flask==2.0.1
	```

5. Continue your development work by returning to [getting started](#gettingStarted).

Note:

* The first time you following the process described above to create `requirements.txt`, a copy will appear at:

	```
	~/IOTstack/volumes/python/app/requirements.txt
	```

	This copy is the result of the "self-repair" code that runs each time the container starts noticing that `requirements.txt` is missing and making a copy from the defaults stored inside the image.

	If you make more changes to the master version of `requirements.txt` in the *services* directory and rebuild the local image, the copy in the *volumes* directory will **not** be kept in-sync. That's because the "self-repair" code **never** overwrites existing files.

	If you want to bring the copy of `requirements.txt` in the *volumes* directory up-to-date:

	```
	$ cd ~/IOTstack
	$ rm ./volumes/python/app/requirements.txt
	$ docker-compose restart python
	```

	The `requirements.txt` file will be recreated and it will be a copy of the version in the *services* directory as of the last image rebuild.

### <a name="scriptBaking"> making your own Python script the default </a>

Suppose the Python script you have been developing reaches a major milestone and you decide to "freeze dry" your work up to that point so that it becomes the default when you ask for a [clean slate](#cleanSlate). Proceed like this:

1. If you have added any packages by following the steps in [adding packages](#addingPackages), run the following command:

	```bash
	$ docker exec python bash -c 'pip3 freeze >requirements.txt'
	```

	That generates a `requirements.txt` representing the state of play inside the running container. Because it is running *inside* the container, the `requirements.txt` created by that command appears *outside* the container at:

	```
	~/IOTstack/volumes/python/app/requirements.txt
	```

2. Make your work the default:

	```bash
	$ cd ~/IOTstack
	$ cp -r ./volumes/python/app/* ./services/python/app
	```

	The `cp` command copies:

	* your Python script;
	* the optional `requirements.txt` (from step 1); and
	* any other files you may have put into the Python working directory.

	Key point:

	* **everything** copied into `./services/python/app` will become part of the new local image.

3. Terminate the Python container and erase its persistent storage area:

	```bash
	$ cd ~/IOTstack
	$ docker-compose rm --force --stop -v python
	$ sudo rm -rf ./volumes/python
	```

	Note:

	* If erasing the persistent storage area feels too risky, just move it out of the way:

		```
		$ cd ~/IOTstack/volumes
		$ sudo mv python python.off
		```

4. Rebuild the local image:

	```bash
	$ cd ~/IOTstack
	$ docker-compose build --force-rm python
	$ docker-compose up -d --force-recreate python
	```

	On its first launch, the new container will re-populate the persistent storage area but, this time, it will be your Python script and any other supporting files, rather than the original "hello world" script.

5. Clean up by removing the old local image:

	```bash
	$ docker system prune -f
	```

### <a name="scriptCanning"> canning your project </a>

Suppose your project has reached the stage where you wish to put it into production as a service under its own name. Make two further assumptions:

1. You have gone through the steps in [making your own Python script the default](#scriptBaking) and you are **certain** that the content of `./services/python/app` correctly captures your project.
2. You want to give your project the name "wishbone".

Proceed like this:

1. Stop the development project:

	```
	$ cd ~/IOTstack
	$ docker-compose rm --force --stop -v python
	```

2. Remove the existing local image:

	```
	$ docker rmi iotstack_python
	```

3. Rename the `python` services directory to the name of your project:

	```
	$ cd ~/IOTstack/services
	$ mv python wishbone
	```

4. Edit the `python` service definition in `docker-compose.yml` and replace references to `python` with the name of your project. In the following, the original is on the left, the edited version on the right, and the lines that need to change are indicated with a "|": 

	```
	python:                                  |  wishbone:
	  container_name: python                 |    container_name: wishbone
	  build: ./services/python/.             |    build: ./services/wishbone/.
	  restart: unless-stopped                     restart: unless-stopped
	  environment:                                environment:
	    - TZ=Etc/UTC                                - TZ=Etc/UTC
	    - IOTSTACK_UID=1000                         - IOTSTACK_UID=1000
	    - IOTSTACK_GID=1000                         - IOTSTACK_GID=1000
	  # ports:                                    # ports:
	  #   - "external:internal"                   #   - "external:internal"
	  volumes:                                    volumes:
	    - ./volumes/python/app:/usr/src/app  |      - ./volumes/wishbone/app:/usr/src/app
	  networks:                                   networks:
	    - iotstack_nw                               - iotstack_nw
	```

	Note:

	* if you make a copy of the `python` service definition and then perform the required "wishbone" edits on the copy, the `python` definition will still be active so `docker-compose` may try to bring up both services. You will eliminate the risk of confusing yourself if you follow these instructions "as written" by **not** leaving the `python` service definition in place.

5. Start the renamed service:

	```
	$ cd ~/IOTstack
	$ docker-compose up -d wishbone
	```

Remember:

* After you have done this, the persistent storage area will be at the path:

	```
	~/IOTstack/volumes/wishbone/app
	``` 

## <a name="routineMaintenance"> routine maintenance </a>

To make sure you are running from the most-recent **base** image of Python from Dockerhub:

```
$ cd ~/IOTstack
$ docker-compose build --no-cache --pull python
$ docker-compose up -d python
$ docker system prune -f
$ docker system prune -f
```

In words:

1. Be in the right directory.
2. Force docker-compose to download the most-recent version of the Python **base** image from Dockerhub, and then run the Dockerfile to build a new **local** image.
3. Instantiate the newly-built **local** image.
4. Remove the old **local** image.
5. Remove the old **base** image

The old base image can't be removed until the old local image has been removed, which is why the `prune` command needs to be run twice.

Note:

* If you have followed the steps in [canning your project](#scriptCanning) and your service has a name other than `python`, just substitute the new name where you see `python` in the two `dockerc-compose` commands.
