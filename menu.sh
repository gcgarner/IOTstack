#!/bin/bash

#get path of menu correct
pushd ~/IOTstack

CURRENT_BRANCH=${1:-$(git name-rev --name-only HEAD)}

# Consts/vars
TMP_DOCKER_COMPOSE_YML=./.tmp/docker-compose.tmp.yml
DOCKER_COMPOSE_YML=./docker-compose.yml
DOCKER_COMPOSE_OVERRIDE_YML=./compose-override.yml

# Minimum Software Versions
COMPOSE_VERSION="3.6"
REQ_DOCKER_VERSION=18.2.0
REQ_PYTHON_VERSION=3.6.9
REQ_PYYAML_VERSION=5.3.1

declare -A cont_array=(
	[portainer]="Portainer"
	[nodered]="Node-RED"
	[influxdb]="InfluxDB"
	[telegraf]="Telegraf (Requires InfluxDB and Mosquitto)"
	[transmission]="transmission"
	[grafana]="Grafana"
	[mosquitto]="Eclipse-Mosquitto"
	[postgres]="Postgres"
	[timescaledb]="Timescaledb"
	[mariadb]="MariaDB (MySQL fork)"
	[adminer]="Adminer"
	[openhab]="openHAB"
	[zigbee2mqtt]="zigbee2mqtt"
	[deconz]="deCONZ"
	[pihole]="Pi-Hole"
	[plex]="Plex media server"
	[tasmoadmin]="TasmoAdmin"
	[rtl_433]="RTL_433 to mqtt"
	[espruinohub]="EspruinoHub"
	[motioneye]="motionEye"
	[webthings_gateway]="Mozilla webthings-gateway"
	[blynk_server]="blynk-server"
	[nextcloud]="Next-Cloud"
	[nginx]="NGINX by linuxserver"
	[diyhue]="diyHue"
	[homebridge]="Homebridge"
	[python]="Python 3"
	[gitea]="Gitea"
	[dozzle]="Dozzle"
)

declare -a armhf_keys=(
	"portainer"
	"nodered"
	"influxdb"
	"grafana"
	"mosquitto"
	"telegraf"
	"mariadb"
	"postgres"
	"timescaledb"
	"transmission"
	"adminer"
	"openhab"
	"zigbee2mqtt"
  "deconz"
	"pihole"
	"plex"
	"tasmoadmin"
	"rtl_433"
	"espruinohub"
	"motioneye"
	"webthings_gateway"
	"blynk_server"
	"nextcloud"
	"diyhue"
	"homebridge"
	"python"
	"gitea"
	"dozzle"
	# add yours here
)
sys_arch=$(uname -m)

#timezones
timezones() {

	env_file=$1
	TZ=$(cat /etc/timezone)

	#test for TZ=
	[ $(grep -c "TZ=" $env_file) -ne 0 ] && sed -i "/TZ=/c\TZ=$TZ" $env_file

}

# this function creates the volumes, services and backup directories. It then assisgns the current user to the ACL to give full read write access
docker_setfacl() {
	[ -d ./services ] || mkdir ./services
	[ -d ./volumes ] || mkdir ./volumes
	[ -d ./backups ] || mkdir ./backups
	[ -d ./tmp ] || mkdir ./tmp

	#give current user rwx on the volumes and backups
	[ $(getfacl ./volumes | grep -c "default:user:$USER") -eq 0 ] && sudo setfacl -Rdm u:$USER:rwx ./volumes
	[ $(getfacl ./backups | grep -c "default:user:$USER") -eq 0 ] && sudo setfacl -Rdm u:$USER:rwx ./backups
}

