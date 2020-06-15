# Grafana
## References
- [Docker](https://hub.docker.com/r/grafana/grafana)
- [Website](https://grafana.com/)

## Security 
Grafana's default credentials are username "admin" password "admin" it will ask you to choose a new password on boot. Go to `<yourIP>:3000` in your web browser.

## Overwriting grafana.ini settings

A list of the settings available in grafana.ini are listed [here](https://grafana.com/docs/installation/configuration/)

To overwrite a setting edit the IOTstack/services/grafana/grafana.env file. The format is `GF_<SectionName>_<KeyName>`

An example would be:
```
GF_PATHS_DATA=/var/lib/grafana
GF_PATHS_LOGS=/var/log/grafana
# [SERVER]
GF_SERVER_ROOT_URL=http://localhost:3000/grafana
GF_SERVER_SERVE_FROM_SUB_PATH=true
# [SECURITY]
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
```

After the alterations run `docker-compose up -d` to pull them in
