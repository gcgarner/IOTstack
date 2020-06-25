#!/usr/bin/env python3

import signal

def main():
  from blessed import Terminal
  import time
  import subprocess
  import yaml
  import os

  global signal
  global dockerCommandsSelectionInProgress
  global mainMenuList
  global currentMenuItemIndex
  global paginationSize
  global paginationStartIndex
  global addonsFile
  term = Terminal()
  hotzoneLocation = [((term.height // 16) + 6), 0]
  paginationToggle = [10, term.height - 25]
  paginationStartIndex = 0
  paginationSize = paginationToggle[0]

  addonsFile = "./.templates/nodered/addons.yml"
  
  def goBack():
    global dockerCommandsSelectionInProgress
    global needsRender
    dockerCommandsSelectionInProgress = False
    needsRender = 1
    print("Back to main menu")
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

    print(term.move(hotzoneLocation[0], hotzoneLocation[1]))

    if paginationStartIndex >= 1:
      # print(term.center("|       ▲      ▲▲▲                                                   ↑           |"))
      print(term.center("|       ^      ^^^                                                   ^           |"))
    else:
      print(term.center("|                                                                                |"))

    for (index, menuItem) in enumerate(menu): # Menu loop
      if index >= paginationStartIndex and index < paginationStartIndex + paginationSize:
        lineText = generateLineText(menuItem[0], paddingBefore=paddingBefore)

        # Menu highlight logic
        if index == selection:
          formattedLineText = '{t.blue_on_green}{title}{t.normal}'.format(t=term, title=menuItem[0])
          paddedLineText = generateLineText(formattedLineText, textLength=len(menuItem[0]), paddingBefore=paddingBefore)
          toPrint = paddedLineText
        else:
          toPrint = '{title}{t.normal}'.format(t=term, title=lineText)
        # #####

        # Menu check render logic
        if menuItem[1]["checked"]:
          toPrint = "     (X) " + toPrint
        else:
          toPrint = "     ( ) " + toPrint

        toPrint = "| " + toPrint + "  |" # Generate border
        toPrint = term.center(toPrint) # Center Text (All lines should have the same amount of printable characters)
        # #####
        print(toPrint)

    if paginationStartIndex + paginationSize < len(menu):
      # print(term.center("|       ▼      ▼▼▼                                                   ↓           |"))
      print(term.center("|       v      vvv                                                   v           |"))
    else:
      print(term.center("|                                                                                |"))
    print(term.center("|                                                                                |"))
    print(term.center("|                                                                                |"))


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
      print(term.black_on_cornsilk4(term.center('IOTstack NodeRed Addons')))
      print("")
      # print(term.center("╔════════════════════════════════════════════════════════════════════════════════╗"))
      print(term.center("/--------------------------------------------------------------------------------\\"))
      print(term.center("|                                                                                |"))
      print(term.center("|      Select NodeRed Addons (npm) to install                                    |"))
      print(term.center("|                                                                                |"))

    if needsRender >= 1:
      renderHotZone(term, needsRender, menu, selection, hotzoneLocation)

    if needsRender == 1:
      print(term.center("|                                                                                |"))
      print(term.center("|                                                                                |"))
      print(term.center("|      Controls:                                                                 |"))
      print(term.center("|      [Space] to select or deselect addon                                       |"))
      print(term.center("|      [Up] and [Down] to move selection cursor                                  |"))
      print(term.center("|      [Tab] Expand or collapse addon menu size                                  |"))
      print(term.center("|      [S] Switch between sorted by checked and sorted alphabetically            |"))
      print(term.center("|      [Enter] to save updated list                                              |"))
      print(term.center("|      [Escape] to cancel changes                                                |"))
      print(term.center("|                                                                                |"))
      print(term.center("|                                                                                |"))
      # print(term.center("║                                                                                ║"))
      # print(term.center("╚════════════════════════════════════════════════════════════════════════════════╝"))
      print(term.center("\\--------------------------------------------------------------------------------/"))

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
    if os.path.exists(addonsFile):
      with open(r'%s' % addonsFile) as objAddonsFile:
        addonsLoaded = yaml.load(objAddonsFile, Loader=yaml.SafeLoader)
        defaultOnAddons = addonsLoaded["addons"]["default_on"]
        defaultOffAddons = addonsLoaded["addons"]["default_off"]
        defaultOnAddons.sort()
        for (index, addonName) in enumerate(defaultOnAddons):
          mainMenuList.append([addonName, { "checked": True }])

        defaultOffAddons.sort()
        for (index, addonName) in enumerate(defaultOffAddons):
          mainMenuList.append([addonName, { "checked": False }])

    else:
      print("Error: '{addonsFile}' file doesn't exist.".format(addonsFile=addonsFile))

  def checkMenuItem(selection):
    global mainMenuList
    if mainMenuList[selection][1]["checked"] == True:
      mainMenuList[selection][1]["checked"] = False
    else:
      mainMenuList[selection][1]["checked"] = True

  if __name__ == 'builtins':
    global signal
    sortBy = 0
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

          key = term.inkey()
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
              runSelection(currentMenuItemIndex)
              if dockerCommandsSelectionInProgress == False:
                return True
            if key.name == 'KEY_ESCAPE':
              dockerCommandsSelectionInProgress = False
              return True
          elif key:
            if key == ' ': # Space pressed
              checkMenuItem(currentMenuItemIndex) # Update checked list
              needsRender = 2
            if key == 's':
              if sortBy == 0:
                sortBy = 1
                mainMenuList.sort(key=lambda x: x[0], reverse=False)
              else:
                sortBy = 0
                mainMenuList.sort(key=lambda x: (x[1]["checked"], x[0]), reverse=True)
              
              needsRender = 2

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
