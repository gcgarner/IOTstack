#!/bin/bash
# vim: noexpandtab

# go to the absolute path of menu.sh
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_BRANCH=$(git name-rev --name-only HEAD)

# Minimum Software Versions
REQ_DOCKER_VERSION=18.2.0
REQ_PYTHON_VERSION=3.6.9

PYTHON_CMD=python3

sys_arch=$(uname -m)

# ----------------------------------------------
# Helper functions
# ----------------------------------------------
function command_exists() {
	command -v "$@" > /dev/null 2>&1
}

function user_in_group()
{
    # see if the group exists
    grep -q "^$1:" /etc/group;

    # sense that the group does not exist
    if [ $? -ne 0 ]; then return 0; fi

    # group exists - now check that the user is a member
    groups | grep -q "\b$1\b"
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

	NUMB_REG='^[0-9]+$'
	if ! [[ $CURR_VERSION_MAJOR =~ $NUMB_REG ]] ; then
		echo "$VERSION_GOOD"
		return 1
	fi
	if ! [[ $CURR_VERSION_MINOR =~ $NUMB_REG ]] ; then
		echo "$VERSION_GOOD"
		return 1
	fi
	if ! [[ $CURR_VERSION_BUILD =~ $NUMB_REG ]] ; then
		echo "$VERSION_GOOD"
		return 1
	fi

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

function check_git_updates()
{
	UPSTREAM=${1:-'@{u}'}
	LOCAL=$(git rev-parse @)
	REMOTE=$(git rev-parse "$UPSTREAM")
	BASE=$(git merge-base @ "$UPSTREAM")

	if [ "$LOCAL" = "$REMOTE" ]; then
			echo "Up-to-date"
	elif [ "$LOCAL" = "$BASE" ]; then
			echo "Need to pull"
	elif [ "$REMOTE" = "$BASE" ]; then
			echo "Need to push"
	else
			echo "Diverged"
	fi
}
function install_python3_and_deps() {
	CURR_PYTHON_VER="${1:-Unknown}"
	CURR_VIRTUALENV="${2:-Unknown}"
	if (whiptail --title "Python 3 and virtualenv" --yesno "Python 3.6.9 or later (Current = $CURR_PYTHON_VER) and virtualenv (Installed = $CURR_VIRTUALENV) are required for IOTstack to function correctly. Install these now?" 20 78); then
		sudo apt update
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
	sudo bash ./scripts/install_docker.sh install
}

function update_docker() {
	sudo bash ./scripts/install_docker.sh upgrade
}

function update_project() {
	git pull origin $CURRENT_BRANCH
	git status
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
		echo "You will need to restart your system before the changes take effect."
		sudo usermod -G "bluetooth" -a $USER
	fi

	if [ ! "$(user_in_group docker)" == "true" ]; then
    echo "User is NOT in 'docker' group. Adding:" >&2
    echo "sudo usermod -G docker -a $USER" >&2
		echo "You will need to restart your system before the changes take effect."
		sudo usermod -G "docker" -a $USER
	fi
}

function do_docker_checks() {
	if command_exists docker; then
		DOCKER_VERSION_GOOD="false"
		DOCKER_VERSION=$(docker version -f "{{.Server.Version}}" 2>&1)
		echo "Command: docker version -f \"{{.Server.Version}}\""
		if [[ "$DOCKER_VERSION" == *"Cannot connect to the Docker daemon"* ]]; then
			echo "Error getting docker version. Error when connecting to docker daemon. Check that docker is running."
			if (whiptail --title "Docker and Docker-Compose" --yesno "Error getting docker version. Error when connecting to docker daemon. Check that docker is running.\n\nCommand: docker version -f \"{{.Server.Version}}\"\n\nExit?" 20 78); then
				exit 1
			fi
		elif [[ "$DOCKER_VERSION" == *" permission denied"* ]]; then
			echo "Error getting docker version. Received permission denied error. Try running with: ./menu.sh --run-env-setup"
			if (whiptail --title "Docker and Docker-Compose" --yesno "Error getting docker version. Received permission denied error.\n\nTry rerunning the menu with: ./menu.sh --run-env-setup\n\nExit?" 20 78); then
				exit 1
			fi
			return 0
		fi
		
		if [[ -z "$DOCKER_VERSION" ]]; then
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
			if [ ! -f .docker_outofdate ]; then
				if (whiptail --title "Docker and Docker-Compose Version Issue" --yesno "Docker version is currently $DOCKER_VERSION which is less than $REQ_DOCKER_VERSION consider upgrading or you may experience issues. You will not be prompted again. You can manually upgrade by typing:\n  sudo apt upgrade docker docker-compose\n\nAttempt to upgrade now?" 20 78); then
					update_docker
				else
					touch .docker_outofdate
				fi
			fi
		fi
	else
		[ -f .docker_outofdate ] && rm .docker_outofdate
		echo "Docker not installed" >&2
		if [ ! -f .docker_notinstalled ]; then
			if (whiptail --title "Docker and Docker-Compose" --yesno "Docker is not currently installed, and is required to run IOTstack. Would you like to install docker and docker-compose now?\nYou will not be prompted again." 20 78); then
					[ -f .docker_notinstalled ] && rm .docker_notinstalled
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
					install_docker
				else
					touch .docker_notinstalled
			fi
		fi
	fi
}

function do_project_checks() {
	echo "Checking for project update" >&2
	git fetch origin $CURRENT_BRANCH

	if [[ "$(check_git_updates)" == "Need to pull" ]]; then
		echo "An update is available for IOTstack" >&2
		if [ ! -f .project_outofdate ]; then
			if (whiptail --title "Project update" --yesno "An update is available for IOTstack\nYou will not be reminded again until after you update.\nYou can upgrade manually by typing:\n  git pull origin $CURRENT_BRANCH \n\n\nWould you like to update now?" 14 78); then
				update_project
			else
				touch .project_outofdate
			fi
		fi
	else
		[ -f .project_outofdate ] && rm .project_outofdate
		echo "Project is up to date" >&2
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

# ----------------------------------------------
# Menu bootstrap entry point
# ----------------------------------------------

if [[ "$*" == *"--no-check"* ]]; then
	echo "Skipping preflight checks."
else
	do_project_checks
	do_env_checks
	do_python3_checks
	echo "Please enter sudo pasword if prompted"
	do_docker_checks

	if [[ "$DOCKER_VERSION_GOOD" == "true" ]] && \
		[[ "$PYTHON_VERSION_GOOD" == "true" ]]; then
		echo "Project dependencies up to date"
		echo ""
	else
		echo "Project dependencies not up to date. Menu may crash."
		echo "To be prompted to update again, run command:"
		echo "  rm .docker_notinstalled || rm .docker_outofdate || rm .project_outofdate"
		echo ""
	fi
fi

while test $# -gt 0
do
	case "$1" in
		--branch) CURRENT_BRANCH=${2:-$(git name-rev --name-only HEAD)}
			;;
		--no-check) echo ""
			;;
		--run-env-setup) # Sudo cannot be run from inside functions.
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
			;;
		--encoding) ENCODING_TYPE=$2
			;;
		--*) echo "bad option $1"
			;;
	esac
	shift
