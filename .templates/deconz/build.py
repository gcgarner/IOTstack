#!/usr/bin/env python3

issues = {} # Returned issues dict
buildHooks = {} # Options, and others hooks
haltOnErrors = True

# Main wrapper function. Required to make local vars work correctly
def main():
  global dockerComposeYaml # The loaded memory YAML of all checked services
  global toRun # Switch for which function to run when executed
  global buildHooks # Where to place the options menu result
  global currentServiceName # Name of the current service
  global issues # Returned issues dict
  global haltOnErrors # Turn on to allow erroring

  # runtime vars
  portConflicts = []

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
      buildHooks["runChecksHook"] = callable(checkForIssues)
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
    import time
    import subprocess
    print("Starting NodeRed Build script")
    time.sleep(0.2)
    subprocess.call("./.templates/deconz/build.sh", shell=True) # TODO: Put this step into the new build system
    print("Finished NodeRed Build script")
    time.sleep(0.2)
    return True

  # #####################################
  # Supporting functions below
  # #####################################

  def checkForIssues():
    for (index, serviceName) in enumerate(dockerComposeYaml):
      if not currentServiceName == serviceName: # Skip self
        currentServicePorts = getExternalPorts(currentServiceName)
        portConflicts = checkPortConflicts(serviceName, currentServicePorts)
        if (len(portConflicts) > 0):
          issues["portConflicts"] = portConflicts

  def getExternalPorts(serviceName):
    externalPorts = []
    try:
      yamlService = dockerComposeYaml[serviceName]
      if "ports" in yamlService:
        for (index, port) in enumerate(yamlService["ports"]):
          try:
            externalAndInternal = port.split(":")
            externalPorts.append(externalAndInternal[0])
          except:
            pass
    except:
      pass
    return externalPorts

  def checkPortConflicts(serviceName, currentPorts):
    portConflicts = []
    if not currentServiceName == serviceName:
      yamlService = dockerComposeYaml[serviceName]
      servicePorts = getExternalPorts(serviceName)
      for (index, servicePort) in enumerate(servicePorts):
        for (index, currentPort) in enumerate(currentPorts):
          if (servicePort == currentPort):
            portConflicts.append([servicePort, serviceName])
    return portConflicts

  if haltOnErrors:
    eval(toRun)()
  else:
    try:
      eval(toRun)()
    except:
      pass

# This check isn't required, but placed here for debugging purposes
global currentServiceName # Name of the current service
if currentServiceName == 'deconz':
  main()
else:
  print("Error. '{}' Tried to run 'deconz' config".format(currentServiceName))
