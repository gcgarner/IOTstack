# Download base image
FROM koenkk/zigbee2mqtt

# change default configuration.yaml to be IOTstack-friendly
# 1. expect the MQTT service to be in the Mosquitto container
# 2. enable the web front end on port 8080
RUN sed -i.bak \
   -e 's/mqtt:\/\/localhost/mqtt:\/\/mosquitto/' \
   -e '$s/$/\n\nfrontend:\n  port: 8080\n# auth_token: PASSWORD\n/' \
   /app/configuration.yaml

# EOF
