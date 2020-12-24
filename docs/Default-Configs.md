# Build Stack Default Passwords for Services

Here you can find a list of the default configurations for IOTstack for quick referece.

## A word of caution
While it is convienent to leave passwords and ports set to their factory value, for security reasons we __strongly__ encourage you to use a randomly generated password for services that require passwords, and/or setup a reverse nginx proxy to require authentication before proxying to services. Only allowing connections originating from LAN or VPN is another way to help secure your services. Security requires a multi-pronged approach.

Do note that the ports listed are not all of the ports containers use. They are mearly the WUI ports.

## List of defaults

| Service Name   | Default Username | Default Password | Default External HTTP/S WUI Port | Multiple Passwords |
| -------------- | ---------------- | ---------------- | -------------------------------- | ------------------ |
| adminer        | *none*           | *none*     | 9080   | No |
| blynk_server   | *none*           | *none*     | 8180   | No |
| deconz         | *none*           | IOtSt4ckDec0nZ | 8090 | No |
| diyhue         | *none*           | *none*     | 8070   | No |
| dozzle         | *none*           | *none*     | 8080   | No |
| espruinohub    | *none*           | *none*     | *none* | No |
| gitea          | *none*           | *none*     | 7920   | No |
| grafana        | *none*           | *none*     | 3000   | No |
| home_assistant | *none*           | *none*     | 8123   | No |
| homebridge     | *none*           | *none*     | 4040   | No |
| influxdb       | *none*           | *none*     | *none* | Yes |
| mariadb        | mariadbuser      | IOtSt4ckmariaDbPw | *none* | Yes |
| mosquitto      | *none*           | *none*     | *none* | No |
| motioneye      | *none*           | *none*     | 8765   | No |
| nextcloud      | *none*           | *none*     | 9321   | No |
| nodered        | nodered          | nodered    | 1880   | No |
| openhab        | *none*           | *none*     | 4050   | No |
| pihole         | *none*           | IOtSt4ckP1Hol3 | 8089 | No |
| plex           | *none*           | *none*     | *none* | No |
| portainer      | *none*           | *none*     | 9002   | No |
| portainer-ce   | *none*           | *none*     | 9001   | No |
| postgres       | postuser         | IOtSt4ckpostgresDbPw   | *none* | Yes |
| python         | *none*           | *none*     | *none* | No |
| rtl_433        | *none*           | *none*     | *none* | No |
| tasmoadmin     | *none*           | *none*     | 8088   | No |
| telegraf       | *none*           | *none*     | *none* | No |
| timescaledb    | timescaleuser    | IOtSt4ckTim3Scale | *none* | No |
| transmission   | *none*           | *none*     | 9091   | No |
| webthingsio_gateway | *none*      | *none*     | 4060   | No |
| zigbee2mqtt    | *none*           | *none*     | *none* | No |
| zigbee2mqtt_assistant | *none*    | *none* | *none* | No |
