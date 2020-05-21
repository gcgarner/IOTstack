#!/bin/bash

#deCONZ device configuration

device_selection=$(whiptail --radiolist --title "Select deCONZ gateway" --notags \
        "Use the [SPACEBAR] to select your deCONZ gateway from the list below AND MAKE SURE IT IS PLUGGED IN (if not, press [ESC])." 20 78 12 \
        "ConBeeII" "ConBee II " "ON" \
        "ConBee" "ConBee " "OFF" \
        "RaspBee" "RaspBee " "OFF" \
        3>&1 1>&2 2>&3)

        case $device_selection in

                        "ConBeeII")
                                cat .templates/deconz/service_conbee_II.yml >>docker-compose.yml
                                echo "...copied ConBee II config from template"
                                ;;
                        "ConBee")
                                cat .templates/deconz/service_conbee.yml >>docker-compose.yml
                                echo "...copied ConBee config from template"
                                ;;
                        "RaspBee")
                                cat .templates/deconz/service_raspbee.yml >>docker-compose.yml
                                echo "...copied RaspBee config from template"
                                ;;
                        esac