#future function add password in build phase
password_dialog() {
	while [[ "$passphrase" != "$passphrase_repeat" || ${#passphrase} -lt 8 ]]; do

		passphrase=$(whiptail --passwordbox "${passphrase_invalid_message}Please enter the passphrase (8 chars min.):" 20 78 3>&1 1>&2 2>&3)
		passphrase_repeat=$(whiptail --passwordbox "Please repeat the passphrase:" 20 78 3>&1 1>&2 2>&3)
		passphrase_invalid_message="Passphrase too short, or not matching! "
	done
	echo $passphrase
}
#test=$( password_dialog )

function command_exists() {
	command -v "$@" > /dev/null 2>&1
}

function minimum_version_check() {
	# minimum_version_check required_version current_major current_minor current_build
	# minimum_version_check "1.2.3" 1 2 3
	REQ_MIN_VERSION_MAJOR=$(echo "$1"| cut -d' ' -f 2 | cut -d'.' -f 1)
	REQ_MIN_VERSION_MINOR=$(echo "$1"| cut -d' ' -f 2 | cut -d'.' -f 2)
	REQ_MIN_VERSION_BUILD=$(echo "$1"| cut -d' ' -f 2 | cut -d'.' -f 3)

	CURR_VERSION_MAJOR=$2
	CURR_VERSION_MINOR=$3
	CURR_VERSION_BUILD=$4
	
	VERSION_GOOD="Unknown"

	if [ -z "$CURR_VERSION_MAJOR" ]; then
		echo "$VERSION_GOOD"
		return 1
	fi

	if [ -z "$CURR_VERSION_MINOR" ]; then
		echo "$VERSION_GOOD"
		return 1
	fi

	if [ -z "$CURR_VERSION_BUILD" ]; then
		echo "$VERSION_GOOD"
		return 1
	fi

	if [ "${CURR_VERSION_MAJOR}" -ge $REQ_MIN_VERSION_MAJOR ]; then
		VERSION_GOOD="true"
		echo "$VERSION_GOOD"
		return 0
	else
		VERSION_GOOD="false"
	fi

	if [ "${CURR_VERSION_MAJOR}" -ge $REQ_MIN_VERSION_MAJOR ] && \
		[ "${CURR_VERSION_MINOR}" -ge $REQ_MIN_VERSION_MINOR ]; then
		VERSION_GOOD="true"
		echo "$VERSION_GOOD"
		return 0
	else
		VERSION_GOOD="false"
	fi

	if [ "${CURR_VERSION_MAJOR}" -ge $REQ_MIN_VERSION_MAJOR ] && \
		[ "${CURR_VERSION_MINOR}" -ge $REQ_MIN_VERSION_MINOR ] && \
		[ "${CURR_VERSION_BUILD}" -ge $REQ_MIN_VERSION_BUILD ]; then
		VERSION_GOOD="true"
		echo "$VERSION_GOOD"
		return 0
	else
		VERSION_GOOD="false"
	fi

	echo "$VERSION_GOOD"
}

function install_python3_and_deps() {
	CURR_PYTHON_VER="${1:-Unknown}"
	CURR_PYYAML_VER="${2:-Unknown}"
	if (whiptail --title "Python 3 and Dependencies" --yesno "Python 3.6.9 or later (Current = $CURR_PYTHON_VER), PyYaml 5.3.1 or later (Current = $CURR_PYYAML_VER) and pip3 is required for compose-overrides.yml file to merge into the docker-compose.yml file. Install these now?" 20 78); then
		sudo apt install -y python3-pip python3-dev
		if [ $? -eq 0 ]; then
			PYTHON_VERSION_GOOD="true"
		else
			echo "Failed to install Python"
			exit 1
		fi
		pip3 install -U pyyaml==5.3.1
				if [ $? -eq 0 ]; then
			PYYAML_VERSION_GOOD="true"
		else
			echo "Failed to install Python"
			exit 1
		fi
	fi
}

function do_python3_pip() {
	PYTHON_VERSION_GOOD="false"
	PYYAML_VERSION_GOOD="false"

	if command_exists python3 && command_exists pip3; then
		PYTHON_VERSION=$(python3 --version)
		echo "Python Version: ${PYTHON_VERSION:-Unknown}"
		PYTHON_VERSION_MAJOR=$(echo "$PYTHON_VERSION"| cut -d' ' -f 2 | cut -d'.' -f 1)
		PYTHON_VERSION_MINOR=$(echo "$PYTHON_VERSION"| cut -d'.' -f 2)
		PYTHON_VERSION_BUILD=$(echo "$PYTHON_VERSION"| cut -d'.' -f 3)

		PYYAML_VERSION=$(python3 ./scripts/yaml_merge.py --pyyaml-version)
		PYYAML_VERSION="${PYYAML_VERSION:-Unknown}"
		PYYAML_VERSION_MAJOR=$(echo "$PYYAML_VERSION"| cut -d' ' -f 2 | cut -d'.' -f 1)
		PYYAML_VERSION_MINOR=$(echo "$PYYAML_VERSION"| cut -d'.' -f 2)
		PYYAML_VERSION_BUILD=$(echo "$PYYAML_VERSION"| cut -d'.' -f 3)

		if [ "$(minimum_version_check $REQ_PYTHON_VERSION $PYTHON_VERSION_MAJOR $PYTHON_VERSION_MINOR $PYTHON_VERSION_BUILD)" == "true" ]; then
			PYTHON_VERSION_GOOD="true"
		else
			echo "Python is outdated."
			install_python3_and_deps "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR.$PYTHON_VERSION_BUILD" "$PYYAML_VERSION_MAJOR.$PYYAML_VERSION_MINOR.$PYYAML_VERSION_BUILD"
			return 1
		fi
		echo "PyYaml Version: $PYYAML_VERSION"
		if [ "$(minimum_version_check $REQ_PYYAML_VERSION $PYYAML_VERSION_MAJOR $PYYAML_VERSION_MINOR $PYYAML_VERSION_BUILD)" == "true" ]; then
			PYYAML_VERSION_GOOD="true"
		else
			echo "PyYaml is outdated."
			if [ "$PYYAML_VERSION" != "Unknown" ]; then
				install_python3_and_deps "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR.$PYTHON_VERSION_BUILD" "$PYYAML_VERSION_MAJOR.$PYYAML_VERSION_MINOR.$PYYAML_VERSION_BUILD"
			else
				install_python3_and_deps "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR.$PYTHON_VERSION_BUILD"
			fi
			return 1
		fi
	else
		install_python3_and_deps
		return 1
	fi
}

#function copies the template yml file to the local service folder and appends to the docker-compose.yml file
function yml_builder() {

	service="services/$1/service.yml"

	[ -d ./services/ ] || mkdir ./services/

	if [ -d ./services/$1 ]; then
		#directory already exists prompt user to overwrite
		sevice_overwrite=$(whiptail --radiolist --title "Overwrite Option" --notags \
			"$1 service directory has been detected, use [SPACEBAR] to select you overwrite option" 20 78 12 \
			"none" "Do not overwrite" "ON" \
			"env" "Preserve Environment and Config files" "OFF" \
			"full" "Pull full service from template" "OFF" \
			3>&1 1>&2 2>&3)

		case $sevice_overwrite in

		"full")
			echo "...pulled full $1 from template"
			rsync -a -q .templates/$1/ services/$1/ --exclude 'build.sh'
			;;
		"env")
			echo "...pulled $1 excluding env file"
			rsync -a -q .templates/$1/ services/$1/ --exclude 'build.sh' --exclude '$1.env' --exclude '*.conf'
			;;
		"none")
			echo "...$1 service not overwritten"
			;;

		esac

	else
		mkdir ./services/$1
		echo "...pulled full $1 from template"
		rsync -a -q .templates/$1/ services/$1/ --exclude 'build.sh'
	fi


	#if an env file exists check for timezone
	[ -f "./services/$1/$1.env" ] && timezones ./services/$1/$1.env

	# if a volumes.yml exists, append to overall volumes.yml file
	[ -f "./services/$1/volumes.yml" ] && cat "./services/$1/volumes.yml" >> docker-volumes.yml

	#add new line then append service
	echo "" >> $TMP_DOCKER_COMPOSE_YML
	cat $service >> $TMP_DOCKER_COMPOSE_YML

	#test for post build
	if [ -f ./.templates/$1/build.sh ]; then
		chmod +x ./.templates/$1/build.sh
		bash ./.templates/$1/build.sh
	fi

	#test for directoryfix.sh
	if [ -f ./.templates/$1/directoryfix.sh ]; then
		chmod +x ./.templates/$1/directoryfix.sh
		echo "...Running directoryfix.sh on $1"
		bash ./.templates/$1/directoryfix.sh
	fi

	#make sure terminal.sh is executable
	[ -f ./services/$1/terminal.sh ] && chmod +x ./services/$1/terminal.sh

}

