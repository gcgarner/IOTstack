#!/usr/bin/env python3

import signal

def main():
  from blessed import Terminal
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  from deps.consts import servicesDirectory, templatesDirectory, buildSettingsFileName
  import time
  import subprocess
  import ruamel.yaml
  import os

  global signal
  global currentServiceName
  global dockerCommandsSelectionInProgress
  global mainMenuList
  global currentMenuItemIndex
  global renderMode
  global paginationSize
  global paginationStartIndex
  global hardwareListFile
  global hideHelpText

  global installCommand

  yaml = ruamel.yaml.YAML()
  yaml.preserve_quotes = True

  try: # If not already set, then set it.
    hideHelpText = hideHelpText
  except:
    hideHelpText = False

  term = Terminal()
  hotzoneLocation = [((term.height // 16) + 6), 0]
  paginationToggle = [10, term.height - 25]
  paginationStartIndex = 0
  paginationSize = paginationToggle[0]

  serviceService = servicesDirectory + currentServiceName
  serviceTemplate = templatesDirectory + currentServiceName
  hardwareListFileSource = serviceTemplate + '/hardware_list.yml'
  
  def goBack():
    global dockerCommandsSelectionInProgress
    global needsRender
    dockerCommandsSelectionInProgress = False
    needsRender = 1
    return True

  mainMenuList = []

  hotzoneLocation = [((term.height // 16) + 6), 0]

  dockerCommandsSelectionInProgress = True
  currentMenuItemIndex = 0
  menuNavigateDirection = 0

  # Render Modes:
  #  0 = No render needed
  #  1 = Full render
  #  2 = Hotzone only
  needsRender = 1

  def onResize(sig, action):
    global mainMenuList
    global currentMenuItemIndex
    mainRender(1, mainMenuList, currentMenuItemIndex)

  def generateLineText(text, textLength=None, paddingBefore=0, lineLength=64):
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

  def renderHotZone(term, renderType, menu, selection, hotzoneLocation, paddingBefore = 4):
    global paginationSize
    selectedTextLength = len("-> ")

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
    print(term.center(commonEmptyLine(renderMode)))
    print(term.center(commonEmptyLine(renderMode)))


  def mainRender(needsRender, menu, selection):
    global paginationStartIndex
    global paginationSize
    term = Terminal()
    
    if selection >= paginationStartIndex + paginationSize:
      paginationStartIndex = selection - (paginationSize - 1) + 1
      needsRender = 1
      
    if selection <= paginationStartIndex - 1:
      paginationStartIndex = selection
      needsRender = 1

    if needsRender == 1:
      print(term.clear())
      print(term.move_y(term.height // 16))
      print(term.black_on_cornsilk4(term.center('IOTstack DeConz Hardware')))
      print("")
      print(term.center(commonTopBorder(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Select DeConz Hardware                                                    {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center(commonEmptyLine(renderMode)))

    if needsRender >= 1:
      renderHotZone(term, needsRender, menu, selection, hotzoneLocation)

    if needsRender == 1:
      print(term.center(commonEmptyLine(renderMode)))
      if not hideHelpText:
        if term.height < 32:
          print(term.center(commonEmptyLine(renderMode)))
          print(term.center("{bv}      Not enough vertical room to render controls help text                     {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center(commonEmptyLine(renderMode)))
        else: 
          print(term.center(commonEmptyLine(renderMode)))
          print(term.center("{bv}      Controls:                                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Space] to select or deselect hardware                                    {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [H] Show/hide this text                                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Enter] to build and save hardware list                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Escape] to cancel changes                                                {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center(commonEmptyLine(renderMode)))
          print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonBottomBorder(renderMode)))

  def runSelection(selection):
    import types
    if len(mainMenuList[selection]) > 1 and isinstance(mainMenuList[selection][1], types.FunctionType):
      mainMenuList[selection][1]()
    else:
      print(term.green_reverse('IOTstack Error: No function assigned to menu item: "{}"'.format(mainMenuList[selection][0])))

  def isMenuItemSelectable(menu, index):
    if len(menu) > index:
      if len(menu[index]) > 1:
        if "skip" in menu[index][1] and menu[index][1]["skip"] == True:
          return False
    return True

  def loadAddonsMenu():
    global mainMenuList
    if os.path.exists(hardwareListFileSource):
      with open(r'%s' % hardwareListFileSource) as objHardwareListFile:
        hardwareKnown = yaml.load(objHardwareListFile)
        knownHardwareList = hardwareKnown["hardwarePaths"]
        if os.path.exists("{serviceDir}{buildSettings}".format(serviceDir=serviceService, buildSettings=buildSettingsFileName)):
          with open("{serviceDir}{buildSettings}".format(serviceDir=serviceService, buildSettings=buildSettingsFileName)) as objSavedHardwareListFile:
            savedHardwareList = yaml.load(objSavedHardwareListFile)
            savedHardware = []

            try:
              savedHardware = savedHardwareList["hardware"]
            except:
              print("Error: Loading saved hardware selection. Please resave your selection.")
              input("Press Enter to continue...")

            for (index, hardwarePath) in enumerate(knownHardwareList):
              if hardwarePath in savedHardware:
                mainMenuList.append([hardwarePath, { "checked": True }])
              else:
                mainMenuList.append([hardwarePath, { "checked": False }])

        else: # No saved list
          for (index, hardwarePath) in enumerate(knownHardwareList):
            if os.path.exists(hardwarePath):
              mainMenuList.append([hardwarePath, { "checked": True }])
            else:
              mainMenuList.append([hardwarePath, { "checked": False }])


    else:
      print("Error: '{hardwareListFile}' file doesn't exist.".format(hardwareListFile=hardwareListFileSource))
      input("Press Enter to continue...")

  def checkMenuItem(selection):
    global mainMenuList
    if mainMenuList[selection][1]["checked"] == True:
      mainMenuList[selection][1]["checked"] = False
    else:
      mainMenuList[selection][1]["checked"] = True

  def saveAddonList():
    try:
      if not os.path.exists(serviceService):
        os.makedirs(serviceService, exist_ok=True)
      deconzYamlHardwareList = {
        "version": "1",
        "application": "IOTstack",
        "service": "deconz",
        "comment": "Build Settings",
        "hardware": []
      }
      for (index, addon) in enumerate(mainMenuList):
        if addon[1]["checked"]:
          deconzYamlHardwareList["hardware"].append(addon[0])

      with open("{serviceDir}{buildSettings}".format(serviceDir=serviceService, buildSettings=buildSettingsFileName), 'w') as outputFile:
        yaml.dump(deconzYamlHardwareList, outputFile)

    except Exception as err: 
      print("Error saving DeConz Hardware list", currentServiceName)
      print(err)
      return False
    global hasRebuiltHardwareSelection
    hasRebuiltHardwareSelection = True
    return True


  if __name__ == 'builtins':
    global signal
    term = Terminal()
    signal.signal(signal.SIGWINCH, onResize)
    loadAddonsMenu()
    with term.fullscreen():
      menuNavigateDirection = 0
      mainRender(needsRender, mainMenuList, currentMenuItemIndex)
      dockerCommandsSelectionInProgress = True
      with term.cbreak():
        while dockerCommandsSelectionInProgress:
          menuNavigateDirection = 0

          if not needsRender == 0: # Only rerender when changed to prevent flickering
            mainRender(needsRender, mainMenuList, currentMenuItemIndex)
            needsRender = 0

          key = term.inkey(esc_delay=0.05)
          if key.is_sequence:
            if key.name == 'KEY_TAB':
              if paginationSize == paginationToggle[0]:
                paginationSize = paginationToggle[1]
              else:
                paginationSize = paginationToggle[0]
              mainRender(1, mainMenuList, currentMenuItemIndex)
            if key.name == 'KEY_DOWN':
              menuNavigateDirection += 1
            if key.name == 'KEY_UP':
              menuNavigateDirection -= 1
            if key.name == 'KEY_ENTER':
              if saveAddonList():
                return True
              else:
                print("Something went wrong. Try saving the list again.")
            if key.name == 'KEY_ESCAPE':
              dockerCommandsSelectionInProgress = False
              return True
          elif key:
            if key == ' ': # Space pressed
              checkMenuItem(currentMenuItemIndex) # Update checked list
              needsRender = 2
            elif key == 'h': # H pressed
              if hideHelpText:
                hideHelpText = False
              else:
                hideHelpText = True
              mainRender(1, mainMenuList, currentMenuItemIndex)

          if menuNavigateDirection != 0: # If a direction was pressed, find next selectable item
            currentMenuItemIndex += menuNavigateDirection
            currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
            needsRender = 2

            while not isMenuItemSelectable(mainMenuList, currentMenuItemIndex):
              currentMenuItemIndex += menuNavigateDirection
              currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
    return True

  return True

originalSignalHandler = signal.getsignal(signal.SIGINT)
main()
signal.signal(signal.SIGWINCH, originalSignalHandler)
