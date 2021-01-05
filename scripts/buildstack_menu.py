#!/usr/bin/env python3
import signal

checkedMenuItems = []
results = {}

def main():
  import os
  import time
  import ruamel.yaml
  import math
  import sys
  import subprocess
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine, padText
  from deps.consts import servicesDirectory, templatesDirectory, volumesDirectory, buildCache, envFile, dockerPathOutput, servicesFileName, composeOverrideFile
  from deps.yaml_merge import mergeYaml
  from blessed import Terminal
  global signal
  global renderMode
  global term
  global paginationSize
  global paginationStartIndex
  global hideHelpText
  global activeMenuLocation
  global lastSelection

  yaml = ruamel.yaml.YAML()
  yaml.preserve_quotes = True

  # Constants
  buildScriptFile = 'build.py'
  dockerSavePathOutput = buildCache

  # Runtime vars
  menu = []
  dockerComposeServicesYaml = {}
  templatesDirectoryFolders = next(os.walk(templatesDirectory))[1]
  term = Terminal()
  hotzoneLocation = [7, 0] # Top text
  paginationToggle = [10, term.height - 22] # Top text + controls text
  paginationStartIndex = 0
  paginationSize = paginationToggle[0]
  activeMenuLocation = 0
  lastSelection = 0
  
  try: # If not already set, then set it.
    hideHelpText = hideHelpText
  except:
    hideHelpText = False

  def buildServices(): # TODO: Move this into a dependency so that it can be executed with just a list of services.
    global dockerComposeServicesYaml
    try:
      runPrebuildHook()
      dockerFileYaml = {}
      menuStateFileYaml = {}
      dockerFileYaml["version"] = "3.6"
      dockerFileYaml["services"] = {}
      menuStateFileYaml["services"] = {}
      dockerFileYaml["services"] = dockerComposeServicesYaml
      menuStateFileYaml["services"] = dockerComposeServicesYaml

      if os.path.exists(envFile):
        with open(r'%s' % envFile) as fileEnv:
          envSettings = yaml.load(fileEnv)
        mergedYaml = mergeYaml(envSettings, dockerFileYaml)
        dockerFileYaml = mergedYaml

      if os.path.exists(composeOverrideFile):
        with open(r'%s' % composeOverrideFile) as fileOverride:
          yamlOverride = yaml.load(fileOverride)

        mergedYaml = mergeYaml(yamlOverride, dockerFileYaml)
        dockerFileYaml = mergedYaml

      with open(r'%s' % dockerPathOutput, 'w') as outputFile:
        yaml.dump(dockerFileYaml, outputFile)

      if not os.path.exists(servicesDirectory):
        os.makedirs(servicesDirectory, exist_ok=True)

      with open(r'%s' % dockerSavePathOutput, 'w') as outputFile:
        yaml.dump(menuStateFileYaml, outputFile)
      runPostBuildHook()

      if os.path.exists('./postbuild.sh'):
        servicesList = ""
        for (index, serviceName) in enumerate(dockerComposeServicesYaml):
          servicesList += " " + serviceName
        subprocess.call("./postbuild.sh" + servicesList, shell=True)

      return True
    except Exception as err: 
      print("Issue running build:")
      print(err)
      input("Press Enter to continue...")
      return False

  def generateTemplateList(templatesDirectoryFolders):
    templatesDirectoryFolders.sort()
    templateListDirectories = []
    for directory in templatesDirectoryFolders:
      serviceFilePath = templatesDirectory + '/' + directory + '/' + servicesFileName
      if os.path.exists(serviceFilePath):
        templateListDirectories.append(directory)

    return templateListDirectories

  def generateLineText(text, textLength=None, paddingBefore=0, lineLength=26):
    result = ""
    for i in range(paddingBefore):
      result += " "

    textPrintableCharactersLength = textLength

    if (textPrintableCharactersLength) == None:
      textPrintableCharactersLength = len(text)

    result += text
    remainingSpace = lineLength - textPrintableCharactersLength

    for i in range(remainingSpace):
      result += " "
    
    return result

  def renderHotZone(term, renderType, menu, selection, paddingBefore, allIssues):
    global paginationSize
    optionsLength = len(" >>   Options ")
    optionsIssuesSpace = len("      ")
    selectedTextLength = len("-> ")
    spaceAfterissues = len("      ")
    issuesLength = len(" !!   Issue ")

    print(term.move(hotzoneLocation[0], hotzoneLocation[1]))

    if paginationStartIndex >= 1:
      print(term.center("{b}       {uaf}      {uaf}{uaf}{uaf}                                                   {ual}           {b}".format(
        b=specialChars[renderMode]["borderVertical"],
        uaf=specialChars[renderMode]["upArrowFull"],
        ual=specialChars[renderMode]["upArrowLine"]
      )))
    else:
      print(term.center(commonEmptyLine(renderMode)))

    menuItemsActiveRow = term.get_location()[0]
    if renderType == 2 or renderType == 1: # Rerender entire hotzone
      for (index, menuItem) in enumerate(menu): # Menu loop
        if "issues" in menuItem[1] and menuItem[1]["issues"]:
          allIssues.append({ "serviceName": menuItem[0], "issues": menuItem[1]["issues"] })

        if index >= paginationStartIndex and index < paginationStartIndex + paginationSize:
          lineText = generateLineText(menuItem[0], paddingBefore=paddingBefore)

          # Menu highlight logic
          if index == selection:
            activeMenuLocation = term.get_location()[0]
            formattedLineText = '-> {t.blue_on_green}{title}{t.normal} <-'.format(t=term, title=menuItem[0])
            paddedLineText = generateLineText(formattedLineText, textLength=len(menuItem[0]) + selectedTextLength, paddingBefore=paddingBefore - selectedTextLength)
            toPrint = paddedLineText
          else:
            toPrint = '{title}{t.normal}'.format(t=term, title=lineText)
          # #####

          # Options and issues
          if "buildHooks" in menuItem[1] and "options" in menuItem[1]["buildHooks"] and menuItem[1]["buildHooks"]["options"]:
            toPrint = toPrint + '{t.blue_on_black} {raf}{raf} {t.normal}'.format(t=term, raf=specialChars[renderMode]["rightArrowFull"])
            toPrint = toPrint + ' {t.white_on_black} Options {t.normal}'.format(t=term)
          else:
            for i in range(optionsLength):
              toPrint += " "

          for i in range(optionsIssuesSpace):
            toPrint += " "

          if "issues" in menuItem[1] and menuItem[1]["issues"]:
            toPrint = toPrint + '{t.red_on_orange} !! {t.normal}'.format(t=term)
            toPrint = toPrint + ' {t.orange_on_black} Issue {t.normal}'.format(t=term)
          else:
            if menuItem[1]["checked"]:
              if not menuItem[1]["issues"] == None and len(menuItem[1]["issues"]) == 0:
                toPrint = toPrint + '     {t.green_on_blue} Pass {t.normal} '.format(t=term)
              else:
                for i in range(issuesLength):
                  toPrint += " "
            else:
              for i in range(issuesLength):
                toPrint += " "

          for i in range(spaceAfterissues):
            toPrint += " "
          # #####

          # Menu check render logic
          if menuItem[1]["checked"]:
            toPrint = "     (X) " + toPrint
          else:
            toPrint = "     ( ) " + toPrint

          toPrint = "{bv} {toPrint}  {bv}".format(bv=specialChars[renderMode]["borderVertical"], toPrint=toPrint) # Generate border
          toPrint = term.center(toPrint) # Center Text (All lines should have the same amount of printable characters)
          # #####
          print(toPrint)


    if renderType == 3: # Only partial rerender of hotzone (the unselected menu item, and the newly selected menu item rows)
      global lastSelection
      global renderOffsetLastSelection
      global renderOffsetCurrentSelection
      # TODO: Finish this, currently disabled. To enable, update the actions for UP and DOWN array keys below to assigned 3 to needsRender
      renderOffsetLastSelection = lastSelection - paginationStartIndex
      renderOffsetCurrentSelection = selection - paginationStartIndex
      lineText = generateLineText(menu[lastSelection][0], paddingBefore=paddingBefore)
      toPrint = '{title}{t.normal}'.format(t=term, title=lineText)
      print('{t.move_y(lastSelection)}{title}'.format(t=term, title=toPrint))
      # print(toPrint)
      print(renderOffsetCurrentSelection, lastSelection, renderOffsetLastSelection)
      lastSelection = selection
      
          # menuItemsActiveRow
          # activeMenuLocation


    if paginationStartIndex + paginationSize < len(menu):
      print(term.center("{b}       {daf}      {daf}{daf}{daf}                                                   {dal}           {b}".format(
        b=specialChars[renderMode]["borderVertical"],
        daf=specialChars[renderMode]["downArrowFull"],
        dal=specialChars[renderMode]["downArrowLine"]
      )))
    else:
      print(term.center(commonEmptyLine(renderMode)))

  def mainRender(menu, selection, renderType = 1):
    global paginationStartIndex
    global paginationSize
    paddingBefore = 4

    allIssues = []

    if selection >= paginationStartIndex + paginationSize:
      paginationStartIndex = selection - (paginationSize - 1) + 1
      renderType = 1
      
    if selection <= paginationStartIndex - 1:
      paginationStartIndex = selection
      renderType = 1

    try:
      if (renderType == 1):
        checkForOptions()
        print(term.clear())
        print(term.move_y(7 - hotzoneLocation[0]))
        print(term.black_on_cornsilk4(term.center('IOTstack Build Menu')))
        print("")
        print(term.center(commonTopBorder(renderMode)))

        print(term.center(commonEmptyLine(renderMode)))
        print(term.center("{bv}      Select containers to build                                                {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center(commonEmptyLine(renderMode)))
        print(term.center(commonEmptyLine(renderMode)))
        print(term.center(commonEmptyLine(renderMode)))

      renderHotZone(term, renderType, menu, selection, paddingBefore, allIssues)

      if (renderType == 1):
        print(term.center(commonEmptyLine(renderMode)))
        if not hideHelpText:
          room = term.height - (28 + len(allIssues) + paginationSize)
          if room < 0:
            allIssues.append({ "serviceName": "BuildStack Menu", "issues": { "screenSize": 'Not enough scren height to render correctly (t-height = ' + str(term.height) + ' v-lines = ' + str(room) + ')' } })
            print(term.center(commonEmptyLine(renderMode)))
            print(term.center("{bv}      Not enough vertical room to render controls help text ({th}, {rm})          {bv}".format(bv=specialChars[renderMode]["borderVertical"], th=padText(str(term.height), 3), rm=padText(str(room), 3))))
            print(term.center(commonEmptyLine(renderMode)))
          else: 
            print(term.center(commonEmptyLine(renderMode)))
            print(term.center("{bv}      Controls:                                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}      [Space] to select or deselect image                                       {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}      [Right] for options for containers that support them                      {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}      [Tab] Expand or collapse build menu size                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}      [H] Show/hide this text                                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            # print(term.center("{bv}      [F] Filter options                                                        {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}      [Enter] to begin build                                                    {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center("{bv}      [Escape] to cancel build                                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
            print(term.center(commonEmptyLine(renderMode)))
            print(term.center(commonEmptyLine(renderMode)))
        print(term.center(commonEmptyLine(renderMode)))
        print(term.center(commonBottomBorder(renderMode)))

        if len(allIssues) > 0:
          print(term.center(""))
          print(term.center(""))
          print(term.center(""))
          print(term.center(("{btl}{bh}{bh}{bh}{bh}{bh}{bh} Build Issues "
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}{bh}"
            "{bh}{bh}{bh}{bh}{bh}{bh}{bh}{btr}").format(
            btl=specialChars[renderMode]["borderTopLeft"],
            btr=specialChars[renderMode]["borderTopRight"],
            bh=specialChars[renderMode]["borderHorizontal"]
          )))
          print(term.center(commonEmptyLine(renderMode, size = 139)))
          for serviceIssues in allIssues:
            for index, issue in enumerate(serviceIssues["issues"]):
              spacesAndBracketsLen = 5
              issueAndTypeLen = len(issue) + len(serviceIssues["serviceName"]) + spacesAndBracketsLen
              serviceNameAndConflictType = '{t.red_on_black}{issueService}{t.normal} ({t.yellow_on_black}{issueType}{t.normal}) '.format(t=term, issueService=serviceIssues["serviceName"], issueType=issue)
              formattedServiceNameAndConflictType = generateLineText(str(serviceNameAndConflictType), textLength=issueAndTypeLen, paddingBefore=0, lineLength=32)
              issueDescription = generateLineText(str(serviceIssues["issues"][issue]), textLength=len(str(serviceIssues["issues"][issue])), paddingBefore=0, lineLength=103)
              print(term.center("{bv} {nm} - {desc} {bv}".format(nm=formattedServiceNameAndConflictType, desc=issueDescription, bv=specialChars[renderMode]["borderVertical"]) ))
          print(term.center(commonEmptyLine(renderMode, size = 139)))
          print(term.center(commonBottomBorder(renderMode, size = 139)))

    except Exception as err: 
      print("There was an error rendering the menu:")
      print(err)
      print("Press [Esc] to go back")
      return

    return

  def setCheckedMenuItems():
    global checkedMenuItems
    checkedMenuItems.clear()
    for (index, menuItem) in enumerate(menu):
      if menuItem[1]["checked"]:
        checkedMenuItems.append(menuItem[0])

  def loadAllServices(reload = False):
    global dockerComposeServicesYaml
    dockerComposeServicesYaml.clear()
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      if reload == False:
        if not checkedMenuItem in dockerComposeServicesYaml:
          serviceFilePath = templatesDirectory + '/' + checkedMenuItem + '/' + servicesFileName
          with open(r'%s' % serviceFilePath) as yamlServiceFile:
            dockerComposeServicesYaml[checkedMenuItem] = yaml.load(yamlServiceFile)[checkedMenuItem]
      else:
        print("reload!")
        time.sleep(1)
        serviceFilePath = templatesDirectory + '/' + checkedMenuItem + '/' + servicesFileName
        with open(r'%s' % serviceFilePath) as yamlServiceFile:
          dockerComposeServicesYaml[checkedMenuItem] = yaml.load(yamlServiceFile)[checkedMenuItem]

    return True

  def loadService(serviceName, reload = False):
    try:
      global dockerComposeServicesYaml
      if reload == False:
        if not serviceName in dockerComposeServicesYaml:
          serviceFilePath = templatesDirectory + '/' + serviceName + '/' + servicesFileName
          with open(r'%s' % serviceFilePath) as yamlServiceFile:
            dockerComposeServicesYaml[serviceName] = yaml.load(yamlServiceFile)[serviceName]
      else:
        print("reload!")
        time.sleep(1)
        servicesFileNamePath = templatesDirectory + '/' + serviceName + '/' + servicesFileName
        with open(r'%s' % serviceFilePath) as yamlServiceFile:
          dockerComposeServicesYaml[serviceName] = yaml.load(yamlServiceFile)[serviceName]
    except Exception as err:
      print("Error running build menu:", err)
      print("Check the following:")
      print("* YAML service name matches the folder name")
      print("* Error in YAML file")
      print("* YAML file is unreadable")
      print("* Buildstack script was modified")
      input("Press Enter to exit...")
      sys.exit(1)

    return True

  def checkForIssues():
    global dockerComposeServicesYaml
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      buildScriptPath = templatesDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
        try:
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeServicesYaml": dockerComposeServicesYaml,
            "toRun": "checkForRunChecksHook",
            "currentServiceName": checkedMenuItem
          }
          execLocals = locals()
          exec(code, execGlobals, execLocals)
          if "buildHooks" in execGlobals and "runChecksHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["runChecksHook"]:
            execGlobals = {
              "dockerComposeServicesYaml": dockerComposeServicesYaml,
              "toRun": "runChecks",
              "currentServiceName": checkedMenuItem
            }
            execLocals = locals()
            try:
              exec(code, execGlobals, execLocals)
              if "issues" in execGlobals and len(execGlobals["issues"]) > 0:
                menu[getMenuItemIndexByService(checkedMenuItem)][1]["issues"] = execGlobals["issues"]
              else:
                menu[getMenuItemIndexByService(checkedMenuItem)][1]["issues"] = []
            except Exception as err:
              print("Error running checkForIssues on '%s'" % checkedMenuItem)
              print(err)
              input("Press Enter to continue...")
          else:
            menu[getMenuItemIndexByService(checkedMenuItem)][1]["issues"] = []
        except Exception as err:
          print("Error running checkForIssues on '%s'" % checkedMenuItem)
          print(err)
          input("Press any key to exit...")
          sys.exit(1)

  def checkForOptions():
    global dockerComposeServicesYaml
    for (index, menuItem) in enumerate(menu):
      buildScriptPath = templatesDirectory + '/' + menuItem[0] + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
        try:
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeServicesYaml": dockerComposeServicesYaml,
            "toRun": "checkForOptionsHook",
            "currentServiceName": menuItem[0],
            "renderMode": renderMode
          }
          execLocals = {}
          exec(code, execGlobals, execLocals)
          if not "buildHooks" in menu[getMenuItemIndexByService(menuItem[0])][1]:
            menu[getMenuItemIndexByService(menuItem[0])][1]["buildHooks"] = {}
          if "options" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["options"]:
            menu[getMenuItemIndexByService(menuItem[0])][1]["buildHooks"]["options"] = True
        except Exception as err:
          print("Error running checkForOptions on '%s'" % menuItem[0])
          print(err)
          input("Press any key to exit...")
          sys.exit(1)

  def runPrebuildHook():
    global dockerComposeServicesYaml
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      buildScriptPath = templatesDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeServicesYaml": dockerComposeServicesYaml,
            "toRun": "checkForPreBuildHook",
            "currentServiceName": checkedMenuItem
          }
          execLocals = locals()
          try:
            exec(code, execGlobals, execLocals)
            if "preBuildHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["preBuildHook"]:
              execGlobals = {
                "dockerComposeServicesYaml": dockerComposeServicesYaml,
                "toRun": "preBuild",
                "currentServiceName": checkedMenuItem
              }
              execLocals = locals()
              exec(code, execGlobals, execLocals)
          except Exception as err:
            print("Error running PreBuildHook on '%s'" % checkedMenuItem)
            print(err)
            input("Press Enter to continue...")
            try: # If the prebuild hook modified the docker-compose object, pull it from the script back to here.
              dockerComposeServicesYaml = execGlobals["dockerComposeServicesYaml"]
            except:
              pass

  def runPostBuildHook():
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      buildScriptPath = templatesDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeServicesYaml": dockerComposeServicesYaml,
            "toRun": "checkForPostBuildHook",
            "currentServiceName": checkedMenuItem
          }
          execLocals = locals()
          try:
            exec(code, execGlobals, execLocals)
            if "postBuildHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["postBuildHook"]:
              execGlobals = {
                "dockerComposeServicesYaml": dockerComposeServicesYaml,
                "toRun": "postBuild",
                "currentServiceName": checkedMenuItem
              }
              execLocals = locals()
              exec(code, execGlobals, execLocals)
          except Exception as err:
            print("Error running PostBuildHook on '%s'" % checkedMenuItem)
            print(err)
            input("Press Enter to continue...")

  def executeServiceOptions():
    global dockerComposeServicesYaml
    menuItem = menu[selection]
    if menu[selection][1]["checked"] and "buildHooks" in menuItem[1] and "options" in menuItem[1]["buildHooks"] and menuItem[1]["buildHooks"]["options"]:
      buildScriptPath = templatesDirectory + '/' + menuItem[0] + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
        with open(buildScriptPath, "rb") as pythonDynamicImportFile:
          code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")

        execGlobals = {
          "dockerComposeServicesYaml": dockerComposeServicesYaml,
          "toRun": "runOptionsMenu",
          "currentServiceName": menuItem[0],
          "renderMode": renderMode
        }
        execLocals = locals()
        exec(code, execGlobals, execLocals)
        dockerComposeServicesYaml = execGlobals["dockerComposeServicesYaml"]
        checkForIssues()
        mainRender(menu, selection, 1)

  def getMenuItemIndexByService(serviceName):
    for (index, menuItem) in enumerate(menu):
      if (menuItem[0] == serviceName):
        return index

  def checkMenuItem(selection):
    global dockerComposeServicesYaml
    if menu[selection][1]["checked"] == True:
      menu[selection][1]["checked"] = False
      menu[selection][1]["issues"] = None
      del dockerComposeServicesYaml[menu[selection][0]]
    else:
      menu[selection][1]["checked"] = True
      print(menu[selection][0])
      loadService(menu[selection][0])

  def prepareMenuState():
    global dockerComposeServicesYaml
    for (index, serviceName) in enumerate(dockerComposeServicesYaml):
      checkMenuItem(getMenuItemIndexByService(serviceName))
      setCheckedMenuItems()
      checkForIssues()

    return True

  def loadCurrentConfigs(templatesList):
    global dockerComposeServicesYaml
    if os.path.exists(dockerSavePathOutput):
      print("Loading config fom: '%s'" % dockerSavePathOutput)
      with open(r'%s' % dockerSavePathOutput) as fileSavedConfigs:
        previousConfigs = yaml.load(fileSavedConfigs)
        if not previousConfigs == None:
          if "services" in previousConfigs:
            dockerComposeServicesYaml = {}
            for (index, serviceName) in enumerate(previousConfigs["services"]):
              if serviceName in templatesList: # This ensures every service loaded has a template directory
                dockerComposeServicesYaml[serviceName] = previousConfigs["services"][serviceName]
            return True
    dockerComposeServicesYaml = {}
    return False

  def onResize(sig, action):
    global paginationToggle
    paginationToggle = [10, term.height - 25]
    mainRender(menu, selection, 1)

  templatesList = generateTemplateList(templatesDirectoryFolders)
  for directory in templatesList:
    menu.append([directory, { "checked": False, "issues": None }])

  if __name__ == 'builtins':
    global results
    global signal
    needsRender = 1
    signal.signal(signal.SIGWINCH, onResize)
    with term.fullscreen():
      print('Loading...')
      selection = 0
      if loadCurrentConfigs(templatesList):
        prepareMenuState()
      mainRender(menu, selection, 1)
      selectionInProgress = True
      with term.cbreak():
        while selectionInProgress:
          key = term.inkey(esc_delay=0.05)
          if key.is_sequence:
            if key.name == 'KEY_TAB':
              needsRender = 1
              if paginationSize == paginationToggle[0]:
                paginationSize = paginationToggle[1]
                paginationStartIndex = 0
              else:
                paginationSize = paginationToggle[0]
            if key.name == 'KEY_DOWN':
              selection += 1
              needsRender = 2
            if key.name == 'KEY_UP':
              selection -= 1
              needsRender = 2
            if key.name == 'KEY_RIGHT':
              executeServiceOptions()
            if key.name == 'KEY_ENTER':
              setCheckedMenuItems()
              checkForIssues()
              selectionInProgress = False
              results["buildState"] = buildServices()
              return results["buildState"]
            if key.name == 'KEY_ESCAPE':
              results["buildState"] = False
              return results["buildState"]
          elif key:
            if key == ' ': # Space pressed
              checkMenuItem(selection) # Update checked list
              setCheckedMenuItems() # Update UI memory
              checkForIssues()
              needsRender = 1
            elif key == 'h': # H pressed
              if hideHelpText:
                hideHelpText = False
              else:
                hideHelpText = True
              needsRender = 1
          else:
            print(key)
            time.sleep(0.5)

          selection = selection % len(menu)

          mainRender(menu, selection, needsRender)

originalSignalHandler = signal.getsignal(signal.SIGINT)
main()
signal.signal(signal.SIGWINCH, originalSignalHandler)