#---------------------------------------------------------------------------------------------------
# Project updates
echo "checking for project update"
git fetch origin master

if [ $(git status | grep -c "Your branch is up to date") -eq 1 ]; then
	#delete .outofdate if it exisist
	[ -f .outofdate ] && rm .outofdate
	echo "Project is up to date"

else
	echo "An update is available for the project"
	if [ ! -f .outofdate ]; then
		whiptail --title "Project update" --msgbox "An update is available for the project\nYou will not be reminded again until you next update" 8 78
		touch .outofdate
	fi
fi

#---------------------------------------------------------------------------------------------------
# Docker updates
if command_exists docker; then
	echo "checking docker version"
	DOCKER_VERSION=$(docker version -f "{{.Server.Version}}")
	DOCKER_VERSION_MAJOR=$(echo "$DOCKER_VERSION"| cut -d'.' -f 1)
	DOCKER_VERSION_MINOR=$(echo "$DOCKER_VERSION"| cut -d'.' -f 2)
	DOCKER_VERSION_BUILD=$(echo "$DOCKER_VERSION"| cut -d'.' -f 3)

	if [ "$(minimum_version_check $REQ_DOCKER_VERSION $DOCKER_VERSION_MAJOR $DOCKER_VERSION_MINOR $DOCKER_VERSION_BUILD )" == "true" ]; then
		echo "Docker version >= $REQ_DOCKER_VERSION. You are good to go."
	else
		if (whiptail --title "Docker and Docker-Compose Version Issue" --yesno "Docker version is currently $DOCKER_VERSION which is less than $REQ_DOCKER_VERSION consider upgrading or you may experience issues. You can manually upgrade by typing 'sudo apt upgrade docker docker-compose'. Attempt to upgrade now?" 20 78); then
			sudo apt upgrade docker docker-compose
		fi
	fi
