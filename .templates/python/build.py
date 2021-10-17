#!/usr/bin/env python3

issues = {} # Returned issues dict
buildHooks = {} # Options, and others hooks
haltOnErrors = True

# Main wrapper function. Required to make local vars work correctly
def main():
  import os
  import time
  import shutil
  import subprocess
  import sys
  
  from deps.consts import servicesDirectory, templatesDirectory, volumesDirectory
  from deps.common_functions import getExternalPorts, getInternalPorts, checkPortConflicts

  global dockerComposeServicesYaml # The loaded memory YAML of all checked services
  global toRun # Switch for which function to run when executed
  global buildHooks # Where to place the options menu result
  global currentServiceName # Name of the current service
  global issues # Returned issues dict
  global haltOnErrors # Turn on to allow erroring
  global hideHelpText # Showing and hiding the help controls text
  global serviceService

  serviceService = servicesDirectory + currentServiceName
  serviceTemplate = templatesDirectory + currentServiceName
  serviceVolume = volumesDirectory + currentServiceName

  try: # If not already set, then set it.
    hideHelpText = hideHelpText
  except:
    hideHelpText = False

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
    # Setup service directory
    if not os.path.exists(serviceService):
      os.makedirs(serviceService, exist_ok=True)

    # copy supporting files
    shutil.copy(r'%s/Dockerfile' % serviceTemplate, r'%s/Dockerfile' % serviceService)
    shutil.copy(r'%s/docker-entrypoint.sh' % serviceTemplate, r'%s/docker-entrypoint.sh' % serviceService)
    shutil.copytree(r'%s/app' % serviceTemplate, r'%s/app' % serviceService)

    return True

  # #####################################
  # Supporting functions below
  # #####################################

  def checkForIssues():
    envFileIssues = checkEnvFiles()
    if (len(envFileIssues) > 0):
      issues["envFileIssues"] = envFileIssues
    for (index, serviceName) in enumerate(dockerComposeServicesYaml):
      if not currentServiceName == serviceName: # Skip self
        currentServicePorts = getExternalPorts(currentServiceName, dockerComposeServicesYaml)
        portConflicts = checkPortConflicts(serviceName, currentServicePorts, dockerComposeServicesYaml)
        if (len(portConflicts) > 0):
          issues["portConflicts"] = portConflicts

  def checkEnvFiles():
    envFileIssues = []
    if not os.path.exists(serviceTemplate + '/app/requirements.txt'):
      envFileIssues.append(serviceTemplate + '/app/requirements.txt does not exist')
    if not os.path.exists(serviceTemplate + '/app/app.py'):
      envFileIssues.append(serviceTemplate + '/app/app.py does not exist')
    return envFileIssues

  # #####################################
  # End Supporting functions
  # #####################################

  if haltOnErrors:
    eval(toRun)()
  else:
    try:
      eval(toRun)()
    except:
      pass

# This check isn't required, but placed here for debugging purposes
global currentServiceName # Name of the current service
if currentServiceName == 'python':
  main()
else:
  print("Error. '{}' Tried to run 'python' config".format(currentServiceName))
