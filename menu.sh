#!/bin/bash

#whiptail guide https://saveriomiroddi.github.io/Shell-scripting-adventures-part-3/

password_dialog() {
    while [[ "$passphrase" != "$passphrase_repeat" || ${#passphrase} -lt 8 ]]; do

            passphrase=$(whiptail --passwordbox "${passphrase_invalid_message}Please enter the passphrase (8 chars min.):" 20 78 3>&1 1>&2 2>&3)
            passphrase_repeat=$(whiptail --passwordbox "Please repeat the passphrase:" 20 78 3>&1 1>&2 2>&3)

            passphrase_invalid_message="Passphrase too short, or not matching! "
    done
    echo  $passphrase
}
#test=$( password_dialog )

function command_exists() {
	command -v "$@" > /dev/null 2>&1
}

function yaml_builder(){
    service="$1/service.yml"
    volume="$1/volume.yml"

    [ -d $1 ] || mkdir $1

    cp -n -R .templates/$1/. ./$1/

    cat $service >> docker-compose.yml
    if [ -f $volume ]
    then
        cat $volume >> volumes.yml
        vol_flag=1
        #rm $volume
    fi

    #rm $service

}

build_nodered() {
node_selection=$(whiptail --title "Node-RED nodes" --checklist --separate-output\
    "Use the [SPACEBAR] to select the nodes you want preinstalled" 20 78 12 -- \
    "node-red-node-pi-gpiod" " " "ON" \
    "node-red-dashboard" " " "ON" \
    "node-red-node-openweathermap" " " "OFF" \
    "node-red-node-google" " " "OFF" \
    "node-red-node-emoncms" " " "OFF" \
    "node-red-node-geofence" " " "OFF" \
    "node-red-node-ping" " " "OFF" \
    "node-red-node-random" " " "OFF" \
    "node-red-node-smooth" " " "OFF" \
    "node-red-node-darksky" " " "OFF" \
    "node-red-contrib-config" " " "OFF" \
    "node-red-contrib-grove" " " "OFF" \
    "node-red-contrib-diode" " " "OFF" \
    "node-red-contrib-bigtimer" " " "OFF" \
    "node-red-contrib-esplogin" " " "OFF" \
    "node-red-contrib-timeout" " " "OFF" \
    "node-red-contrib-moment" " " "OFF" \
    "node-red-contrib-particle" " " "OFF" \
    "node-red-contrib-web-worldmap" " " "OFF" \
    "node-red-contrib-ramp-thermostat" " " "OFF" \
    "node-red-contrib-isonline" " " "OFF" \
    "node-red-contrib-npm" " " "OFF" \
    "node-red-contrib-file-function" " " "OFF" \
    "node-red-contrib-boolean-logic" " " "OFF" \
    "node-red-contrib-blynk-ws" " " "OFF" \
    "node-red-contrib-owntracks" " " "OFF" \
    "node-red-contrib-alexa-local" " " "OFF" \
    "node-red-contrib-heater-controller" " " "OFF" \
    3>&1 1>&2 2>&3)

    ##echo "$check_selection"
    mapfile -t checked_nodes <<< "$node_selection"

    touch ./nodered/Dockerfile
    echo "FROM nodered/node-red:latest" > ./nodered/Dockerfile
    #node red install script instpired from https://tech.scargill.net/the-script/
    echo "RUN for addonnodes in \\" >> ./nodered/Dockerfile
    for checked in "${checked_nodes[@]}"; do
            echo "$checked \\"  >> ./nodered/Dockerfile
    done
    echo "; do \\"  >> ./nodered/Dockerfile
    echo "npm install \${addonnodes} ;\\"  >> ./nodered/Dockerfile
    echo "done;" >> ./nodered/Dockerfile

}

#---------------------------------------------------------------------------------------------------
# Menu system starts here
#display main menu
mainmenu_selection=$(whiptail --title "Main Menu" --menu --notags \
    "" 20 78 12 -- \
    "install" "Install Docker" \
    "build" "Build Stack" \
    "commands" "Docker commands" \
    "misc" "Miscellaneous commands" \
    3>&1 1>&2 2>&3)

case $mainmenu_selection in
    "install")
        #sudo apt update && sudo apt upgrade -y ;;

        if  command_exists docker; then
            echo "docker already installed"
        else
        echo "Install Docker"
            curl -fsSL https://get.docker.com | sh
            sudo usermod -aG docker $USER
        fi

        if command_exists docker-compose; then
            echo "docker-compose already installed"
        else
            echo "Install docker-compose"
            sudo apt install -y docker-compose
        fi

        if ( whiptail --title "Restart Required" --yesno "It is recommended that you restart you device now. Select yes to do so now" 20 78); then
            sudo reboot
        fi
        ;;
    "build")
        container_selection=$(whiptail --title "Container Selection"  --notags --separate-output --checklist \
            "Use the [SPACEBAR] to select which containers you would like to install" 20 78 12 \
            "portainer" "Portainer" "ON" \
            "nodered" "Node-RED" "ON" \
            "influxdb" "InfluxDB" "ON" \
            "grafana" "Grafana" "ON" \
            "mqtt" "Eclipse-Mosquitto" "ON" \
            "pihole" "Pi-hole" "OFF" \
            "postgres" "Postgres" "OFF" \
            "adminer" "Adminer" "OFF" \
            3>&1 1>&2 2>&3)

        mapfile -t containers <<< "$container_selection"

        touch docker-compose.yml
        echo "version: '2'" > docker-compose.yml
        echo "services:" >> docker-compose.yml

        touch volumes.yml
        echo "volumes:" > volumes.yml
        vol_flag=0

        for container in "${containers[@]}"; do

            case $container in

            "portainer")
                echo "Adding portainer container"
                yaml_builder "portainer"
                ;;
            "nodered")
                echo "Adding Node-RED container"
                yaml_builder "nodered"
                build_nodered
                ;;
            "influxdb")
                echo "Adding influxdb container"
                yaml_builder "influxdb"
                ;;
            "grafana")
                echo "Adding Grafana"
                yaml_builder "grafana"
                ;;
            "mqtt")
                echo "Adding Mosquitto"
                yaml_builder "mosquitto"
                ;;
            "pihole")
                echo "Adding Pi-Hole container"
                yaml_builder "pihole"
                ;;
            "postgres")
                echo "Adding Postgres Container"
                yaml_builder "postgres"
                ;;
            "adminer")
                echo "Adding Adminer container"
                yaml_builder "adminer"
                ;;
            *)
                echo "Failed to add $container container"
                ;;
            esac
        done

        if [ $vol_flag -gt 0 ]
        then
            cat volumes.yml >> docker-compose.yml
        fi
        rm volumes.yml

        echo "docker-compose successfully created"
        echo "run \'docker-compose up -d\' to start the stack"

    ;;
    "commands")

        docker_selection=$(whiptail --title "Docker commands"  --menu --notags \
            "Shortcut to common docker commands" 20 78 12 -- \
            "start" "Start stack" \
            "restart" "Restart stack" \
            "stop" "Stop stack" \
            "stop_all" "Stop any running container regardless of stack" \
            "pull" "Update all containers" \
            "prune_volumes" "Delete all stopped containers and docker volumes" \
            "prune_images" "Delete all images not associated with container" \
             3>&1 1>&2 2>&3)

        case $docker_selection in
        "start") ./start.sh ;;
        "stop") ./stop.sh ;;
        "stop_all") ./stop-all.sh ;;
        "restart") ./restart.sh ;;
        "pull") ./update.sh ;;
        "prune_volumes") ./prune-volumes.sh ;;
        "prune_images") ./prune-images.sh ;;
        esac
    ;;

    "misc")
        misc_sellection=$(whiptail --title "Miscellaneous Commands" --menu --notags \
            "Some helpful commands" 20 78 12 -- \
            "swap" "Disable swap" \
            3>&1 1>&2 2>&3)

        case $misc_sellection in
	"swap")
		sudo dphys-swapfile swapoff
		sudo dphys-swapfile uninstall
		sudo update-rc.d dphys-swapfile remove
                echo "Swap file has been removed"
	;;
	esac
    ;;

    *) ;;
esac

