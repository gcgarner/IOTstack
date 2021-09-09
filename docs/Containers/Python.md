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
	
	Notes:
	
	* This service definition is for "new menu" (master branch). The only difference with "old menu" (old-menu branch) is the omission of the last two lines.
	* See also [customising your Python service definition](#customisingPython).


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

## <a name="yourPythonScript"> developing your own Python script </a>

1. Edit (or replace) the file:

	```
	~/IOTstack/volumes/python/app/app.py
	```
	
2. Tell the python container to notice the change by:

	```bash
	$ cd ~/IOTstack
	$ docker-compose restart python
	```
	
## <a name="debugging"> when things go wrong - check the log </a>

If the container misbehaves, the log is your friend:

```
$ docker logs python
```

## <a name="cleanSlate"> getting a clean slate </a>

If you make a mess of things and need to start from a clean slate:

```bash
$ cd ~/IOTstack
$ docker-compose rm --force --stop -v python
$ sudo rm -rf ./volumes/python
$ docker-compose up -d python
```

The container will re-initialise the persistent storage area from its defaults.

## <a name="bakingPython"> making your own Python script the default </a>

Suppose you have been developing a Python script and you want to "freeze dry" everything into an image so that it becomes the default when you ask for a clean slate.

1. If you have identified a need for a `requirements.txt`, create that by running the following command:

	```bash
	$ docker exec python bash -c 'pip3 freeze >requirements.txt'
	```
	
	That creates a file at the following path (it will be owned by root):
	
	```
	~/IOTstack/volumes/python/app/requirements.txt
	```

2. Run the following commands:

	```bash
	$ cd ~/IOTstack
	$ cp -r ./volumes/python/app/* ./services/python/app
	```

	The `cp` command copies:
	
	* your Python script;
	* the optional `requirements.txt`; and
	* any other files you may have put into the Python working directory.

	Key point:
	
	* **everything** copied into the `./services/python/app` directory will become part of the new image.

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
	$ cd ~IOTstack
	$ docker-compose up --build -d python
	```
	
	The `--build` directive will trigger a new Dockerfile run which, in turn, will process the (optional) `requirements.txt` and then bundle your Python application and any other supporting folders and files into a new local image, and then instantiate that to be the new running container.
	
	On its first launch, the new container will re-populate the persistent storage area but, this time it will be your Python script and any other supporting files, rather than the original "hello world" script.
	
5. Clean up by removing the old local image:

	```bash
	$ docker system prune -f
	```

## <a name="customisingPython"> customising your Python service definition </a>

The service definition shown in [selecting Python in the menu](#menuPython) contains a number of customisation points:

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

After making a change to the service definition, you can apply it via:

```bash
$ cd ~/IOTstack
$ docker-compose up -d python
```

## <a name="persistentStorage"> writing to disk </a>

Inside the container the working directory is `/usr/src/app` (ie as mapped in the `volumes:` directive of the service definition). Any data your Python script writes into this directory (or a sub-directory) will persist across container launches.

If your script writes into any other directory inside the container, the data will be lost when the container re-launches.

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
