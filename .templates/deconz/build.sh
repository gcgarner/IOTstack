#!/bin/bash

#deCONZ device configuration

DOCKER_COMPOSE_PATH=./.tmp/docker-compose.tmp.yml

if [[ ! -f $DOCKER_COMPOSE_PATH ]]; then
        echo "[deCONZ] Warning: $DOCKER_COMPOSE_PATH does not exist."
fi

device_selection=$(whiptail --radiolist --title "Select deCONZ gateway" --notags \
        "Use the [SPACEBAR] to select your deCONZ gateway from the list below AND MAKE SURE IT IS PLUGGED IN (if not, press [ESC])." 20 78 12 \
        "ConBeeII" "ConBee II " "ON" \
        "ConBee" "ConBee " "OFF" \
        "RaspBee" "RaspBee " "OFF" \
        3>&1 1>&2 2>&3)

        case $device_selection in

                        "ConBeeII")
                                if [[ ! -f ./.templates/deconz/service_conbee_II.yml ]]; then
                                        echo "Error: ./.templates/deconz/service_conbee_II.yml does not exist."
                                else
                                        cat ./.templates/deconz/service_conbee_II.yml >> $DOCKER_COMPOSE_PATH
                                        echo "...copied ConBee II config from template"
                                fi
                                ;;
                        "ConBee")
                                if [[ ! -f ./.templates/deconz/service_conbee.yml ]]; then
                                        echo "Error: ./.templates/deconz/service_conbee.yml does not exist."
                                else
                                        cat ./.templates/deconz/service_conbee.yml >> $DOCKER_COMPOSE_PATH
                                        echo "...copied ConBee config from template"
                                fi
                                ;;
                        "RaspBee")
                                if [[ ! -f ./.templates/deconz/service_raspbee.yml ]]; then
                                        echo "Error: ./.templates/deconz/service_raspbee.yml does not exist."
                                else
                                        cat ./.templates/deconz/service_raspbee.yml >> $DOCKER_COMPOSE_PATH
                                        echo "...copied RaspBee config from template"
                                fi
                                ;;
                        esac