else
	echo "docker not installed"
fi

#---------------------------------------------------------------------------------------------------
# Menu system starts here
# Display main menu
mainmenu_selection=$(whiptail --title "Main Menu" --menu --notags \
	"" 20 78 12 -- \
	"install" "Install Docker" \
	"build" "Build Stack" \
	"hassio" "Install Hass.io (Requires Docker)" \
	"native" "Native Installs" \
	"commands" "Docker commands" \
	"backup" "Backup options" \
	"misc" "Miscellaneous commands" \
	"update" "Update IOTstack" \
	3>&1 1>&2 2>&3)

case $mainmenu_selection in
#MAINMENU Install docker  ------------------------------------------------------------
"install")
	#sudo apt update && sudo apt upgrade -y ;;

	if command_exists docker; then
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

	if (whiptail --title "Restart Required" --yesno "It is recommended that you restart your device now. Select yes to do so now" 20 78); then
		sudo reboot
	fi
	;;
	#MAINMENU Build stack ------------------------------------------------------------
"build")

	title=$'Container Selection'
	message=$'Use the [SPACEBAR] to select which containers you would like to install'
	entry_options=()

	#check architecture and display appropriate menu
	if [ $(echo "$sys_arch" | grep -c "arm") ]; then
		keylist=("${armhf_keys[@]}")
	else
		echo "your architecture is not supported yet"
		exit
	fi

	#loop through the array of descriptions
	for index in "${keylist[@]}"; do
		entry_options+=("$index")
		entry_options+=("${cont_array[$index]}")

		#check selection
		if [ -f ./services/selection.txt ]; then
			[ $(grep "$index" ./services/selection.txt) ] && entry_options+=("ON") || entry_options+=("OFF")
		else
			entry_options+=("OFF")
		fi
	done

	container_selection=$(whiptail --title "$title" --notags --separate-output --checklist \
		"$message" 20 78 12 -- "${entry_options[@]}" 3>&1 1>&2 2>&3)

	mapfile -t containers <<<"$container_selection"

	#if no container is selected then dont overwrite the docker-compose.yml file
	if [ -n "$container_selection" ]; then
		touch $TMP_DOCKER_COMPOSE_YML

		echo "version: '$COMPOSE_VERSION'" > $TMP_DOCKER_COMPOSE_YML
		echo "services:" >> $TMP_DOCKER_COMPOSE_YML

		#set the ACL for the stack
		#docker_setfacl

		# store last sellection
		[ -f ./services/selection.txt ] && rm ./services/selection.txt
		#first run service directory wont exist
		[ -d ./services ] || mkdir services
		touch ./services/selection.txt
		#Run yml_builder of all selected containers
		for container in "${containers[@]}"; do
			echo "Adding $container container"
			yml_builder "$container"
			echo "$container" >>./services/selection.txt
		done

		if [ -f "$DOCKER_COMPOSE_OVERRIDE_YML" ]; then
			do_python3_pip
			
			if [ "$PYTHON_VERSION_GOOD" == "true" ] && [ "$PYYAML_VERSION_GOOD" == "true" ]; then
				echo "merging docker overrides with docker-compose.yml"
				python3 ./scripts/yaml_merge.py $TMP_DOCKER_COMPOSE_YML  $DOCKER_COMPOSE_OVERRIDE_YML $DOCKER_COMPOSE_YML
			else
				echo "incorrect python or dependency versions, aborting override and using docker-compose.yml"
				cp $TMP_DOCKER_COMPOSE_YML $DOCKER_COMPOSE_YML
			fi
		else
			echo "no override found, using docker-compose.yml"
			cp $TMP_DOCKER_COMPOSE_YML $DOCKER_COMPOSE_YML
		fi

		echo "docker-compose successfully created"
		echo "run 'docker-compose up -d' to start the stack"
	else

		echo "Build cancelled"

	fi
	;;
	#MAINMENU Docker commands -----------------------------------------------------------
