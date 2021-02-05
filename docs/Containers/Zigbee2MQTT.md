# Zigbee2MQTT
* [Web Guide](https://www.zigbee2mqtt.io/information/docker.html)

## First startup

After starting the stack check to see if there is an error due to missing device. This is because the devices are mapped differently on the Pi. If your device is not showing in the container then you can also follow the followings steps.

If you get a startup failure open the docker-compose.yml file and under zigbee2mqtt change device to map to container (uncomment one of alternatives):

```yml
 devices:
      - /dev/ttyAMA0:/dev/ttyACM0
      #- /dev/ttyACM0:/dev/ttyACM0
      #- /dev/ttyUSB0:/dev/ttyACM0 # Electrolama zig-a-zig-ah! (zzh!) maybe other as well
```

and run docker-compose up -d again

If the container starts then run `docker logs zigbee2mqtt` so see the log output and if your device is recognised. You may need to reset the device for docker to see it.

To edit the configuration file `sudo nano volumes/zigbee2mqtt/data/configuration.yaml` you many need to restart the container for changes to take affect `docker-compose restart zigbee2mqtt`

Please follow instructions on https://www.zigbee2mqtt.io/

## terminal access

To access the terminal run `docker exec -it zigbee2mqtt /bin/sh`
