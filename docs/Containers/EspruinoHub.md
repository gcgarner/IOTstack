# Espruinohub
This is a testing container

I tried it however the container keeps restarting `docker logs espruinohub` I get "BLE Broken?" but could just be i dont have any BLE devices nearby

web interface is on "{your_Pis_IP}:1888"

see https://github.com/espruino/EspruinoHub#status--websocket-mqtt--espruino-web-ide for other details

there were no recommendations for persistent data volumes. so `docker-compose down` may destroy all you configurations so use `docker-compose stop` in stead 

please let me know about your success or issues [here](https://github.com/gcgarner/IOTstack/issues/84)