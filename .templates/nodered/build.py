#!/usr/bin/env python3

issues = {} # Returned issues dict
buildHooks = {} # Options, and others hooks
haltOnErrors = True

# Main wrapper function. Required to make local vars work correctly
def main():
  import os
  import time
  import ruamel.yaml
  import signal
  import sys
  from blessed import Terminal
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine, padText
  from deps.consts import servicesDirectory, templatesDirectory
  from deps.common_functions import getExternalPorts, getInternalPorts, checkPortConflicts, enterPortNumberWithWhiptail

  global dockerComposeServicesYaml # The loaded memory YAML of all checked services
  global renderMode # For rendering fancy or basic ascii characters
  global toRun # Switch for which function to run when executed
  global buildHooks # Where to place the options menu result
  global currentServiceName # Name of the current service
  global issues # Returned issues dict
  global haltOnErrors # Turn on to allow erroring
  global serviceService
  global serviceTemplate
  global addonsFile
  global hideHelpText
  global hasRebuiltAddons

  try: # If not already set, then set it.
    hideHelpText = hideHelpText
  except:
    hideHelpText = False

  documentationHint = 'https://sensorsiot.github.io/IOTstack/Containers/Node-RED'

  yaml = ruamel.yaml.YAML()
  yaml.preserve_quotes = True

  # runtime vars
  portConflicts = []
  hasRebuiltAddons = False

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

    # Other prebuild steps
    print("Starting NodeRed Build script")
    time.sleep(0.1)
    with open(r'%s/Dockerfile.template' % serviceTemplate, 'r') as dockerTemplate:
      templateData = dockerTemplate.read()

    with open(r'%s' % addonsFile) as objAddonsFile:
      addonsSelected = yaml.load(objAddonsFile)

    addonsInstallCommands = ""
    if os.path.exists(addonsFile):
      installCommand = addonsSelected["dockerFileInstallCommand"]
      for (index, addonName) in enumerate(addonsSelected["addons"]):
        if (addonName == 'node-red-node-sqlite'): # SQLite requires a special param
          addonsInstallCommands = addonsInstallCommands + "{installCommand} --unsafe-perm {addonName}\n".format(addonName=addonName, installCommand=installCommand)
        else:
          addonsInstallCommands = addonsInstallCommands + "{installCommand} {addonName}\n".format(addonName=addonName, installCommand=installCommand)

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
    for (index, serviceName) in enumerate(dockerComposeServicesYaml):
      if not currentServiceName == serviceName: # Skip self
        currentServicePorts = getExternalPorts(currentServiceName, dockerComposeServicesYaml)
        portConflicts = checkPortConflicts(serviceName, currentServicePorts, dockerComposeServicesYaml)
        if (len(portConflicts) > 0):
          issues["portConflicts"] = portConflicts

  def checkFiles():
    fileIssues = []
    if not os.path.exists(serviceService + '/addons_list.yml'):
      fileIssues.append('/addons_list.yml does not exist. Build addons file in options to fix. This is optional')
    return fileIssues

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
    return True

  def enterPortNumberExec():
    # global term
    global needsRender
    global dockerComposeServicesYaml
    externalPort = getExternalPorts(currentServiceName, dockerComposeServicesYaml)[0]
    internalPort = getInternalPorts(currentServiceName, dockerComposeServicesYaml)[0]
    newPortNumber = enterPortNumberWithWhiptail(term, dockerComposeServicesYaml, currentServiceName, hotzoneLocation, externalPort)

    if newPortNumber > 0:
      dockerComposeServicesYaml[currentServiceName]["ports"][0] = "{newExtPort}:{oldIntPort}".format(
        newExtPort = newPortNumber,
        oldIntPort = internalPort
      )
      createMenu()
    needsRender = 1

  def onResize(sig, action):
    global nodeRedBuildOptions
    global currentMenuItemIndex
    mainRender(1, nodeRedBuildOptions, currentMenuItemIndex)

  def selectNodeRedAddons():
    global needsRender
    global hasRebuiltAddons
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
    try:
      hasRebuiltAddons = execGlobals["hasRebuiltAddons"]
    except:
      hasRebuiltAddons = False
    screenActive = True
    needsRender = 1

  nodeRedBuildOptions = []

  def createMenu():
    global nodeRedBuildOptions
    try:
      nodeRedBuildOptions = []
      portNumber = getExternalPorts(currentServiceName, dockerComposeServicesYaml)[0]
      nodeRedBuildOptions.append([
        "Change external WUI Port Number from: {port}".format(port=portNumber),
        enterPortNumberExec
      ])
    except: # Error getting port
      pass
    nodeRedBuildOptions.append(["Go back", goBack])

    if os.path.exists(serviceService + '/addons_list.yml'):
      nodeRedBuildOptions.insert(0, ["Select & overwrite addons list", selectNodeRedAddons])
    else:
      nodeRedBuildOptions.insert(0, ["Select & build addons list", selectNodeRedAddons])

  def runOptionsMenu():
    createMenu()
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
      if os.path.exists(serviceService + '/addons_list.yml'):
        if hasRebuiltAddons:
          print(term.center(commonEmptyLine(renderMode)))
          print(term.center('{bv}     {t.grey_on_blue4} {text} {t.normal}{t.white_on_black}{t.normal}                            {bv}'.format(t=term, text="Addons list has been rebuilt: addons_list.yml", bv=specialChars[renderMode]["borderVertical"])))
        else:
          print(term.center(commonEmptyLine(renderMode)))
          print(term.center('{bv}     {t.grey_on_blue4} {text} {t.normal}{t.white_on_black}{t.normal}                   {bv}'.format(t=term, text="Using existing addons_list.yml for addons installation", bv=specialChars[renderMode]["borderVertical"])))
      else:
        print(term.center(commonEmptyLine(renderMode)))
        print(term.center(commonEmptyLine(renderMode)))
      if not hideHelpText:
        print(term.center(commonEmptyLine(renderMode)))
        print(term.center("{bv}      Controls:                                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [H] Show/hide this text                                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [Enter] to run command or save input                                      {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [Escape] to go back to build stack menu                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center(commonEmptyLine(renderMode)))
        if len(documentationHint) > 1:
          if len(documentationHint) > 56:
            documentationAndPadding = padText(documentationHint, 71)
            print(term.center("{bv}      Documentation:                                                            {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}        {dap} {bv}".format(bv=specialChars[renderMode]["borderVertical"], dap=documentationAndPadding)))
          else:
            documentationAndPadding = padText(documentationHint, 56)
            print(term.center("{bv}        Documentation: {dap} {bv}".format(bv=specialChars[renderMode]["borderVertical"], dap=documentationAndPadding)))
          print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonBottomBorder(renderMode)))

  def runSelection(selection):
    import types
    global nodeRedBuildOptions
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
    global hideHelpText
    global nodeRedBuildOptions
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

          key = term.inkey(esc_delay=0.05)
          if key.is_sequence:
            if key.name == 'KEY_TAB':
              menuNavigateDirection += 1
            if key.name == 'KEY_DOWN':
              menuNavigateDirection += 1
            if key.name == 'KEY_UP':
              menuNavigateDirection -= 1
            if key.name == 'KEY_LEFT':
              goBack()
            if key.name == 'KEY_ENTER':
              runSelection(currentMenuItemIndex)
            if key.name == 'KEY_ESCAPE':
              return True
          elif key:
            if key == 'h': # H pressed
              if hideHelpText:
                hideHelpText = False
              else:
                hideHelpText = True
              mainRender(1, nodeRedBuildOptions, currentMenuItemIndex)

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
