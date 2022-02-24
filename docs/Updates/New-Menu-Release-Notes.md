# New IOTstack Menu

## Background
Originally this script was written in bash. After a while it became obvious that bash wasn't well suited to dealing with all the different types of configuration files, and logic that goes with configuring everything. IOTstack needs to be accessible to all levels of programmers and tinkerers, not just ones experienced with Linux and bash. For this reason, it was rewritten in Python since the language syntax is easier to understand, and is more commonly used for scripting and programming than bash. Bash is still used in IOTstack where it makes sense to use it, but the menu system itself uses Python. The code is intentionally made so that beginners and experienced programmers could contribute to the project. We are always open to improvements if you have suggestions.

## On-going improvements
There are many features that are needing to be introduced into the new menu system. From meta tags on services for filtering, to optional nginx autoconfiguration and authentication. For this reason you may initially experience bugs (very hard to test every type of configuration!). The new menu system has been worked on and tested for 6 months and we think it's stable enough to merge into the master branch for mainstream usage. The code still needs some work to make it easier to add new services and to not require copy pasting the same code for each new service. Also to make the menu system not be needed at all (so it can be automated with bash scripts).

## Breaking changes
There are a few changes that you need to be aware of:

* Docker Environmental `*.env` files are no longer a thing by default. Everything needed is specified in the service.yml file, you can still optionally use them though either with [Custom Overrides](../Basic_setup/Custom.md) or with the [PostBuild](../Developers/PostBuild-Script.md) script. Specific config files for certain services still work as they once did.
* Python 3, pip3, PyYAML and Blessed are all required to be installed.
* Not backwards compatible with old menu system. You will be able to switch back to the old menu system for a period of time by changing to the `old-menu` branch. It will be unmaintained except for critical updates. It will eventually be removed - but not before everyone is ready to leave it.

**Test that your backups are working before you switch.** The `old-menu` branch will become avaiable just before the new menu is merged into master to ensure it has the latest commits applied.

## Full change list
* Menu and everything that goes with it rewritten in Python and Blessed
* Easy installation script
* All services rewritten to be compatible with PyYAML
* Optional port selection for services
* Issue checking for services before building
* Options for services now in menu (no more editing `service.yml` files)
* Automatic password generation for each service
* Pre and post scripts for customising services
* Removed env files
* Backup and restoring more streamlined
* Documentation updated for all services
* No longer needs to be installed in the home directory `~`.
