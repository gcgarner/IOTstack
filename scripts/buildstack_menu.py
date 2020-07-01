#!/usr/bin/env python3
import signal

checkedMenuItems = []
results = {}

def main():
  import os
  import time
  import yaml
  import math
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  from blessed import Terminal
  global signal
  global renderMode
  global term
  global paginationSize
  global paginationStartIndex

  # Constants
  templateDirectory = './.templates'
  serviceFile = 'service.yml'
  buildScriptFile = 'build.py'
  dockerPathOutput = './docker-compose.yml'
  dockerSavePathOutput = './services/docker-compose.save.yml'
  composeOverrideFile = './compose-override.yml'

  # Runtime vars
  menu = []
  dockerComposeYaml = {}
  templateDirectoryFolders = next(os.walk(templateDirectory))[1]
  term = Terminal()
  hotzoneLocation = [7, 0] # Top text
  paginationToggle = [10, term.height - 21] # Top text + controls text
  paginationStartIndex = 0
  paginationSize = paginationToggle[0]
  
  def buildServices():
    global dockerComposeYaml
    try:
      runPrebuildHook()
      dockerFileYaml = {}
      menuStateFileYaml = {}
      dockerFileYaml["version"] = "3.6"
      dockerFileYaml["services"] = {}
      menuStateFileYaml["services"] = {}
      dockerFileYaml["services"] = dockerComposeYaml
      menuStateFileYaml["services"] = dockerComposeYaml

      if os.path.exists(composeOverrideFile):
        with open(r'%s' % composeOverrideFile) as fileOverride:
          yamlOverride = yaml.load(fileOverride, Loader=yaml.SafeLoader)

        mergedYaml = mergeYaml(yamlOverride, dockerFileYaml)
        dockerFileYaml = mergedYaml

      with open(r'%s' % dockerPathOutput, 'w') as outputFile:
        yaml.dump(dockerFileYaml, outputFile, default_flow_style=False, sort_keys=False)

      with open(r'%s' % dockerSavePathOutput, 'w') as outputFile:
        yaml.dump(menuStateFileYaml, outputFile, default_flow_style=False, sort_keys=False)
      runPostbuildHook()
      return True
    except Exception as err: 
      print("Issue running build:")
      print(err)
      time.sleep(5)
      return False

  def mergeYaml(priorityYaml, defaultYaml):
    finalYaml = {}
    if isinstance(defaultYaml, dict):
      for dk, dv in defaultYaml.items():
        if dk in priorityYaml:
          finalYaml[dk] = mergeYaml(priorityYaml[dk], dv)
        else:
          finalYaml[dk] = dv
      for pk, pv in priorityYaml.items():
        if pk in finalYaml:
          finalYaml[pk] = mergeYaml(finalYaml[pk], pv)
        else:
          finalYaml[pk] = pv
    else:
      finalYaml = defaultYaml
    return finalYaml

  def generateTemplateList(templateDirectoryFolders):
    templateDirectoryFolders.sort()
    templateListDirectories = []
    for directory in templateDirectoryFolders:
      serviceFilePath = templateDirectory + '/' + directory + '/' + serviceFile
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


    for (index, menuItem) in enumerate(menu): # Menu loop
      if "issues" in menuItem[1] and menuItem[1]["issues"]:
        allIssues.append({ "serviceName": menuItem[0], "issues": menuItem[1]["issues"] })

      if index >= paginationStartIndex and index < paginationStartIndex + paginationSize:
        lineText = generateLineText(menuItem[0], paddingBefore=paddingBefore)

        # Menu highlight logic
        if index == selection:
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
    checkForOptions()

    if selection >= paginationStartIndex + paginationSize:
      paginationStartIndex = selection - (paginationSize - 1) + 1
      renderType = 1
      
    if selection <= paginationStartIndex - 1:
      paginationStartIndex = selection
      renderType = 1

    try:
      if (renderType == 1):
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
        print(term.center(commonEmptyLine(renderMode)))
        print(term.center("{bv}      Controls:                                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [Space] to select or deselect image                                       {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [Right] for options for containers that support them                      {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
        print(term.center("{bv}      [Tab] Expand or collapse build menu size                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
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

  def loadServices():
    global dockerComposeYaml
    dockerComposeYaml.clear()
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      serviceFilePath = templateDirectory + '/' + checkedMenuItem + '/' + serviceFile
      with open(r'%s' % serviceFilePath) as yamlServiceFile:
        dockerComposeYaml[checkedMenuItem] = yaml.load(yamlServiceFile, Loader=yaml.SafeLoader)[checkedMenuItem]

    return True

  def checkForIssues():
    global dockerComposeYaml
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      buildScriptPath = templateDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeYaml": dockerComposeYaml,
            "toRun": "checkForRunChecksHook",
            "currentServiceName": checkedMenuItem
          }
          execLocals = locals()
          exec(code, execGlobals, execLocals)
          if "buildHooks" in execGlobals and "runChecksHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["runChecksHook"]:
            execGlobals = {
              "dockerComposeYaml": dockerComposeYaml,
              "toRun": "runChecks",
              "currentServiceName": checkedMenuItem
            }
            execLocals = locals()
            exec(code, execGlobals, execLocals)
            if "issues" in execGlobals and len(execGlobals["issues"]) > 0:
              menu[getMenuItemIndexByService(checkedMenuItem)][1]["issues"] = execGlobals["issues"]
            else:
              menu[getMenuItemIndexByService(checkedMenuItem)][1]["issues"] = []
          else:
            menu[getMenuItemIndexByService(checkedMenuItem)][1]["issues"] = []

  def checkForOptions():
    global dockerComposeYaml
    for (index, menuItem) in enumerate(menu):
      buildScriptPath = templateDirectory + '/' + menuItem[0] + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeYaml": dockerComposeYaml,
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

  def runPrebuildHook():
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      buildScriptPath = templateDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeYaml": dockerComposeYaml,
            "toRun": "checkForPreBuildHook",
            "currentServiceName": checkedMenuItem
          }
          execLocals = locals()
          exec(code, execGlobals, execLocals)
          if "preBuildHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["preBuildHook"]:
            execGlobals = {
              "dockerComposeYaml": dockerComposeYaml,
              "toRun": "preBuild",
              "currentServiceName": checkedMenuItem
            }
            execLocals = locals()
            exec(code, execGlobals, execLocals)

  def runPostbuildHook():
    for (index, checkedMenuItem) in enumerate(checkedMenuItems):
      buildScriptPath = templateDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
      if os.path.exists(buildScriptPath):
          with open(buildScriptPath, "rb") as pythonDynamicImportFile:
            code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
          execGlobals = {
            "dockerComposeYaml": dockerComposeYaml,
            "toRun": "checkForPostBuildHook",
            "currentServiceName": checkedMenuItem
          }
          execLocals = locals()
          exec(code, execGlobals, execLocals)
          if "postBuildHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["postBuildHook"]:
            execGlobals = {
              "dockerComposeYaml": dockerComposeYaml,
              "toRun": "postBuild",
              "currentServiceName": checkedMenuItem
            }
            execLocals = locals()
            exec(code, execGlobals, execLocals)

  def executeServiceOptions():
    menuItem = menu[selection]
    if "buildHooks" in menuItem[1] and "options" in menuItem[1]["buildHooks"] and menuItem[1]["buildHooks"]["options"]:
      buildScriptPath = templateDirectory + '/' + menuItem[0] + '/' + buildScriptFile
      print(buildScriptPath)
      if os.path.exists(buildScriptPath):
        with open(buildScriptPath, "rb") as pythonDynamicImportFile:
          code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
        execGlobals = {
          "dockerComposeYaml": dockerComposeYaml,
          "toRun": "runOptionsMenu",
          "currentServiceName": menuItem[0],
          "renderMode": renderMode
        }
        execLocals = locals()
        exec(code, execGlobals, execLocals)
        checkForIssues()
        mainRender(menu, selection, 1)

  def getMenuItemIndexByService(serviceName):
    for (index, menuItem) in enumerate(menu):
      if (menuItem[0] == serviceName):
        return index

  def checkMenuItem(selection):
    if menu[selection][1]["checked"] == True:
      menu[selection][1]["checked"] = False
      menu[selection][1]["issues"] = None
    else:
      menu[selection][1]["checked"] = True

  def prepareMenuState():
    global dockerComposeYaml
    for (index, serviceName) in enumerate(dockerComposeYaml):
      checkMenuItem(getMenuItemIndexByService(serviceName))
      setCheckedMenuItems()
      checkForIssues()

    return True

  def loadCurrentConfigs():
    global dockerComposeYaml
    if os.path.exists(dockerSavePathOutput):
      with open(r'%s' % dockerSavePathOutput) as fileSavedConfigs:
        previousConfigs = yaml.load(fileSavedConfigs, Loader=yaml.SafeLoader)
        if not previousConfigs == None:
          if "services" in previousConfigs:
            dockerComposeYaml = previousConfigs["services"]
            return True
    dockerComposeYaml = {}
    return False

  def onResize(sig, action):
    global paginationToggle
    paginationToggle = [10, term.height - 25]
    mainRender(menu, selection, 1)

  templatesList = generateTemplateList(templateDirectoryFolders)
  for directory in templatesList:
    menu.append([directory, { "checked": False, "issues": None }])

  if __name__ == 'builtins':
    global results
    global signal
    signal.signal(signal.SIGWINCH, onResize)
    with term.fullscreen():
      selection = 0
      if loadCurrentConfigs():
        prepareMenuState()
      mainRender(menu, selection, 1)
      selectionInProgress = True
      with term.cbreak():
        while selectionInProgress:
          key = term.inkey()
          if key.is_sequence:
            if key.name == 'KEY_TAB':
              if paginationSize == paginationToggle[0]:
                paginationSize = paginationToggle[1]
              else:
                paginationSize = paginationToggle[0]
              mainRender(menu, selection, 1)
            if key.name == 'KEY_DOWN':
              selection += 1
            if key.name == 'KEY_UP':
              selection -= 1
            if key.name == 'KEY_RIGHT':
              executeServiceOptions()
            if key.name == 'KEY_ENTER':
              setCheckedMenuItems()
              loadServices()
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
              loadServices()
              checkForIssues()
              mainRender(menu, selection, 1)
            else:
              time.sleep(0.1)

          selection = selection % len(menu)

          mainRender(menu, selection, 2)

originalSignalHandler = signal.getsignal(signal.SIGINT)
main()
signal.signal(signal.SIGWINCH, originalSignalHandler)
