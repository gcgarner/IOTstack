# Default passwords and ports

Here you can find a list of the default configurations for IOTstack for quick reference.

## A word of caution
While it is convenient to leave passwords and ports set to their factory value, for security reasons we __strongly__ encourage you to use a randomly generated password for services that require passwords, and/or setup a reverse nginx proxy to require authentication before proxying to services. Only allowing connections originating from LAN or VPN is another way to help secure your services. Security requires a multi-pronged approach.

For services in host mode, only the external port is shown(if required).

## List of defaults

| Service Name   | Username | Password | External Port | Internal Port | Multiple Passwords  |
| -------------- | ---------------- | ---------------- | -------------------------------- | ------------------ | ----|
| adguardhome    | *none*           | *none*     | 8089<br>3001<br>53  | 8089<br>3001<br>53 | No |
| adminer        | *none*           | *none*     | 9080   | 8080 | No  |
| blynk_server   | *none*           | *none*     | 8180<br>8440<br>9443<br> | 8080<br>8440<br>9443<br> | No |
| chronograf     | *none*           | *none*     | 8888   | 8888 | No  |
| dashmachine    | *none*           | *none*     | 5000   | 5000 | No  |
| deconz         | *none*           | IOtSt4ckDec0nZ | 8090<br>443<br>5901 | 80<br>443<br>5900 | No |
| diyhue         | *none*           | *none*     | 8070<br>1900<br>1982<br>2100 | 80<br>1900<br>1982<br>2100| No |
| domoticz       | *none*           | *none*     | 8083<br>6144<br>1443 | 8080<br>6144<br>1443| No |
| dozzle         | *none*           | *none*     | 8889   | 8080 | No  |
| duckdns        | *none*           | *none*     |        |      | No  |
| espruinohub    | *none*           | *none*     | 1888   |      | No  |
| gitea          | *none*           | *none*     | 7920<br>2222   | 3000<br>22| No |
| grafana        | *none*           | *none*     | 3000   | 3000 | No  |
| heimdall       | *none*           | *none*     | 8880<br>8883  | 80<br>443| No |
| home_assistant | *none*           | *none*     | 8123   |      | No  |
| homebridge     | *none*           | *none*     | 8581   |      | No  |
| homer          | *none*           | *none*     | 8881   | 8080 | No  |
| influxdb       | *none*           | *none*     | 8086   | 8086 | Yes |
| influxdb2      | *none*           | *none*     | 8087   | 8086 | Yes |
| kapacitor      | *none*           | *none*     | 9092   | 9092 | Yes |
| mariadb        | mariadbuser      | IOtSt4ckmariaDbPw   | 3306 | 3306| Yes |
| mosquitto      | *none*           | *none*     | 1883   |1883  | No  |
| motioneye      | *none*           | *none*     | 8765<br>8081  |8765<br>8081 | No |
| n8n            | *none*           | *none*     | 5678   |5678  | No  |
| nextcloud      | *none*           | *none*     | 9321   |80    | No  |
| nodered        | *none*           | *none*     | 1880   | 1880 | No  |
| octoprint      | *none*           | *none*     | 9980   | 80   | No  |
| openhab        | *none*           | *none*     | 4050   |      | No  |
| pihole         | *none*           | *none*     | 8089<br>53<br>67 | 80<br>53<br>67 | No  |
| plex           | *none*           | *none*     | 32400  |      | No  |
| portainer-agent| *none*           | *none*     | 9001   | 9001 | No  |
| portainer-ce   | *none*           | *none*     | 8000<br>9000  | 8000<br>9000 | No |
| postgres       | postuser         | IOtSt4ckpostgresDbPw   | 5432 | 5432| Yes |
| prometheus     | *none*           | *none*     | 9090   |9090  | No  |
| prometheus-cadvisor | *none*      | *none*     | 8082   |8080  | No  |
| prometheus-nodeexporter | *none*  | *none*     | 9100   |      | No  |
| python         | *none*           | *none*     | *none* |*none*| No  |
| qbittorrent    | *none*           | *none*     | 15080<br>6881<br>1080 |15080<br>6881<br>1080 | No  |
| ring-mqtt      | *none*           | *none*     | 8554<br>55123 |8554<br>55123 | No  |
| rtl_433        | *none*           | *none*     | *none* |*none*| No  |
| scrypted       | *none*           | *none*     | 10443  |      | No  |
| syncthing      | *none*           | *none*     | 8384<br>22000<br>21027 |      | No |
| tasmoadmin     | *none*           | *none*     | 8088   | 80   | No  |
| telegraf       | *none*           | *none*     | 8092<br>8094<br>8125| 8092<br>8094<br>8125 | No |
| timescaledb    | postgres         | IOtSt4ckTim3Scale   | 5433 |5432 | No |
| transmission   | *none*           | *none*     | 9091<br>51413<br>   | 9091<br>51413<br> | No |
| webthingsio_gateway | *none*      | *none*     | 4060<br>4061  |     | No |
| wireguard      | *none*           | *none*     | 51820  | 51820| No |
| zerotier-client| *none*           | *none*     |        |      | No |
| zerotier-router| *none*           | *none*     |        |      | No |
| zigbee2mqtt    | *none*           | *none*     | 8080   | 8080 | No |
| zigbee2mqtt_assistant | *none*    | *none*     | 8880   | 80   | No |
