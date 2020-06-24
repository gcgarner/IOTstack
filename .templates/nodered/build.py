#!/usr/bin/env python3

issues = {} # Returned issues dict
buildHooks = {} # Options, and others hooks
haltOnErrors = True

# Main wrapper function. Required to make local vars work correctly
def main():
  import os
  import time
  import yaml
  import signal
  from blessed import Terminal
  
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
    global buildHooks
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
    subprocess.call("./.templates/nodered/build.sh", shell=True) # TODO: Put this step into the new build system
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

  ############################
  # Menu Logic
  ############################

  global currentMenuItemIndex
  global selectionInProgress
  global menuNavigateDirection
  global needsRender

  selectionInProgress = True
  currentMenuItemIndex = 0
  menuNavigateDirection = 0
  needsRender = 1
  term = Terminal()
  hotzoneLocation = [((term.height // 16) + 6), 0]

  def goBack():
    global selectionInProgress
    global needsRender
    selectionInProgress = False
    needsRender = 1
    print("Back to build stack menu")
    return True

  def onResize(sig, action):
    global nodeRedBuildOptions
    global currentMenuItemIndex
    mainRender(1, nodeRedBuildOptions, currentMenuItemIndex)

  def selectNodeRedAddons():
    global needsRender
    dockerCommandsFilePath = "./.templates/nodered/addons.py"
    with open(dockerCommandsFilePath, "rb") as pythonDynamicImportFile:
      code = compile(pythonDynamicImportFile.read(), dockerCommandsFilePath, "exec")
    # execGlobals = globals()
    # execLocals = locals()
    execGlobals = {}
    execLocals = {}
    screenActive = False
    exec(code, execGlobals, execLocals)
    signal.signal(signal.SIGWINCH, onResize)
    screenActive = True
    needsRender = 1

  nodeRedBuildOptions = [
    ["Select Addons", selectNodeRedAddons],
    ["Go back", goBack]
  ]

  def runOptionsMenu():
    menuEntryPoint()
    return True

  def renderHotZone(term, menu, selection, hotzoneLocation):
    lineLengthAtTextStart = 75
    print(term.move(hotzoneLocation[0], hotzoneLocation[1]))
    for (index, menuItem) in enumerate(menu):
      toPrint = ""
      if index == selection:
        toPrint += ('|   {t.blue_on_green} {title} {t.normal}'.format(t=term, title=menuItem[0]))
      else:
        toPrint += ('|   {t.normal} {title} '.format(t=term, title=menuItem[0]))

      for i in range(lineLengthAtTextStart - len(menuItem[0])):
        toPrint += " "

      toPrint += "|"

      toPrint = term.center(toPrint)

      print(toPrint)

  def mainRender(needsRender, menu, selection):
    term = Terminal()
    
    if needsRender == 1:
      print(term.clear())
      print(term.move_y(term.height // 16))
      print(term.black_on_cornsilk4(term.center('IOTstack NodeRed Options')))
      print("")
      # print(term.center("╔════════════════════════════════════════════════════════════════════════════════╗"))
      print(term.center("/--------------------------------------------------------------------------------\\"))
      print(term.center("|                                                                                |"))
      print(term.center("|      Select Option to configure                                                |"))
      print(term.center("|                                                                                |"))

    if needsRender >= 1:
      renderHotZone(term, menu, selection, hotzoneLocation)

    if needsRender == 1:
      print(term.center("|                                                                                |"))
      print(term.center("|                                                                                |"))
      print(term.center("|      Controls:                                                                 |"))
      print(term.center("|      [Up] and [Down] to move selection cursor                                  |"))
      print(term.center("|      [Enter] to run command                                                    |"))
      print(term.center("|      [Escape] to go back to main menu                                          |"))
      print(term.center("|                                                                                |"))
      print(term.center("|                                                                                |"))
      # print(term.center("╚════════════════════════════════════════════════════════════════════════════════╝"))
      print(term.center("\\--------------------------------------------------------------------------------/"))

  def runSelection(selection):
    import types
    if len(nodeRedBuildOptions[selection]) > 1 and isinstance(nodeRedBuildOptions[selection][1], types.FunctionType):
      nodeRedBuildOptions[selection][1]()
    else:
      print(term.green_reverse('IOTstack Error: No function assigned to menu item: "{}"'.format(nodeRedBuildOptions[selection][0])))

  def isMenuItemSelectable(menu, index):
    if len(menu) > index:
      if len(menu[index]) > 2:
        if menu[index][2]["skip"] == True:
          return False
    return True

  def menuEntryPoint():
    # These need to be reglobalised due to eval()
    global currentMenuItemIndex
    global selectionInProgress
    global menuNavigateDirection
    global needsRender
    term = Terminal()
    with term.fullscreen():
      menuNavigateDirection = 0
      mainRender(needsRender, nodeRedBuildOptions, currentMenuItemIndex)
      selectionInProgress = True
      with term.cbreak():
        while selectionInProgress:
          menuNavigateDirection = 0

          if needsRender: # Only rerender when changed to prevent flickering
            mainRender(needsRender, nodeRedBuildOptions, currentMenuItemIndex)
            needsRender = 0

          key = term.inkey()
          if key.is_sequence:
            if key.name == 'KEY_TAB':
              menuNavigateDirection += 1
            if key.name == 'KEY_DOWN':
              menuNavigateDirection += 1
            if key.name == 'KEY_UP':
              menuNavigateDirection -= 1
            if key.name == 'KEY_ENTER':
              runSelection(currentMenuItemIndex)
            if key.name == 'KEY_ESCAPE':
              return True
          elif key:
            print("got {0}.".format(key))

          if menuNavigateDirection != 0: # If a direction was pressed, find next selectable item
            currentMenuItemIndex += menuNavigateDirection
            currentMenuItemIndex = currentMenuItemIndex % len(nodeRedBuildOptions)
            needsRender = 2

            while not isMenuItemSelectable(nodeRedBuildOptions, currentMenuItemIndex):
              currentMenuItemIndex += menuNavigateDirection
              currentMenuItemIndex = currentMenuItemIndex % len(nodeRedBuildOptions)
    return True

  ####################
  # End menu section
  ####################

  if haltOnErrors:
    eval(toRun)()
  else:
    try:
      eval(toRun)()
    except:
      pass

# This check isn't required, but placed here for debugging purposes
global currentServiceName # Name of the current service
if currentServiceName == 'nodered':
  main()
else:
  print("Error. '{}' Tried to run 'nodered' config".format(currentServiceName))
