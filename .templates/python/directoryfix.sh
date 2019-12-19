#!/bin/bash

# Directoryfix for python

if [ ! -d ./volumes/python/app ]; then
	sudo mkdir -p ./volumes/python/app
	sudo chown -R pi:pi ./volumes/python
	echo 'print("hello world")' >./volumes/python/app/app.py

fi
