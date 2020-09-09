#!/bin/sh

NEWPORT=$(whiptail --inputbox "Enter in new port number (1-65535):" 8 78 "$1" --title "$2" 3>&1 1>&2 2>&3)
exitstatus=$?

if [ $exitstatus = 0 ]; then
  echo -n "$NEWPORT","$exitstatus"
else
  echo -n "CANCEL","$exitstatus"
fi