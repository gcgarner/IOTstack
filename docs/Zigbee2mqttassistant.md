# Zigbee2Mqtt Assistant
## References
- [Docker](https://hub.docker.com/r/carldebilly/zigbee2mqttassistant)
- [Website](https://github.com/yllibed/Zigbee2MqttAssistant/blob/master/README.md)

## About

This service a web frontend which displays Zigbee2Mqtt service messages and able to control it over Mqtt. For the 
servie a working Mqtt server is required and that have to be configured.

## Environment Parameters

Z2MA_SETTINGS__MQTTSERVER=mosquitto  - The mqtt service instance which is used by Zigbee2Mqtt instance.
Z2MA_SETTINGS__MQTTUSERNAME=<optional> - When mqtt server have authentication this user is used.
Z2MA_SETTINGS__MQTTPASSWORD=<optional> - When mqtt server have authentication this user is used.
TZ=Europe/Budapest <optional> - Recommmended to setup for correct timestamps.

## Accessing the UI
The  Zigbee2Mqtt Assistant UI is available using port 8880 (http://your.local.ip.address:8880/)