done

# This section is temporary, it's just for notifying people of potential breaking changes.
if [[ -f .new_install ]]; then
	echo "Existing installation detected."
else
	if [[ -f docker-compose.yml ]]; then
		echo "Warning: Please ensure to read the following prompt"
		sleep 1
		if (whiptail --title "Project update" --yesno "There has been a large update to IOTstack, and there may be breaking changes to your current setup. Would you like to switch to the older branch by having the command:\ngit checkout old-menu\n\nrun for you?\n\nIt's suggested that you backup your existing IOTstack instance if you select No\n\nIf you run into problems, please open an issue: https://github.com/SensorsIot/IOTstack/issues\n\nOr Discord: https://discord.gg/ZpKHnks\n\nRelease Notes: https://github.com/SensorsIot/IOTstack/blob/master/docs/New-Menu-Release-Notes.md" 24 95); then
			echo "Running command: git checkout old-menu"
			git checkout old-menu
			sleep 2
		fi
	fi
	touch .new_install
fi

set -e # stop execution on failure
if cmp -s requirements-menu.txt .virtualenv-menu/requirements.txt; then
	echo "Using existing python virtualenv for menu"
	source .virtualenv-menu/bin/activate
else
	rm -rf .virtualenv-menu
	echo "Creating python virtualenv for menu..."
	virtualenv -q --seed pip .virtualenv-menu
	source .virtualenv-menu/bin/activate
	echo "Installing menu requirements into the virtualenv..."
	pip3 install -q -r requirements-menu.txt
	cp requirements-menu.txt .virtualenv-menu/requirements.txt
fi

# Hand control to new menu
$PYTHON_CMD ./scripts/menu_main.py $ENCODING_TYPE
