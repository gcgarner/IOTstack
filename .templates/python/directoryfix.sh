#!/bin/bash

# Directoryfix for python

if [ ! -d ./volumes/python/app ]; then
	sudo mkdir -p ./volumes/python/app
	sudo chown -R $(whoami):$(whoami) ./volumes/python
	echo 'print("hello world")' >./volumes/python/app/app.py

fi
