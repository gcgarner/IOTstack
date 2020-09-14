# Contributong a service to IOTstack

On this page you can find information on how to contribute a service to IOTstack.

## Checks
* `service.yml` file is correct
* `build.py` file is correct
* Service allows for changing external port from Build Stack's options menu if service uses a port
* Use a default password, or allow the user to generate a random password for the service for initial installation.
* Ensure Default-Configs [Default Configs](https://sensorsiot.github.io/IOTstack/Default-Configs) is updated with port and username/password.
* Must detect port confilicts with other services on [BuildStack](https://sensorsiot.github.io/IOTstack/Menu-System) Menu.
* `Pre` and `Post` hooks work with no errors. 
* Does not require user to edit config files in order to get the service running
* Any configs that are required before getting the service running should be configured in the service's options menu (and an Issue should be raised if not).

Links:
* [Default configs](https://sensorsiot.github.io/IOTstack/Default-Configs)
* [Password configuration for Services](https://sensorsiot.github.io/IOTstack/BuildStack-RandomPassword)
* [Build Stack Menu System](https://sensorsiot.github.io/IOTstack/Menu-System)
* [Coding a new service](https://sensorsiot.github.io/IOTstack/BuildStack-Services)