#!/bin/bash

# Directoryfix for python

#current user
u=$(whoami)

if [ ! -d ./volumes/python/app ]; then
	sudo mkdir -p ./volumes/python/app
	sudo chown -R $u:$u ./volumes/python
	echo 'print("hello world")' >./volumes/python/app/app.py

fi
