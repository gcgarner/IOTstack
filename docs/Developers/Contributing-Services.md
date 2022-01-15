# Contributing a service to IOTstack

On this page you can find information on how to contribute a service to IOTstack. We are generally very accepting of new services where they are useful. Keep in mind that if it is not IOTstack, selfhosted, or automation related we may not approve the PR.

Services will grow over time, we may split up the buildstack menu into subsections or create filters to make organising all the services we provide easier to find.

## Checks
* `service.yml` file is correct
* `build.py` file is correct
* Service allows for changing external WUI port from Build Stack's options menu if service uses a HTTP/S port
* Use a default password, or allow the user to generate a random password for the service for initial installation. If the service asks to setup an account this can be ignored.
* Ensure [Default Configs](../Default-Configs.md) is updated with WUI port and username/password.
* Must detect port confilicts with other services on [BuildStack](Menu-System.md) Menu.
* `Pre` and `Post` hooks work with no errors. 
* Does not require user to edit config files in order to get the service running.
* Ensure that your service can be backed up and restored without errors or data loss.
* Any configs that are required before getting the service running should be configured in the service's options menu (and a BuildStack menu Issue should be displayed if not).
* Fork the repo and push the changes to your fork. Create a cross repo PR for the mods to review. We may request additional changes from you.

## Follow up
If your new service is approved and merged then congratulations! Please watch the Issues page on github over the next few days and weeks to see if any users have questions or issues with your new service.

Links:

* [Default configs](../Default-Configs.md)
* [Password configuration for Services](BuildStack-RandomPassword.md)
* [Build Stack Menu System](Menu-System.md)
* [Coding a new service](BuildStack-Services.md)
* [IOTstack issues](htps://github.com/SensorsIot/IOTstack/issues)
