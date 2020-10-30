#!/bin/bash

# Created by: Slyke
# Email: steven.lawler777@gmail.com
# Version: 2 (IOTstack)
# Date: 2020-07-08
# This script allows you to automatically install SSH keys from your github account, and optionally disable password authentication for sshd.
# License: MIT

VERBOSE_MODE=0
DISABLE_PASSWORD_AUTH=0
SKIP_SSH_WARNING=0
AUTH_KEYS_FILE=~/.ssh/authorized_keys
SSH_CONFIG_FILE=/etc/ssh/sshd_config

function printHelp() {
  echo "Usage:"
  echo "  --quiet"
  echo "    No output, unless displaying errors or input is required."
  echo ""
  echo "  --clear"
  echo "    Clears all entries in $AUTH_KEYS_FILE"
  echo ""
  echo "  --username {USERNAME}"
  echo "    Set your github username so that you are not prompted for it"
  echo ""
  echo "  --disable-password-authentication"
  echo "    Updates $SSH_CONFIG_FILE to disable password authentication and then restarts ssh service. Requires sudo access. Warning: You may lock yourself out."
  echo ""
  echo "  --skip-ssh-warning"
  echo "    Skips the warning and the wait when --disable-password-authentication is set."
  echo ""
  echo "  --help"
  echo "    Displays this message"
  echo ""
  echo "Example:"
  echo "  $0 --clear --username slyke --quiet"
  echo ""
  exit 0
}

function setUsername() {
  GH_USERNAME=$1
}

function clearAuthKeys() {
  if [ -f $AUTH_KEYS_FILE ]; then
    echo "" > $AUTH_KEYS_FILE
  fi
}

function disablePasswordAuthentication () {
  sudo grep -q "ChallengeResponseAuthentication" $SSH_CONFIG_FILE && sed -i "/^[^#]*ChallengeResponseAuthentication[[:space:]]yes.*/c\ChallengeResponseAuthentication no" $SSH_CONFIG_FILE || echo "ChallengeResponseAuthentication no" >> $SSH_CONFIG_FILE
  sudo grep -q "^[^#]*PasswordAuthentication" $SSH_CONFIG_FILE && sed -i "/^[^#]*PasswordAuthentication[[:space:]]yes/c\PasswordAuthentication no" $SSH_CONFIG_FILE || echo "PasswordAuthentication no" >> $SSH_CONFIG_FILE
  sudo service ssh restart
}

while test $# -gt 0
do
  case "$1" in
    --quiet) VERBOSE_MODE=1
        ;;
    --username) setUsername $2
        ;;
    --clear) clearAuthKeys
        ;;
    --disable-password-authentication) DISABLE_PASSWORD_AUTH=1
        ;;
    --disable-password-auth) DISABLE_PASSWORD_AUTH=1
        ;;
    --disable-passwd-auth) DISABLE_PASSWORD_AUTH=1
        ;;
    --skip-ssh-warning) SKIP_SSH_WARNING=1
        ;;
    --help) printHelp
        ;;
    -h) printHelp
        ;;
    --*) echo "Bad option $1"; echo "For help use: $0 --help "; exit 3
        ;;
  esac
  shift
done

if [ -z ${GH_USERNAME+x} ]; then
  echo ""
  echo "Enter your github username"
  read GH_USERNAME;
fi

exec 3>&1
# exec 4>&2

if [[ "$VERBOSE_MODE" -eq 1 ]]; then
  exec 1>/dev/null
  # exec 2>/dev/null
fi

if [ ! -f $AUTH_KEYS_FILE ]; then
  echo "Created: '$AUTH_KEYS_FILE'"
  touch $AUTH_KEYS_FILE
fi

if [[ "$DISABLE_PASSWORD_AUTH" -eq 1 ]]; then
  if [[ ! "$SKIP_SSH_WARNING" -eq 1 ]]; then
    echo "Will disable password authentication and restart sshd service after installing ssh keys."
    echo "Press ctrl+c now to cancel."
    sleep 5
  fi
fi

SSH_KEYS=$(curl -s "https://github.com/$GH_USERNAME.keys")

KEYS_ADDED=0
KEYS_SKIPPED=0

if [[ "$SSH_KEYS" == "Not Found" ]]; then
  >&2 echo "Username '$GH_USERNAME' not found"
  >&2 echo "URL: 'https://github.com/$GH_USERNAME.keys'"
  exit 1
fi

if [[ ${#SSH_KEYS} -le 16 ]]; then
  >&2 echo "Something went wrong retrieving SSH keys for '$GH_USERNAME'"
  >&2 echo "URL: 'https://github.com/$GH_USERNAME.keys'"
  >&2 echo "Result: "
  >&2 echo "$SSH_KEYS"
  exit 2
fi

while read -r AUTH_KEY; do AUTHKEYS+=("$AUTH_KEY"); done <<<"$SSH_KEYS"

for i in "${!AUTHKEYS[@]}"; do
  if grep -Fxq "${AUTHKEYS[$i]}" $AUTH_KEYS_FILE ; then
    echo "Key $i already exists in '$AUTH_KEYS_FILE' Skipping..."
    KEYS_SKIPPED=$(( $KEYS_SKIPPED + 1 ))
  else
    echo "${AUTHKEYS[$i]}" >> $AUTH_KEYS_FILE
    echo "Key [$i] added."
    KEYS_ADDED=$(( $KEYS_ADDED + 1 ))
  fi
done

echo "Keys Added: $KEYS_ADDED"
echo "Keys Skipped: $KEYS_SKIPPED"

if [[ "$DISABLE_PASSWORD_AUTH" -eq 1 ]]; then
  echo "Disabling password authentication and restarting sshd:"
  disablePasswordAuthentication
fi
