#!/bin/bash

pushd ~/IOTstack > /dev/null 2>&1

CURRENT_BRANCH=${1:-$(git name-rev --name-only HEAD)}

# Minimum Software Versions
COMPOSE_VERSION="3.6"
REQ_DOCKER_VERSION=18.2.0
REQ_PYTHON_VERSION=3.6.9
REQ_PIP_VERSION=3.6.9
REQ_PYYAML_VERSION=5.3.1
REQ_BLESSED_VERSION=1.17.5

PYTHON_CMD=python3
VGET_CMD="$PYTHON_CMD ./scripts/python_deps_check.py"

sys_arch=$(uname -m)

# ----------------------------------------------
# Helper functions
# ----------------------------------------------
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

function install_python3_and_deps() {
	CURR_PYTHON_VER="${1:-Unknown}"
	CURR_PYYAML_VER="${2:-Unknown}"
	if (whiptail --title "Python 3 and Dependencies" --yesno "Python 3.6.9 or later (Current = $CURR_PYTHON_VER), PyYaml 5.3.1 or later (Current = $CURR_PYYAML_VER), blessed and pip3 are required for the main menu and compose-overrides.yml file to merge into the docker-compose.yml file. Install these now?" 20 78); then
		sudo apt install -y python3-pip python3-dev
		if [ $? -eq 0 ]; then
			PYTHON_VERSION_GOOD="true"
		else
			echo "Failed to install Python" >&2
			exit 1
		fi
		pip3 install -U pyyaml==5.3.1 blessed
		if [ $? -eq 0 ]; then
			PYYAML_VERSION_GOOD="true"
			BLESSED_GOOD="true"
		else
			echo "Failed to install Python" >&2
			exit 1
		fi
	fi
}

function install_docker() {
	sudo source ./scripts/install_docker.sh install
}

function update_docker() {
	sudo source ./scripts/install_docker.sh upgrade
}

function update_project() {
	git pull origin $CURRENT_BRANCH
	git status
}

