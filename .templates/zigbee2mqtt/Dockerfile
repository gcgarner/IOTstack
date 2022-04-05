# This file is deprecated. It is being retained for backwards
# compatibility with existing docker-compose.yml files but will
# be removed, eventually.

# Download base image
FROM koenkk/zigbee2mqtt

# change default configuration.yaml to be IOTstack-friendly
# 1. expect the MQTT service to be in the Mosquitto container
# 2. enable the web front end on port 8080
RUN sed -i.bak \
   -e 's/mqtt:\/\/localhost/mqtt:\/\/mosquitto/' \
   -e '$s/$/\n\nfrontend:\n  port: 8080\n# auth_token: PASSWORD\n/' \
   /app/configuration.yaml

RUN echo "*** DEPRECATION NOTICE: Please read IOTstack Zigbee2MQTT documentation:"
RUN echo "*** https://sensorsiot.github.io/IOTstack/Containers/Zigbee2MQTT/"

# EOF
