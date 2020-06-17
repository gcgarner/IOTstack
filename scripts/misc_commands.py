#!/usr/bin/env python3

def main():
  from blessed import Terminal
  import time
  import subprocess

  global dockerCommandsSelectionInProgress
  
  def setSwapinessTo0():
    print("Set swapiness to 0:")
    subprocess.call(".scripts/disable_swap.sh disableswap", shell=True)
    print("")
    time.sleep(1)
    return True
  
  def uninstallSwapfile():
    print("Uninstall Swapfile:")
    subprocess.call(".scripts/disable_swap.sh uninstallswap", shell=True)
    print("")
    time.sleep(1)
    return True

  def installLog2Ram():
    print("Install log2ram:")
    subprocess.call("bash disable_swap.sh", shell=True)
    print("")
    time.sleep(1)
    return True

  def goBack():
    global dockerCommandsSelectionInProgress
    global needsRender
    dockerCommandsSelectionInProgress = False
    needsRender = True
    print("Back to main menu")
    return True

  mainMenuList = [
    ["Uninstall Swapfile (Disables swap)", uninstallSwapfile],
    ["Set swapiness to 0 (Also disables swap)", setSwapinessTo0],
    ["Install log2ram", installLog2Ram],
    ["Back", goBack]
  ]

  dockerCommandsSelectionInProgress = True
  currentMenuItemIndex = 0
  menuNavigateDirection = 0
  needsRender = True

  def mainRender(menu, selection):
    term = Terminal()
    print(term.clear())

    print(term.clear())
    print(term.move_y(term.height // 16))
    print(term.black_on_cornsilk4(term.center('IOTstack Miscellaneous Commands')))
    print("")
    print(term.center("╔════════════════════════════════════════════════════════════════════════════════╗"))
    print(term.center("║                                                                                ║"))
    print(term.center("║      Select Command to run                                                     ║"))
    print(term.center("║                                                                                ║"))

    lineLengthAtTextStart = 75

    for (index, menuItem) in enumerate(menu):
      toPrint = ""
      if index == selection:
        toPrint += ('║   {t.blue_on_green} {title} {t.normal}'.format(t=term, title=menuItem[0]))
      else:
        toPrint += ('║   {t.normal} {title} '.format(t=term, title=menuItem[0]))

      for i in range(lineLengthAtTextStart - len(menuItem[0])):
        toPrint += " "

      toPrint += "║"

      toPrint = term.center(toPrint)
      
      print(toPrint)

    print(term.center("║                                                                                ║"))
    print(term.center("║                                                                                ║"))
    print(term.center("║      Controls:                                                                 ║"))
    print(term.center("║      [Up] and [Down] to move selection cursor                                  ║"))
    print(term.center("║      [Enter] to run command                                                    ║"))
    print(term.center("║      [Escape] to go back to main menu                                          ║"))
    print(term.center("║                                                                                ║"))
    print(term.center("║                                                                                ║"))
    print(term.center("╚════════════════════════════════════════════════════════════════════════════════╝"))



  def runSelection(selection):
    import types
    if len(mainMenuList[selection]) > 1 and isinstance(mainMenuList[selection][1], types.FunctionType):
      mainMenuList[selection][1]()
    else:
      print(term.green_reverse('IOTstack Error: No function assigned to menu item: "{}"'.format(mainMenuList[selection][0])))

  def isMenuItemSelectable(menu, index):
    if len(menu) > index:
      if len(menu[index]) > 2:
        if menu[index][2]["skip"] == True:
          return False
    return True

  if __name__ == 'builtins':
    term = Terminal()
    with term.fullscreen():
      menuNavigateDirection = 0
      mainRender(mainMenuList, currentMenuItemIndex)
      dockerCommandsSelectionInProgress = True
      with term.cbreak():
        while dockerCommandsSelectionInProgress:
          menuNavigateDirection = 0

          if needsRender: # Only rerender when changed to prevent flickering
            mainRender(mainMenuList, currentMenuItemIndex)
            needsRender = False

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
              if dockerCommandsSelectionInProgress == False:
                return True
            if key.name == 'KEY_ESCAPE':
              dockerCommandsSelectionInProgress = False
              return True
          elif key:
            print("got {0}.".format(key))

          if menuNavigateDirection != 0: # If a direction was pressed, find next selectable item
            currentMenuItemIndex += menuNavigateDirection
            currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
            needsRender = True

            while not isMenuItemSelectable(mainMenuList, currentMenuItemIndex):
              currentMenuItemIndex += menuNavigateDirection
              currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
    return True

  return True

main()