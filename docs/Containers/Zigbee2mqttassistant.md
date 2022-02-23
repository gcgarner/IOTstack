# Zigbee2Mqtt Assistant

## References

- [Docker](https://hub.docker.com/r/carldebilly/zigbee2mqttassistant)
- [Website](https://github.com/yllibed/Zigbee2MqttAssistant/blob/master/README.md)

## About

This service a web frontend which displays Zigbee2Mqtt service messages and able to control it over MQTT. For the 
servie a working MQTT server is required and that have to be configured.

## Environment Parameters

* `Z2MA_SETTINGS__MQTTSERVER=mosquitto` - The MQTT service instance which is used by Zigbee2Mqtt instance. Here, "mosquitto" is the name of the container.
* `Z2MA_SETTINGS__MQTTUSERNAME=name` - Used if your MQTT service has authentication enabled. Optional.
* `Z2MA_SETTINGS__MQTTPASSWORD=password` - Used if your MQTT service has authentication enabled. Optional.
* `TZ=Etc/UTC`- Set to your timezone. Optional but recommended.

## Accessing the UI

The Zigbee2Mqtt Assistant UI is available using port 8880. For example:

* `http://your.local.ip.address:8880/`
