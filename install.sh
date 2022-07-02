#!/bin/bash

# Minimum Software Versions
REQ_DOCKER_VERSION=18.2.0
REQ_PYTHON_VERSION=3.6.9

PYTHON_CMD=python3

sys_arch=$(uname -m)

while test $# -gt 0
do
    case "$1" in
        --no-ask) NOASKCONFIRM="true"
            ;;
        --*) echo "bad option $1"
            ;;
    esac
    shift
done

echo "IOTstack Installation"
if [ "$EUID" -eq "0" ]; then
  echo "Please do not run as root"
  exit
fi

function command_exists() {
	command -v "$@" > /dev/null 2>&1
}

function minimum_version_check() {
	# Usage: minimum_version_check required_version current_major current_minor current_build
	# Example: minimum_version_check "1.2.3" 1 2 3
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

function user_in_group()
{
	if grep -q $1 /etc/group ; then
		if id -nGz "$USER" | grep -qzxF "$1";	then
				echo "true"
		else
				echo "false"
		fi
	else
		echo "notgroup"
	fi
}

function install_python3_and_deps() {
	CURR_PYTHON_VER="${1:-Unknown}"
	CURR_VIRTUALENV="${2:-Unknown}"
  if ([ "$NOASKCONFIRM" == "true" ] ||
      whiptail --title "Python 3 and virtualenv" --yesno "Python 3.6.9 or later (Current = $CURR_PYTHON_VER) and virtualenv (Installed = $CURR_VIRTUALENV) are required for the main menu. Install these now?" 20 78); then
    echo "Installing Python3 and virtualenv"
    sudo apt install -y python3-dev python3-virtualenv
    if [ $? -eq 0 ]; then
      PYTHON_VERSION_GOOD="true"
    else
      echo "Failed to install Python and virtualenv" >&2
      exit 1
    fi
  fi
}

function install_docker() {
  if command_exists docker; then
    echo "Docker already installed" >&2
  else
    echo "Install Docker" >&2
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
  fi

  if command_exists docker-compose; then
    echo "docker-compose already installed" >&2
  else
    echo "Install docker-compose" >&2
    sudo apt install -y docker-compose
  fi

	echo "" >&2
	echo "You should now restart your system" >&2
}

function update_docker() {
	sudo apt upgrade docker docker-compose
}

function do_python3_checks() {
	VIRTUALENV_GOOD="false"
	if command_exists virtualenv; then
		VIRTUALENV_GOOD="true"
		echo "Python virtualenv found." >&2
	fi
	PYTHON_VERSION_GOOD="false"
	if command_exists $PYTHON_CMD; then
		PYTHON_VERSION=$($PYTHON_CMD --version 2>/dev/null)
		PYTHON_VERSION_MAJOR=$(echo "$PYTHON_VERSION"| cut -d' ' -f 2 | cut -d' ' -f 2 | cut -d'.' -f 1)
		PYTHON_VERSION_MINOR=$(echo "$PYTHON_VERSION"| cut -d' ' -f 2 | cut -d'.' -f 2)
		PYTHON_VERSION_BUILD=$(echo "$PYTHON_VERSION"| cut -d' ' -f 2 | cut -d'.' -f 3)

		printf "Python Version: '${PYTHON_VERSION:-Unknown}'. "
		if [ "$(minimum_version_check $REQ_PYTHON_VERSION $PYTHON_VERSION_MAJOR $PYTHON_VERSION_MINOR $PYTHON_VERSION_BUILD)" == "true" -a "$VIRTUALENV_GOOD" == "true" ]; then
			PYTHON_VERSION_GOOD="true"
			echo "Python and virtualenv is up to date." >&2
		else
			echo "Python is outdated or virtualenv is missing" >&2
			install_python3_and_deps "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR.$PYTHON_VERSION_BUILD" "$VIRTUALENV_GOOD"
			return 1
		fi
	else
		install_python3_and_deps
		return 1
	fi
}

function do_env_setup() {
	echo "Setting up environment:"
	if [[ ! "$(user_in_group bluetooth)" == "notgroup" ]] && [[ ! "$(user_in_group bluetooth)" == "true" ]]; then
    echo "User is NOT in 'bluetooth' group. Adding:" >&2
    echo "sudo usermod -G bluetooth -a $USER" >&2
		sudo usermod -G "bluetooth" -a $USER
	fi

	if [ ! "$(user_in_group docker)" == "true" ]; then
    echo "User is NOT in 'docker' group. Adding:" >&2
    echo "sudo usermod -G docker -a $USER" >&2
		sudo usermod -G "docker" -a $USER
	fi
}

function do_docker_checks() {
	if command_exists docker; then
		DOCKER_VERSION_GOOD="false"
		DOCKER_VERSION=$(docker version -f "{{.Server.Version}}")
		if [ ! -z "$DOCKER_VERSION" ]; then
			echo "Error getting docker version. Error when running docker command. Check that docker is installed correctly."
		fi
		DOCKER_VERSION_MAJOR=$(echo "$DOCKER_VERSION"| cut -d'.' -f 1)
		DOCKER_VERSION_MINOR=$(echo "$DOCKER_VERSION"| cut -d'.' -f 2)
		DOCKER_VERSION_BUILD=$(echo "$DOCKER_VERSION"| cut -d'.' -f 3)
		DOCKER_VERSION_BUILD=$(echo "$DOCKER_VERSION_BUILD"| cut -f1 -d"-")
		DOCKER_VERSION_BUILD=$(echo "$DOCKER_VERSION_BUILD"| cut -f1 -d"+")

		if [ "$(minimum_version_check $REQ_DOCKER_VERSION $DOCKER_VERSION_MAJOR $DOCKER_VERSION_MINOR $DOCKER_VERSION_BUILD )" == "true" ]; then
			[ -f .docker_outofdate ] && rm .docker_outofdate
			DOCKER_VERSION_GOOD="true"
			echo "Docker version $DOCKER_VERSION >= $REQ_DOCKER_VERSION. Docker is good to go." >&2
		else
      if [ "$NOASKCONFIRM" == "true" ]; then
        update_docker
      else
        if [ ! -f .docker_outofdate ]; then
          if (whiptail --title "Docker and Docker-Compose Version Issue" --yesno "Docker version is currently $DOCKER_VERSION which is less than $REQ_DOCKER_VERSION consider upgrading or you may experience issues. You will not be prompted again. You can manually upgrade by typing:\n  sudo apt upgrade docker docker-compose\n\nAttempt to upgrade now?" 20 78); then
            update_docker
          else
            touch .docker_outofdate
          fi
        fi
      fi
		fi
	else
		[ -f .docker_outofdate ] && rm .docker_outofdate
		echo "Docker not installed" >&2
    if [ "$NOASKCONFIRM" == "true" ]; then
      do_env_setup
      install_docker
    else
      if [ ! -f .docker_notinstalled ]; then
        if (whiptail --title "Docker and Docker-Compose" --yesno "Docker is not currently installed, and is required to run IOTstack. Would you like to install docker and docker-compose now?\nYou will not be prompted again." 20 78); then
            [ -f .docker_notinstalled ] && rm .docker_notinstalled
            do_env_setup
            install_docker
          else
            touch .docker_notinstalled
        fi
      fi
    fi
	fi
}

function do_env_checks() {
	GROUPSGOOD=0

	if [[ ! "$(user_in_group bluetooth)" == "notgroup" ]] && [[ ! "$(user_in_group bluetooth)" == "true" ]]; then
	  GROUPSGOOD=1
    echo "User is NOT in 'bluetooth' group" >&2
	fi

	if [[ ! "$(user_in_group docker)" == "true" ]]; then
	  GROUPSGOOD=1
    echo "User is NOT in 'docker' group" >&2
	fi

	if [ "$GROUPSGOOD" == 1 ]; then
		echo "!! You might experience issues with docker or bluetooth. To fix run: ./menu.sh --run-env-setup"
	fi
}

function do_kernel_checks() {
    if ! grep -q "cgroup_memory=1 cgroup_enable=memory" /boot/cmdline.txt; then
        echo "Kernel cgroups not enabled. Adding kernel parameters." >&2
        echo "You will need to restart your system before the changes take effect."
        echo $(cat /boot/cmdline.txt) cgroup_memory=1 cgroup_enable=memory | sudo tee /boot/cmdline.txt
    fi
}

touch .new_install
echo "Enter in the sudo password when prompted, to install dependencies"

sudo apt-get install git -y
git clone https://github.com/SensorsIot/IOTstack.git
cd IOTstack

if [ $? -eq 0 ]; then
  echo "IOTstack cloned"
else
  echo "Could not find IOTstack directory"
	exit 5
fi

do_python3_checks
do_docker_checks
echo "Setting up environment:"
if [[ ! "$(user_in_group bluetooth)" == "notgroup" ]] && [[ ! "$(user_in_group bluetooth)" == "true" ]]; then
	echo "User is NOT in 'bluetooth' group. Adding:" >&2
	echo "sudo usermod -G bluetooth -a $USER" >&2
	echo "You will need to restart your system before the changes take effect."
	sudo usermod -G "bluetooth" -a $USER
fi

if [ ! "$(user_in_group docker)" == "true" ]; then
	echo "User is NOT in 'docker' group. Adding:" >&2
	echo "sudo usermod -G docker -a $USER" >&2
	echo "You will need to restart your system before the changes take effect."
	sudo usermod -G "docker" -a $USER
fi
do_env_checks
do_kernel_checks
