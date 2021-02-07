#1/bin/bash

WG_CONF_TEMPLATE_PATH=./.templates/wireguard/wg0.conf
WG_CONF_DEST_PATH=./services/wireguard/config

if [[ ! -f $WG_CONF_TEMPLATE_PATH ]]; then
    echo "[Wireguard] Warning: $WG_CONF_TEMPLATE_PATH does not exist."
else 
    if [[ ! -d $WG_CONF_DEST_PATH ]]; then
        mkdir -p $WG_CONF_DEST_PATH
        cp -r $WG_CONF_TEMPLATE_PATH $WG_CONF_DEST_PATH
    fi;
fi
