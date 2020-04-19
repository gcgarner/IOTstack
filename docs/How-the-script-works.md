# How the script works
The build script creates the ./services directory and populates it from the template file in .templates . The script then appends the text withing each service.yml file to the docker-compose.yml . When the stack is rebuild the menu doesn not overwrite the service folder if it already exists. Make sure to sync any alterations you have made to the docker-compose.yml file with the respective service.yml so that on your next build your changes pull through.

The .gitignore file is setup such that if you do a `git pull origin master` it does not overwrite the files you have already created. Because the build script does not overwrite your service directory any changes in the .templates directory will have no affect on the services you have already made. You will need to move your service folder out to get the latest version of the template.


