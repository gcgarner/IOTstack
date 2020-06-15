#!/bin/bash

# create directories for named volumes
TRANSMISSION_BASEDIR=.volumes/transmission
mkdir -p $TRANSMISSION_BASEDIR/downloads
mkdir -p $TRANSMISSION_BASEDIR/watch
mkdir -p $TRANSMISSION_BASEDIR/config
