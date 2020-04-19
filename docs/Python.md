# Python
* [Docker hub](https://hub.docker.com/_/python)

## Running python code in docker

In order to run code in docker the container needs to be build from a Dockerfile. There are 2 key files in the service directory

### services/python/requirements.txt

Normally on your system you would install modules with pip and they would be available system wide. The container that comes off Docker hub is blank and we will have to install them and bake them into the container. Before your first run add the modules that you require to the requirements.txt, each on a new line

```
flask
bs4
```
**IMPORTANT**: Every time you alter the requirements file you will need to rebuild the container and bake in the new modules

To build the container run `docker-compose build python`. 

### services/python/service.yml

This is the template that gets concatenated into docker-compose.yml and there are a few things to note here

```yml
  python:
    container_name: python
    build: ./services/python/.
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./volumes/python/app:/usr/src/app
```

The container runs in host network mode. This is because i have no idea which ports you want to use. The implication of this is you will not be able to connect by name to the other container and therefore if you want to connect to the mqtt service or influx you will need to use `localhost` or `127.0.0.1` because the python container "thinks" from network perspective that it is the Pi

The container is set to restart unless stopped. Therefore if you write an application it will effectively execute in an endless loop. If you only want a run once method then you will need to comment out the "restart" section in the docker-compose.yml file and the service.yml

## Where to put your code

You will need to copy your code to `IOTstack/volumes/python/app`. The container is set to execute `app.py` as the main file.

### writing to the console

If you execute a print statement the text will appear in the console of the container. The output can be accessed by running `docker logs python`

### writing to disk
Inside the container the working directory is `/usr/src/app` as mapped in the volume command. It would be advised to read or write any data from this directory.

## Image clutter

Doing multiple builds of the python image will create many unused images. These can be cleaned up inside portainer or by running `./scripts/prune-images.sh`
