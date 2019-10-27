#!/bin/bash

#whiptail guide https://saveriomiroddi.github.io/Shell-scripting-adventures-part-3/

#future function add password in build phase
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

#function copies the template yml file to the local service folder and appends to the docker-compose.yml file
function yml_builder(){
    service="services/$1/service.yml"

    [ -d ./services/ ] || mkdir ./services/
    [ -d ./services/$1 ] || mkdir ./services/$1

    cp -n -RT .templates/$1/ ./services/$1/

    cat $service >> docker-compose.yml

    #rm $service

}

# build Dockerfile for nodered
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
    "node-red-contrib-influxdb" " " "ON" \
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

    nr_dfile=./services/nodered/Dockerfile

    touch $nr_dfile
    echo "FROM nodered/node-red:latest" > $nr_dfile
    #node red install script inspired from https://tech.scargill.net/the-script/
    echo "RUN for addonnodes in \\" >> $nr_dfile
    for checked in "${checked_nodes[@]}"; do
            echo "$checked \\"  >> $nr_dfile
    done
    echo "; do \\"  >> $nr_dfile
    echo "npm install \${addonnodes} ;\\"  >> $nr_dfile
    echo "done;" >> $nr_dfile

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
    #MAINMENU Install docker  ------------------------------------------------------------	
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
    #MAINMENU Build stack ------------------------------------------------------------	
    "build")
        container_selection=$(whiptail --title "Container Selection"  --notags --separate-output --checklist \
            "Use the [SPACEBAR] to select which containers you would like to install" 20 78 12 \
            "portainer" "Portainer" "ON" \
            "nodered" "Node-RED" "ON" \
            "influxdb" "InfluxDB" "ON" \
            "grafana" "Grafana" "ON" \
            "mosquitto" "Eclipse-Mosquitto" "ON" \
            "postgres" "Postgres" "OFF" \
            "adminer" "Adminer" "OFF" \
            3>&1 1>&2 2>&3)

        mapfile -t containers <<< "$container_selection"

        touch docker-compose.yml
        echo "version: '2'" > docker-compose.yml
        echo "services:" >> docker-compose.yml

        for container in "${containers[@]}"; do

            case $container in

            "portainer")
                echo "Adding portainer container"
                yml_builder "portainer"
                ;;
            "nodered")
                echo "Adding Node-RED container"
                yml_builder "nodered"
                build_nodered
                ;;
            "influxdb")
                echo "Adding influxdb container"
                yml_builder "influxdb"
                ;;
            "grafana")
                echo "Adding Grafana"
                yml_builder "grafana"
                ;;
            "mosquitto")
                echo "Adding Mosquitto"
                yml_builder "mosquitto"
                ;;
            "postgres")
                echo "Adding Postgres Container"
                yml_builder "postgres"
                ;;
            "adminer")
                echo "Adding Adminer container"
                yml_builder "adminer"
                ;;
            *)
                echo "Failed to add $container container"
                ;;
            esac
        done

        echo "docker-compose successfully created"
        echo "run \'docker-compose up -d\' to start the stack"

    ;;
    #MAINMENU Docker commands ------------------------------------------------------------	
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
        "start") ./scripts/start.sh ;;
        "stop") ./scripts/stop.sh ;;
        "stop_all") ./scripts/stop-all.sh ;;
        "restart") ./scripts/restart.sh ;;
        "pull") ./scripts/update.sh ;;
        "prune_volumes") ./scripts/prune-volumes.sh ;;
        "prune_images") ./scripts/prune-images.sh ;;
        esac
    ;;
    #MAINMENU Misc commands------------------------------------------------------------	
    "misc")
        misc_sellection=$(whiptail --title "Miscellaneous Commands" --menu --notags \
            "Some helpful commands" 20 78 12 -- \
            "swap" "Disable swap" \
            "dropbox-uploader" "Dropbox-Uploader" \
            "log2ram" "install log2ram to decrease load on sd card, moves /var/log into ram" \
            3>&1 1>&2 2>&3)

        case $misc_sellection in
	"swap")
		sudo dphys-swapfile swapoff
		sudo dphys-swapfile uninstall
		sudo update-rc.d dphys-swapfile remove
                echo "Swap file has been removed"
	;;
        "dropbox-uploader")
            if [ ! -d ~/Dropbox-Uploader ]
            then
                git clone https://github.com/andreafabrizi/Dropbox-Uploader.git ~/Dropbox-Uploader
                chmod +x ~/Dropbox-Uploader/dropbox_uploader.sh
                pushd ~/Dropbox-Uploader && sudo ./dropbox_uploader.sh
		popd
            else
                echo "Dropbox uploader already installed"
            fi
        ;;
        "log2ram")
            if [ ! -d ~/log2ram ]
            then
                git clone https://github.com/azlux/log2ram.git ~/log2ram
                chmod +x ~/log2ram/install.sh
                pushd ~/log2ram && sudo ./install.sh
		popd
            else
                echo "log2ram already installed"
            fi
        ;;
	esac
    ;;

    *) ;;
esac

