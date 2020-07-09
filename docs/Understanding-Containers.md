# Let’s begin by understanding, What is Docker?

In simple terms, Docker is a software platform that simplifies the process of building, running, 
managing and distributing applications. It does this by virtualizing the operating system of the 
computer on which it is installed and running.

# The Problem
Let’s say you have three different Python-based applications that you plan to host on a single server 
(which could either be a physical or a virtual machine).

Each of these applications makes use of a different version of Python, as well as the associated 
libraries and dependencies, differ from one application to another.

Since we cannot have different versions of Python installed on the same machine, this prevents us from 
hosting all three applications on the same computer.

# The Solution
Let’s look at how we could solve this problem without making use of Docker. In such a scenario, we 
could solve this problem either by having three physical machines, or a single physical machine, which 
is powerful enough to host and run three virtual machines on it.

Both the options would allow us to install different versions of Python on each of these machines, 
along with their associated dependencies.

The machine on which Docker is installed and running is usually referred to as a Docker Host or Host in
simple terms. So, whenever you plan to deploy an application on the host, it would create a logical 
entity on it to host that application. In Docker terminology, we call this logical entity a Container or 
Docker Container to be more precise.

Whereas the kernel of the host’s operating system is shared across all the containers that are running 
on it.

This allows each container to be isolated from the other present on the same host. Thus it supports 
multiple containers with different application requirements and dependencies to run on the same host, 
as long as they have the same operating system requirements.

# Docker Terminology

Docker Images and Docker Containers are the two essential things that you will come across daily while 
working with Docker.

In simple terms, a Docker Image is a template that contains the application, and all the dependencies 
required to run that application on Docker.

On the other hand, as stated earlier, a Docker Container is a logical entity. In more precise terms, 
it is a running instance of the Docker Image.

# What is Docker-Compose?

Docker Compose provides a way to orchestrate multiple containers that work together. Docker compose 
is a simple yet powerful tool that is used to run multiple containers as a single service. 
For example, suppose you have an application which requires Mqtt as a communication service between IOT devices
and OpenHAB instance as a Smarthome application service. In this case by docker-compose, you can create one 
single file (docker-compose.yml) which will create both the containers as a single service without starting 
each separately. It wires up the networks (literally), mounts all volumes and exposes the ports.

The IOTstack with the templates and menu is a generator for that docker-compose service descriptor.

# How Docker Compose Works?

use yaml files to configure application services (docker-compose.yaml)
can start all the services with a single command ( docker-compose up )
can stop all the service with a single command ( docker-compose down )

# How are the containers connected
The containers are automagically connected when we run the stack with docker-compose up. 
The containers using same logical network (by default) where the instances can access each other with the instance 
logical name. Means if there is an instance called *mosquitto* and an *openhab*, when openHAB instance need
to access mqtt on that case the domain name of mosquitto will be resolved as the runnuning instance of mosquitto.

# How the container are connected to host machine

## Volumes

The containers are enclosed processes which state are lost with the restart of container. To be able to 
persist states volumes (images or directories) can be used to share data with the host. 
Which means if you need to persist some database, configuration or any state you have to bind volumes where the 
running service inside the container will write files to that binded volume.
In order to understand what a Docker volume is, we first need to be clear about how the filesystem normally works 
in Docker. Docker images are stored as series of read-only layers. When we start a container, Docker takes 
the read-only image and adds a read-write layer on top. If the running container modifies an existing file, 
the file is copied out of the underlying read-only layer and into the top-most read-write layer where the 
changes are applied. The version in the read-write layer hides the underlying file, but does not 
destroy it -- it still exists in the underlying layer. When a Docker container is deleted, 
relaunching the image will start a fresh container without any of the changes made in the previously 
running container -- those changes are lost, thats the reason that configs, databases are not persisted,

Volumes are the preferred mechanism for persisting data generated by and used by Docker containers.
While bind mounts are dependent on the directory structure of the host machine, volumes are completely 
managed by Docker. In IOTstack project uses the volumes directory in general to bind these container volumes.

## Ports
When containers running a we would like to delegate some services to the outside world, for example
OpenHAB web frontend have to be accessible for users. There are several ways to achive that. One is
mounting the port to the most machine, this called port binding. On that case service will have a dedicated
port which can be accessed, one drawback is one host port can be used one serice only. Another way is reverse proxy. 
The term reverse proxy (or Load Balancer in some terminology) is normally applied to a service that sits in front 
of one or more servers (in our case containers), accepting requests from clients for resources located on the 
server(s). From the client point of view, the reverse proxy appears to be the web server and so is 
totally transparent to the remote user. Which means several service can share same port the server
will route the request by the URL (virtual domain or context path). For example, there is *grafana* and *openHAB*
instances, where the *opeanhab.domain.tld* request will be routed to openHAB instance 8181 port while 
*grafana.domain.tld* to grafana instance 3000 port. On that case the proxy have to be mapped for host port 80 and/or
444 on host machine, the proxy server will access the containers via the docker virtual network.


Source materials used:

https://takacsmark.com/docker-compose-tutorial-beginners-by-example-basics/
https://www.freecodecamp.org/news/docker-simplified-96639a35ff36/
https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/
https://blog.container-solutions.com/understanding-volumes-docker

