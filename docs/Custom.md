# Custom services and overriding default settings for IOTstack
You can specify modifcations to the `docker-compose.yml` file, including your own networks and custom containers/services.

Create a file called `compose-override.yml` in the main directory, and place your modifications into it. These changes will be merged into the `docker-compose.yml` file next time you run the build script.

The `compose-override.yml` file has been added to the `.gitignore` file, so it shouldn't be touched when upgrading IOTstack. It has been added to the backup script, and so will be included when you back up and restore IOTstack. Always test your backups though! New versions of IOTstack may break previous builds.

## How it works
1. After the build process has been completed, a temporary docker compose file is created in the `tmp` directory.
2. The script then checks if `compose-override.yml` exists:
    * If it exists, then continue to step `3`
    * If it does not exist, copy the temporary docker compose file to the main directory and rename it to `docker-compose.yml`.
3. Using the `yaml_merge.py` script, merge both the `compose-override.yml` and the temporary docker compose file together; Using the temporary file as the default values and interating through each level of the yaml structure, check to see if the `compose-override.yml` has a value set.
4. Output the final file to the main directory, calling it `docker-compose.yml`.

## A word of caution
If you specify an override for a service, and then rebuild the `docker-compose.yml` file, but deselect the service from the list, then the YAML merging will still produce that override.

For example, lets say NodeRed was selected to have have the following override specified in `compose-override.yml`:
```
services:
  nodered:
    restart: always
```

When rebuilding the menu, ensure to have NodeRed service always included because if it's no longer included, the only values showing in the final `docker-compose.yml` file for NodeRed will be the `restart` key and its value. Docker Compose will error with the following message:
```
Service nodered has neither an image nor a build context specified. At least one must be provided.
```

When attempting to bring the services up with `docker-compose up -d`.

Either remove the override for NodeRed in `compose-override.yml` and rebuild the stack, or ensure that NodeRed is built with the stack to fix this.

## Examples

### Overriding default settings
Lets assume you put the following into the `compose-override.yml` file:
```
services:
  mosquitto:
    ports:
      - 1996:1996
      - 9001:9001
```

Normally the mosquitto service would be built like this inside the `docker-compose.yml` file:
```
version: '3.6'
services:
  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto
    restart: unless-stopped
    user: "1883"
    ports:
      - 1883:1883
      - 9001:9001
    volumes:
      - ./volumes/mosquitto/data:/mosquitto/data
      - ./volumes/mosquitto/log:/mosquitto/log
      - ./volumes/mosquitto/pwfile:/mosquitto/pwfile
      - ./services/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./services/mosquitto/filter.acl:/mosquitto/config/filter.acl
```

Take special note of the ports list.

If you run the build script with the `compose-override.yml` file in place, and open up the final `docker-compose.yml` file, you will notice that the port list have been replaced with the ones you specified in the `compose-override.yml` file.
```
version: '3.6'
services:
  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto
    restart: unless-stopped
    user: "1883"
    ports:
      - 1996:1996
      - 9001:9001
    volumes:
      - ./volumes/mosquitto/data:/mosquitto/data
      - ./volumes/mosquitto/log:/mosquitto/log
      - ./volumes/mosquitto/pwfile:/mosquitto/pwfile
      - ./services/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./services/mosquitto/filter.acl:/mosquitto/config/filter.acl
```

Do note that it will replace the entire list, if you were to specify
```
services:
  mosquitto:
    ports:
      - 1996:1996
```

Then the final output will be:
```
version: '3.6'
services:
  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto
    restart: unless-stopped
    user: "1883"
    ports:
      - 1996:1996
    volumes:
      - ./volumes/mosquitto/data:/mosquitto/data
      - ./volumes/mosquitto/log:/mosquitto/log
      - ./volumes/mosquitto/pwfile:/mosquitto/pwfile
      - ./services/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./services/mosquitto/filter.acl:/mosquitto/config/filter.acl
```

### Adding custom services

Custom services can be added in a similar way to overriding default settings for standard services. Lets add a Minecraft and rcon server to IOTstack.
Firstly, put the following into `compose-override.yml`:
```
services:
  mosquitto:
    ports:
      - 1996:1996
      - 9001:9001
  minecraft:
    image: itzg/minecraft-server
    ports:
      - "25565:25565"
    volumes:
      - "./volumes/minecraft:/data"
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "PASSWORD"
      RCON_PORT: 28016
      VERSION: "1.15.2"
      REPLACE_ENV_VARIABLES: "TRUE"
      ENV_VARIABLE_PREFIX: "CFG_"
      CFG_DB_HOST: "http://localhost:3306"
      CFG_DB_NAME: "IOTstack Minecraft"
      CFG_DB_PASSWORD_FILE: "/run/secrets/db_password"
    restart: unless-stopped
  rcon:
    image: itzg/rcon
    ports:
      - "4326:4326"
      - "4327:4327"
    volumes:
      - "./volumes/rcon_data:/opt/rcon-web-admin/db"
secrets:
  db_password:
    file: ./db_password
```

Then create the service directory that the new instance will use to store persistant data:

`mkdir -p ./volumes/minecraft`

and

`mkdir -p ./volumes/rcon_data`

Obviously you will need to give correct folder names depending on the `volumes` you specify for your custom services. If your new service doesn't require persistant storage, then you can skip this step.

Then simply run the `./menu.sh` command, and rebuild the stack with what ever services you had before.

Using the Mosquitto example above, the final `docker-compose.yml` file will look like:

```
version: '3.6'
services:
  mosquitto:
    ports:
    - 1996:1996
    - 9001:9001
    container_name: mosquitto
    image: eclipse-mosquitto
    restart: unless-stopped
    user: '1883'
    volumes:
    - ./volumes/mosquitto/data:/mosquitto/data
    - ./volumes/mosquitto/log:/mosquitto/log
    - ./services/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
    - ./services/mosquitto/filter.acl:/mosquitto/config/filter.acl
  minecraft:
    image: itzg/minecraft-server
    ports:
    - 25565:25565
    volumes:
    - ./volumes/minecraft:/data
    environment:
      EULA: 'TRUE'
      TYPE: PAPER
      ENABLE_RCON: 'true'
      RCON_PASSWORD: PASSWORD
      RCON_PORT: 28016
      VERSION: 1.15.2
      REPLACE_ENV_VARIABLES: 'TRUE'
      ENV_VARIABLE_PREFIX: CFG_
      CFG_DB_HOST: http://localhost:3306
      CFG_DB_NAME: IOTstack Minecraft
      CFG_DB_PASSWORD_FILE: /run/secrets/db_password
    restart: unless-stopped
  rcon:
    image: itzg/rcon
    ports:
    - 4326:4326
    - 4327:4327
    volumes:
    - ./volumes/rcon_data:/opt/rcon-web-admin/db
secrets:
  db_password:
    file: ./db_password
```

Do note that the order of the YAML keys is not guaranteed.
