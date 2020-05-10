#!/bin/bash

#deCONZ device configuration

device_selection=$(whiptail --radiolist --title "deCONZ device configuration" --notags \
        "Use the [SPACEBAR] to select your Zigbee device from the list below and make sure it is plugged in (if not, press [ESC])." 20 78 12 \
        "ConBeeII" "ConBee II " "ON" \
        "ConBee" "ConBee " "OFF" \
        "RaspBee" "RaspBee " "OFF" \
        3>&1 1>&2 2>&3)

        case $device_selection in

                        "ConBeeII")
                                echo "...copied ConBee II config from template"
                                echo "" >>docker-compose.yml
                                cat .templates/deconz/service_conbee_II.yml >>docker-compose.yml
                                ;;
                        "ConBee")
                                echo "...copied ConBee config from template"
                                echo "" >>docker-compose.yml
                                cat .templates/deconz/service_conbee.yml >>docker-compose.yml
                                ;;
                        "RaspBee")
                                echo "...copied RaspBee config from template"
                                echo "" >>docker-compose.yml
                                cat .templates/deconz/service_raspbee.yml >>docker-compose.yml
                                ;;
                        esac
