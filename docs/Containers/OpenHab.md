# openHAB

## References

- [DockerHub](https://hub.docker.com/r/openhab/openhab/)
- [GitHub](https://github.com/openhab/openhab-docker)
- [openHAB website](https://www.openhab.org/)

openHAB runs in "host mode" so there are no port mappings. The default port bindings on IOTstack are:

* 4050 - the HTTP port of the web interface (instead of 8080)
* 4051 - the HTTPS port of the web interface (instead of 8443)
* 8101 - the SSH port of the Console (since openHAB 2.0.0)
* 5007 - the LSP port for validating rules (since openHAB 2.2.0)

If you want to change either of the first two:

1. Edit the `openhab` fragment in `docker-compose.yml`:

	```
	    - OPENHAB_HTTP_PORT=4050
	    - OPENHAB_HTTPS_PORT=4051
	```

2. Recreate the openHAB container:

	```
	$ cd ~/IOTstack
	$ docker-compose up -d openhab
	```

There do not appear to be any environment variables to control ports 8101 or 5007 so, if other containers you need to run also depend on those ports, you will have to figure out some way of resolving the conflict.

Note:

* The original IOTstack documentation included:

	> openHAB has been added without Amazon Dashbutton binding.

	but it is not clear if this is still the case.
	
* [Amazon Dashbuttons have been discontinued](https://www.theverge.com/2019/2/28/18245315/amazon-dash-buttons-discontinued) so this may no longer be relevant.

