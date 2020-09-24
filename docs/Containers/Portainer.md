# Portainer
## References 
- [Docker](https://hub.docker.com/r/portainer/portainer/)
- [Website](https://www.portainer.io/)

## Portainer restart by itself

There is an issue with the armhf Portainer image where it randomly restarts. This does not affect its operation. The bug has been reported.

## About

Portainer is a great application for managing Docker. In your web browser navigate to `#yourip:9000`. You will be asked to choose a password. In the next window select 'Local' and connect, it shouldn't ask you this again. From here you can play around, click local, and take a look around. This can help you find unused images/containers. On the Containers section, there are 'Quick actions' to view logs and other stats. Note: This can all be done from the CLI but portainer just makes it much much easier. 

## Setup Public IP

When you first run Portainer and navigate to the Containers list you will see that there is a clickable link to the ports however this will direct you to `0.0.0.0:port`. This is because Portainer doesn't know your IP address. This can be set in the endpoint

![image](https://user-images.githubusercontent.com/46672225/69695462-26a31a80-10e5-11ea-991d-24b7282c8963.png)

and set the public IP

![image](https://user-images.githubusercontent.com/46672225/69695485-3c184480-10e5-11ea-85f7-8385ac339d76.png)

## Forgotten password

If you have forgotten the password you created for the container, stop the stack remove portainers volume with `sudo rm -r ./volumes/portainer` and start the stack. Your browser may get a little confused when it restarts. Just navigate to "yourip:9000" (may require more than one attempt) and create your new login details. If it doesn't ask you to connect to the 'Local' docker or shows an empty endpoint just logout and log back in and it will give you the option. From now on it should just work fine.