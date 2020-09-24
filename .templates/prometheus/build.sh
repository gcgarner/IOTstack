#!/bin/bash

DOCKER_COMPOSE_PATH=./.tmp/docker-compose.tmp.yml
TEMPLATE_PATH=./.templates/prometheus

if [[ ! -f $DOCKER_COMPOSE_PATH ]]; then
  echo "[Prometheus] Warning: $DOCKER_COMPOSE_PATH does not exist."
fi

# Configure Prometheus Add-ons

option_selection=$(whiptail --title "Select Prometheus Options" --checklist --separate-output \
  "Use the [SPACEBAR] to select add-on containers from the list below." 20 78 12 -- \
  "node-exporter" "monitor this computer " "ON" \
  "cadvisor-arm" "monitor full container stack " "ON" \
  3>&1 1>&2 2>&3)

mapfile -t selected_options <<< "$option_selection"

# (cat $TEMPLATE_PATH/service.yml; echo) >> $DOCKER_COMPOSE_PATH

for option in "${selected_options[@]}"; do
  # insert add-on service
  (cat $TEMPLATE_PATH/service_${option}.yml; echo) >> $DOCKER_COMPOSE_PATH

  # include add-on in depends_on
  sed -i.bak -e "/depends_on:/a\\
    \\ \\ \\ \\ \\ \\ - ${option}" $DOCKER_COMPOSE_PATH
done

# clean up
rm ${DOCKER_COMPOSE_PATH}.bak
