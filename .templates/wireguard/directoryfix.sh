WG_CONF_TEMPLATE_PATH=./.templates/wireguard/wg0.conf
WG_CONF_DEST_PATH=./services/wireguard/config

if [[ ! -f $WG_CONF_TEMPLATE_PATH ]]; then
    echo "[Wireguard] Warning: $WG_CONF_TEMPLATE_PATH does not exist."
  else
    [ -d $WG_CONF_DEST_PATH ] || mkdir -p $WG_CONF_DEST_PATH
    cp -r $WG_CONF_TEMPLATE_PATH $WG_CONF_DEST_PATH
fi
