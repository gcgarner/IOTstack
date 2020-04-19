# Custom container
If you have a container that you want to stop and start with the stack you can now use the custom container option. This you can use for testing or in prep for a Pull Request.

You will need to create a directory for your container call `IOTstack/services/<container>`

Inside that container create a `service.yml` containing your service and configurations. Have a look at one of the other services for inspiration.

Create a file called `IOTstack/services/custom.txt` and and enter your container names, one per line

Run the menu.sh and build the stack. After you have made the selection you will be asked if you want to add the custom containers.

Now your container will be part of the docker-compose.yml file and will respond to the docker-compose up -d commands.

Docker creates volumes under root and your container may require different ownership on the volume directory. You can see an example of the workaround for this in the python template in `IOTstack/.templates/python/directoryfix.sh`