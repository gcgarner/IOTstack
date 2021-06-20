# Build Stack Services system

This page explains how the build stack system works for developers.

## How to define a new service
A service only requires 2 files:
* `service.yml` - Contains data for docker-compose
* `build.py` - Contains logic that the menu system uses.

### A basic service
Inside the `service.yml` is where the service data for docker-compose is housed, for example:
```
adminer:
  container_name: adminer
  image: adminer
  restart: unless-stopped
  ports:
    - "9080:8080"
```
It is important that the service name match the directory that it's in - that means that the `adminer` service must be placed into a folder called `adminer` inside the `./.templates` directory.


### Basic build code for service
At the very least, the `build.py` requires the following code:
```
#!/usr/bin/env python3

issues = {} # Returned issues dict
buildHooks = {} # Options, and others hooks
haltOnErrors = True

# Main wrapper function. Required to make local vars work correctly
def main():
  global currentServiceName # Name of the current service

  # This lets the menu know whether to put " >> Options " or not
  # This function is REQUIRED.
  def checkForOptionsHook():
    try:
      buildHooks["options"] = callable(runOptionsMenu)
    except:
      buildHooks["options"] = False
      return buildHooks
    return buildHooks

  # This function is REQUIRED.
  def checkForPreBuildHook():
    try:
      buildHooks["preBuildHook"] = callable(preBuild)
    except:
      buildHooks["preBuildHook"] = False
      return buildHooks
    return buildHooks

  # This function is REQUIRED.
  def checkForPostBuildHook():
    try:
      buildHooks["postBuildHook"] = callable(postBuild)
    except:
      buildHooks["postBuildHook"] = False
      return buildHooks
    return buildHooks

  # This function is REQUIRED.
  def checkForRunChecksHook():
    try:
      buildHooks["runChecksHook"] = callable(runChecks)
    except:
      buildHooks["runChecksHook"] = False
      return buildHooks
    return buildHooks

  # Entrypoint for execution
  if haltOnErrors:
    eval(toRun)()
  else:
    try:
      eval(toRun)()
    except:
      pass

# This check isn't required, but placed here for debugging purposes
global currentServiceName # Name of the current service
if currentServiceName == 'adminer': # Make sure you update this.
  main()
else:
  print("Error. '{}' Tried to run 'adminer' config".format(currentServiceName))
```
This code doesn't have any port conflicting checking or menu code in it, and just allows the service to be built as is. The best way to learn on extending the functionality of the service's build script is to look at the other services' build scripts. You can also check out the advanced sections on adding menus and checking for issues for services though for a deeper explanation of specific situations.

### Basic code for a service that uses bash
If Python isn't your thing, here's a code blob you can copy and paste. Just be sure to update the lines where the comments start with `---`
```
#!/usr/bin/env python3

issues = {} # Returned issues dict
buildHooks = {} # Options, and others hooks
haltOnErrors = True

# Main wrapper function. Required to make local vars work correctly
def main():
  import subprocess
  global dockerComposeServicesYaml # The loaded memory YAML of all checked services
  global toRun # Switch for which function to run when executed
  global buildHooks # Where to place the options menu result
  global currentServiceName # Name of the current service
  global issues # Returned issues dict
  global haltOnErrors # Turn on to allow erroring

  from deps.consts import servicesDirectory, templatesDirectory, volumesDirectory, servicesFileName

  # runtime vars
  serviceVolume = volumesDirectory + currentServiceName # Unused in example
  serviceService = servicesDirectory + currentServiceName # Unused in example
  serviceTemplate = templatesDirectory + currentServiceName

  # This lets the menu know whether to put " >> Options " or not
  # This function is REQUIRED.
  def checkForOptionsHook():
    try:
      buildHooks["options"] = callable(runOptionsMenu)
    except:
      buildHooks["options"] = False
      return buildHooks
    return buildHooks

  # This function is REQUIRED.
  def checkForPreBuildHook():
    try:
      buildHooks["preBuildHook"] = callable(preBuild)
    except:
      buildHooks["preBuildHook"] = False
      return buildHooks
    return buildHooks

  # This function is REQUIRED.
  def checkForPostBuildHook():
    try:
      buildHooks["postBuildHook"] = callable(postBuild)
    except:
      buildHooks["postBuildHook"] = False
      return buildHooks
    return buildHooks

  # This function is REQUIRED.
  def checkForRunChecksHook():
    try:
      buildHooks["runChecksHook"] = callable(runChecks)
    except:
      buildHooks["runChecksHook"] = False
      return buildHooks
    return buildHooks

  # This service will not check anything unless this is set
  # This function is optional, and will run each time the menu is rendered
  def runChecks():
    checkForIssues()
    return []

  # This function is optional, and will run after the docker-compose.yml file is written to disk.
  def postBuild():
    return True

  # This function is optional, and will run just before the build docker-compose.yml code.
  def preBuild():
    execComm = "bash {currentServiceTemplate}/build.sh".format(currentServiceTemplate=serviceTemplate) # --- You may want to change this
    print("[Wireguard]: ", execComm) # --- Ensure to update the service name with yours
    subprocess.call(execComm, shell=True) # This is where the magic happens
    return True

  # #####################################
  # Supporting functions below
  # #####################################

  def checkForIssues():
    return True

  if haltOnErrors:
    eval(toRun)()
  else:
    try:
      eval(toRun)()
    except:
      pass

# This check isn't required, but placed here for debugging purposes
global currentServiceName # Name of the current service
if currentServiceName == 'wireguard': # --- Ensure to update the service name with yours
  main()
else:
  print("Error. '{}' Tried to run 'wireguard' config".format(currentServiceName)) # --- Ensure to update the service name with yours

```