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
  import shutil
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  from deps.consts import servicesDirectory, templatesDirectory
  from blessed import Terminal

  global dockerComposeYaml # The loaded memory YAML of all checked services
  global renderMode # For rendering fancy or basic ascii characters
  global toRun # Switch for which function to run when executed
  global buildHooks # Where to place the options menu result
  global currentServiceName # Name of the current service
  global issues # Returned issues dict
  global haltOnErrors # Turn on to allow erroring
  global serviceService
  global serviceTemplate
  global addonsFile

  # runtime vars
  portConflicts = []

  serviceService = servicesDirectory + currentServiceName
  serviceTemplate = templatesDirectory + currentServiceName
  addonsFile = serviceService + "/addons_list.yml"

  dockerfileTemplateReplace = "%run npm install modules list%"

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
    import time

    # Setup service directory
    if not os.path.exists(serviceService):
      os.makedirs(serviceService, exist_ok=True)

    # Files copy
    shutil.copy(r'%s/nodered.env' % serviceTemplate, r'%s/nodered.env' % serviceService)

    # Other prebuild steps
    print("Starting NodeRed Build script")
    time.sleep(0.1)
    with open(r'%s/Dockerfile.template' % serviceTemplate, 'r') as dockerTemplate:
      templateData = dockerTemplate.read()

    with open(r'%s' % addonsFile) as objAddonsFile:
      addonsSelected = yaml.load(objAddonsFile, Loader=yaml.SafeLoader)

    addonsInstallCommands = ""
    if os.path.exists(addonsFile):
      for (index, addonName) in enumerate(addonsSelected["addons"]):
        if (addonName == 'node-red-node-sqlite'):
          addonsInstallCommands = addonsInstallCommands + "RUN npm install --unsafe-perm {addonName}\n".format(addonName=addonName)
        else:
          addonsInstallCommands = addonsInstallCommands + "RUN npm install {addonName}\n".format(addonName=addonName)

    templateData = templateData.replace(dockerfileTemplateReplace, addonsInstallCommands)

    with open(r'%s/Dockerfile' % serviceService, 'w') as dockerTemplate:
      dockerTemplate.write(templateData)
    print("Finished NodeRed Build script")
    time.sleep(0.3)
    return True

  # #####################################
  # Supporting functions below
  # #####################################

  def checkForIssues():
    fileIssues = checkFiles()
    if (len(fileIssues) > 0):
      issues["fileIssues"] = fileIssues
    for (index, serviceName) in enumerate(dockerComposeYaml):
      if not currentServiceName == serviceName: # Skip self
        currentServicePorts = getExternalPorts(currentServiceName)
        portConflicts = checkPortConflicts(serviceName, currentServicePorts)
        if (len(portConflicts) > 0):
          issues["portConflicts"] = portConflicts

  def checkFiles():
    fileIssues = []
    if not os.path.exists(serviceTemplate + '/nodered.env'):
      fileIssues.append(serviceTemplate + '/nodered.env does not exist')
    if not os.path.exists(serviceService + '/addons_list.yml'):
      fileIssues.append(serviceService + '/addons_list.yml does not exist. Build addons file to fix.')
    return fileIssues

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
    execGlobals = {
      "currentServiceName": currentServiceName,
      "renderMode": renderMode
    }
    execLocals = {}
    screenActive = False
    exec(code, execGlobals, execLocals)
    signal.signal(signal.SIGWINCH, onResize)
    screenActive = True
    needsRender = 1

  nodeRedBuildOptions = []
  nodeRedBuildOptions.append(["Go back", goBack])

  if os.path.exists(serviceService + '/addons_list.yml'):
    nodeRedBuildOptions.insert(0, ["Select & overwrite addons list", selectNodeRedAddons])
  else:
    nodeRedBuildOptions.insert(0, ["Select & build addons list", selectNodeRedAddons])

  def runOptionsMenu():
    menuEntryPoint()
    return True

  def renderHotZone(term, menu, selection, hotzoneLocation):
    lineLengthAtTextStart = 71
    print(term.move(hotzoneLocation[0], hotzoneLocation[1]))
    for (index, menuItem) in enumerate(menu):
      toPrint = ""
      if index == selection:
        toPrint += ('{bv} -> {t.blue_on_green} {title} {t.normal} <-'.format(t=term, title=menuItem[0], bv=specialChars[renderMode]["borderVertical"]))
      else:
        toPrint += ('{bv}    {t.normal} {title}    '.format(t=term, title=menuItem[0], bv=specialChars[renderMode]["borderVertical"]))

      for i in range(lineLengthAtTextStart - len(menuItem[0])):
        toPrint += " "

      toPrint += "{bv}".format(bv=specialChars[renderMode]["borderVertical"])

      toPrint = term.center(toPrint)

      print(toPrint)

  def mainRender(needsRender, menu, selection):
    term = Terminal()
    
    if needsRender == 1:
      print(term.clear())
      print(term.move_y(term.height // 16))
      print(term.black_on_cornsilk4(term.center('IOTstack NodeRed Options')))
      print("")
      print(term.center(commonTopBorder(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Select Option to configure                                                {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center(commonEmptyLine(renderMode)))

    if needsRender >= 1:
      renderHotZone(term, menu, selection, hotzoneLocation)

    if needsRender == 1:
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Controls:                                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center("{bv}      [Enter] to run command                                                    {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center("{bv}      [Escape] to go back to build stack menu                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonBottomBorder(renderMode)))

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