function do_python3_checks() {
	PYTHON_VERSION_GOOD="false"
	PYYAML_VERSION_GOOD="false"
	BLESSED_GOOD="false"

	if command_exists $PYTHON_CMD && command_exists pip3; then
		PYTHON_VERSION=$($PYTHON_CMD --version)
		PYTHON_VERSION_MAJOR=$(echo "$PYTHON_VERSION"| cut -d' ' -f 2 | cut -d'.' -f 1)
		PYTHON_VERSION_MINOR=$(echo "$PYTHON_VERSION"| cut -d'.' -f 2)
		PYTHON_VERSION_BUILD=$(echo "$PYTHON_VERSION"| cut -d'.' -f 3)

		PYYAML_VERSION=$($VGET_CMD --pyyaml-version)
		PYYAML_VERSION="${PYYAML_VERSION:-Unknown}"
		PYYAML_VERSION_MAJOR=$(echo "$PYYAML_VERSION"| cut -d' ' -f 2 | cut -d'.' -f 1)
		PYYAML_VERSION_MINOR=$(echo "$PYYAML_VERSION"| cut -d'.' -f 2)
		PYYAML_VERSION_BUILD=$(echo "$PYYAML_VERSION"| cut -d'.' -f 3)

		BLESSED_VERSION=$($VGET_CMD --blessed-version)
		BLESSED_VERSION="${BLESSED_VERSION:-Unknown}"
		BLESSED_VERSION_MAJOR=$(echo "$BLESSED_VERSION"| cut -d' ' -f 2 | cut -d'.' -f 1)
		BLESSED_VERSION_MINOR=$(echo "$BLESSED_VERSION"| cut -d'.' -f 2)
		BLESSED_VERSION_BUILD=$(echo "$BLESSED_VERSION"| cut -d'.' -f 3)

		printf "Python Version: '${PYTHON_VERSION:-Unknown}'. "
		if [ "$(minimum_version_check $REQ_PYTHON_VERSION $PYTHON_VERSION_MAJOR $PYTHON_VERSION_MINOR $PYTHON_VERSION_BUILD)" == "true" ]; then
			PYTHON_VERSION_GOOD="true"
			echo "Python is up to date." >&2
		else
			echo "Python is outdated." >&2
			install_python3_and_deps "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR.$PYTHON_VERSION_BUILD" "$PYYAML_VERSION_MAJOR.$PYYAML_VERSION_MINOR.$PYYAML_VERSION_BUILD"
			return 1
		fi
		printf "PyYAML Version: '$PYYAML_VERSION'. "
		if [ "$(minimum_version_check $REQ_PYYAML_VERSION $PYYAML_VERSION_MAJOR $PYYAML_VERSION_MINOR $PYYAML_VERSION_BUILD)" == "true" ]; then
			PYYAML_VERSION_GOOD="true"
			echo "PyYAML is up to date." >&2
		else
			echo "PyYAML is outdated." >&2
			if [ "$PYYAML_VERSION" != "Unknown" ]; then
				install_python3_and_deps "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR.$PYTHON_VERSION_BUILD" "$PYYAML_VERSION_MAJOR.$PYYAML_VERSION_MINOR.$PYYAML_VERSION_BUILD"
			else
				install_python3_and_deps "$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR.$PYTHON_VERSION_BUILD"
			fi
			return 1
		fi
		printf "Blessed Version: '$BLESSED_VERSION'. "
		if [ "$(minimum_version_check $REQ_BLESSED_VERSION $BLESSED_VERSION_MAJOR $BLESSED_VERSION_MINOR $BLESSED_VERSION_BUILD)" == "true" ]; then
			PYYAML_VERSION_GOOD="true"
			echo "Blessed is up to date." >&2
		else
			echo "Blessed is outdated." >&2
			if [ "$BLESSED_VERSION" != "Unknown" ]; then
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

function do_docker_checks() {
	if command_exists docker; then
		DOCKER_VERSION_GOOD="false"
		DOCKER_VERSION=$(docker version -f "{{.Server.Version}}")
		DOCKER_VERSION_MAJOR=$(echo "$DOCKER_VERSION"| cut -d'.' -f 1)
		DOCKER_VERSION_MINOR=$(echo "$DOCKER_VERSION"| cut -d'.' -f 2)
		DOCKER_VERSION_BUILD=$(echo "$DOCKER_VERSION"| cut -d'.' -f 3)

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
			if (whiptail --title "Docker and Docker-Compose" --yesno "Docker is not currently installed, and is required to run IOTstack. You will not be prompted again.\nWould you like to install docker and docker-compose now?" 20 78); then
					[ -f .docker_notinstalled ] && rm .docker_notinstalled
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

	if [ $(git status | grep -c "Your branch is up to date") -eq 1 ]; then
		[ -f .project_outofdate ] && rm .project_outofdate
		echo "Project is up to date" >&2
	else
		echo "An update is available for IOTstack" >&2
		if [ ! -f .project_outofdate ]; then
			if (whiptail --title "Project update" --yesno "An update is available for IOTstack\nYou will not be reminded again until after you update.\nYou can upgrade manually by typing:\n  git pull origin $CURRENT_BRANCH \n\n\nWould you like to update now?" 14 78); then
				update_project
			else
				touch .project_outofdate
			fi
		fi
	fi
}

# ----------------------------------------------
# Menu bootstrap entry point
# ----------------------------------------------
if [ "$2" = "--no-check" ]; then
	echo "Skipping preflight checks."
else
	do_project_checks
	do_python3_checks
	do_docker_checks

	if [ "$DOCKER_VERSION_GOOD" == "true" ] && \
		[ "$PYTHON_VERSION_GOOD" == "true" ] && \
		[ "$PYYAML_VERSION_GOOD" == "true" ] && \
		[ "$BLESSED_GOOD" == "true" ]; then
		echo "Project dependencies up to date"
		echo ""
	else
		echo "Project dependencies not up to date. Menu may crash."
		echo "To be prompted to update again, run command:"
		echo "  rm .docker_notinstalled || rm .docker_outofdate || rm .project_outofdate"
		echo ""
	fi
fi

# Hand control to new menu
$PYTHON_CMD ./scripts/menu_main.py

popd > /dev/null 2>&1