"commands")

	docker_selection=$(
		whiptail --title "Docker commands" --menu --notags \
			"Shortcut to common docker commands" 20 78 12 -- \
			"aliases" "Add iotstack_up and iotstack_down aliases" \
			"start" "Start stack" \
			"restart" "Restart stack" \
			"stop" "Stop stack" \
			"stop_all" "Stop any running container regardless of stack" \
			"pull" "Update all containers" \
			"prune_volumes" "Delete all stopped containers and docker volumes" \
			"prune_images" "Delete all images not associated with container" \
			3>&1 1>&2 2>&3
	)

	case $docker_selection in
	"start") ./scripts/start.sh ;;
	"stop") ./scripts/stop.sh ;;
	"stop_all") ./scripts/stop-all.sh ;;
	"restart") ./scripts/restart.sh ;;
	"pull") ./scripts/update.sh ;;
	"prune_volumes") ./scripts/prune-volumes.sh ;;
	"prune_images") ./scripts/prune-images.sh ;;
	"aliases")
		touch ~/.bash_aliases
		if [ $(grep -c 'IOTstack' ~/.bash_aliases) -eq 0 ]; then
			echo ". ~/IOTstack/.bash_aliases" >>~/.bash_aliases
			echo "added aliases"
		else
			echo "aliases already added"
		fi
		source ~/.bashrc
		echo "aliases will be available after a reboot"
		;;
	esac
	;;
	#Backup menu ---------------------------------------------------------------------
