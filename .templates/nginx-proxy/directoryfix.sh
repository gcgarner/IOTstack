#!/bin/bash
if [ ! -d ./volumes/nginx-proxy/nginx-conf ]; then
	sudo mkdir -p ./volumes/nginx-proxy/nginx-conf
	sudo chown -R pi:pi ./volumes/nginx-proxy/nginx-conf
fi

if [ ! -d ./volumes/nginx-proxy/nginx-vhost ]; then
	sudo mkdir -p ./volumes/nginx-proxy/nginx-vhost
	sudo chown -R pi:pi ./volumes/nginx-proxy/nginx-vhost
fi

if [ ! -d ./volumes/nginx-proxy/html ]; then
	sudo mkdir -p ./volumes/nginx-proxy/html
	sudo chown -R pi:pi ./volumes/nginx-proxy/html
fi

if [ ! -d ./volumes/nginx-proxy/certs ]; then
	sudo mkdir -p ./volumes/nginx-proxy/certs
	sudo chown -R pi:pi ./volumes/nginx-proxy/certs
fi

if [ ! -d ./volumes/nginx-proxy/log ]; then
	sudo mkdir -p ./volumes/nginx-proxy/log
	sudo chown -R pi:pi ./volumes/nginx-proxy/log
fi

cp ./services/nginx-proxy//nginx.tmpl ./volumes/nginx-proxy
