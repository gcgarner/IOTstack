# Zigbe2MQTT
* [Web Guide](https://www.zigbee2mqtt.io/information/docker.html)

## First startup

After starting the stack check to see if there is an error due to missing device. This is because the devices are mapped differently on the Pi. If your device is not showing in the container then you can also follow the followings steps.

If you get a startup failure open the docker-compose.yml file and under zigbee2mqtt change this:

```yml
 devices:
      - /dev/ttyAMA0:/dev/ttyACM0
      #- /dev/ttyACM0:/dev/ttyACM0
```

to 

```yml
 devices:
      #- /dev/ttyAMA0:/dev/ttyACM0
      - /dev/ttyACM0:/dev/ttyACM0
```

and run docker-compose up -d again

If the container starts then run `docker logs zigbe2mqtt` so see the log output and if your device is recognised. You may need to reset the device for docker to see it.

To edit the configuration file `sudo nano volumes/zigbee2mqtt/data/configuration.yaml` you many need to restart the container for changes to take affect `docker-compose restart zigbee2mqtt`

Unfortunately I don't own a zigbee device and cannot offer support on the setup you will need to follow the website instructions for further instructions https://www.zigbee2mqtt.io/

## terminal access

to access the terminal run `docker exec -it zigbee2mqtt /bin/sh` or select `/bin/sh