"backup")
	backup_sellection=$(whiptail --title "Backup Options" --menu --notags \
		"Select backup option" 20 78 12 -- \
		"dropbox-uploader" "Dropbox-Uploader" \
		"rclone" "google drive via rclone" \
		3>&1 1>&2 2>&3)

	case $backup_sellection in

	"dropbox-uploader")
		if [ ! -d ~/Dropbox-Uploader ]; then
			git clone https://github.com/andreafabrizi/Dropbox-Uploader.git ~/Dropbox-Uploader
			chmod +x ~/Dropbox-Uploader/dropbox_uploader.sh
			pushd ~/Dropbox-Uploader && ./dropbox_uploader.sh
			popd
		else
			echo "Dropbox uploader already installed"
		fi

		#add enable file for Dropbox-Uploader
		[ -d ~/IOTstack/backups ] || sudo mkdir -p ~/IOTstack/backups/
		sudo touch ~/IOTstack/backups/dropbox
		;;
	"rclone")
		sudo apt install -y rclone
		echo "Please run 'rclone config' to configure the rclone google drive backup"

		#add enable file for rclone
		[ -d ~/IOTstack/backups ] || sudo mkdir -p ~/IOTstack/backups/
		sudo touch ~/IOTstack/backups/rclone
		;;
	esac
	;;
	#MAINMENU Misc commands------------------------------------------------------------
"misc")
	misc_sellection=$(
		whiptail --title "Miscellaneous Commands" --menu --notags \
			"Some helpful commands" 20 78 12 -- \
			"swap" "Disable swap by uninstalling swapfile" \
			"swappiness" "Disable swap by setting swappiness to 0" \
			"log2ram" "install log2ram to decrease load on sd card, moves /var/log into ram" \
			3>&1 1>&2 2>&3
	)

	case $misc_sellection in
	"swap")
		sudo dphys-swapfile swapoff
		sudo dphys-swapfile uninstall
		sudo update-rc.d dphys-swapfile remove
		sudo systemctl disable dphys-swapfile
		#sudo apt-get remove dphys-swapfile
		echo "Swap file has been removed"
		;;
	"swappiness")
		if [ $(grep -c swappiness /etc/sysctl.conf) -eq 0 ]; then
			echo "vm.swappiness=0" | sudo tee -a /etc/sysctl.conf
			echo "updated /etc/sysctl.conf with vm.swappiness=0"
		else
			sudo sed -i "/vm.swappiness/c\vm.swappiness=0" /etc/sysctl.conf
			echo "vm.swappiness found in /etc/sysctl.conf update to 0"
		fi

		sudo sysctl vm.swappiness=0
		echo "set swappiness to 0 for immediate effect"
		;;
	"log2ram")
		if [ ! -d ~/log2ram ]; then
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

"hassio")
	echo "install requirements for hass.io"
	sudo apt install -y bash jq curl avahi-daemon dbus
	hassio_machine=$(whiptail --title "Machine type" --menu \
		"Please select you device type" 20 78 12 -- \
		"raspberrypi4" " " \
		"raspberrypi3" " " \
		"raspberrypi2" " " \
		"raspberrypi4-64" " " \
		"raspberrypi3-64" " " \
		"qemux86" " " \
		"qemux86-64" " " \
		"qemuarm" " " \
		"qemuarm-64" " " \
		"orangepi-prime" " " \
		"odroid-xu" " " \
		"odroid-c2" " " \
		"intel-nuc" " " \
		"tinker" " " \
		3>&1 1>&2 2>&3)
	if [ -n "$hassio_machine" ]; then
		curl -sL https://raw.githubusercontent.com/home-assistant/supervised-installer/master/installer.sh | sudo bash -s -- -m $hassio_machine
	else
		echo "no selection"
		exit
	fi
	;;
"update")
	echo "Pulling latest project file from Github.com ---------------------------------------------"
	git pull origin $CURRENT_BRANCH
	echo "git status ------------------------------------------------------------------------------"
	git status
	;;
"native")

	native_selections=$(whiptail --title "Native installs" --menu --notags \
		"Install local applications" 20 78 12 -- \
		"rtl_433" "RTL_433" \
		"rpieasy" "RPIEasy" \
		3>&1 1>&2 2>&3)

	case $native_selections in
	"rtl_433")
		bash ./.native/rtl_433.sh
		;;
	"rpieasy")
		bash ./.native/rpieasy.sh
		;;
	esac
	;;
*) ;;

esac

popd > /dev/null 2>&1
