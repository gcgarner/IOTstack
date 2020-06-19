#!/usr/bin/env python3
import signal

def main():
  from blessed import Terminal
  import time
  import subprocess

  global signal
  global dockerCommandsSelectionInProgress
  global mainMenuList
  global currentMenuItemIndex
  term = Terminal()
  hotzoneLocation = [((term.height // 16) + 6), 0]
  
  def onResize(sig, action):
    global mainMenuList
    global currentMenuItemIndex
    mainRender(1, mainMenuList, currentMenuItemIndex)

  def installHassIo():
    print("Install Hass.IO")
    print("./.native/hassio.sh")
    subprocess.call("./.native/hassio.sh", shell=True)
    print("")
    print("Preinstallation complete. Your system may run slow for a few hours as Hass.io installs its services.")
    print("Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(0.5)
    return True

  def installRtl433():
    print("Install RTL_433")
    print("./.native/rtl_433.sh")
    subprocess.call("./.native/rtl_433.sh", shell=True)
    print("")
    print("Installation complete. Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(0.5)
    return True

  def installRpiEasy():
    print("Install RPIEasy")
    print("./.native/rpieasy.sh")
    subprocess.call("./.native/rpieasy.sh", shell=True)
    print("")
    print("Installation complete. Press [Up] or [Down] arrow key to show the menu if it has scrolled too far.")
    time.sleep(0.5)
    return True

  def goBack():
    global dockerCommandsSelectionInProgress
    global needsRender
    dockerCommandsSelectionInProgress = False
    needsRender = 1
    print("Back to main menu")
    return True

  mainMenuList = [
    ["Hass.io", installHassIo],
    ["RTL_433", installRtl433],
    ["RPIEasy", installRpiEasy],
    ["Back", goBack]
  ]

  dockerCommandsSelectionInProgress = True
  currentMenuItemIndex = 0
  menuNavigateDirection = 0

  # Render Modes:
  #  0 = No render needed
  #  1 = Full render
  #  2 = Hotzone only
  needsRender = 1

  def renderHotZone(term, menu, selection, hotzoneLocation):
    print(term.move(hotzoneLocation[0], hotzoneLocation[1]))
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

  def mainRender(menu, selection):
    term = Terminal()

    if needsRender == 1:
      print(term.clear())
      print(term.move_y(term.height // 16))
      print(term.black_on_cornsilk4(term.center('Native Installs')))
      print("")
      print(term.center("╔════════════════════════════════════════════════════════════════════════════════╗"))
      print(term.center("║                                                                                ║"))
      print(term.center("║      Select service to install                                                 ║"))
      print(term.center("║                                                                                ║"))

    if needsRender >= 1:
      renderHotZone(term, menu, selection, hotzoneLocation)

    if needsRender == 1:
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

          if not needsRender == 0: # Only rerender when changed to prevent flickering
            mainRender(mainMenuList, currentMenuItemIndex)
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
            needsRender = 2

            while not isMenuItemSelectable(mainMenuList, currentMenuItemIndex):
              currentMenuItemIndex += menuNavigateDirection
              currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
    return True

  return True


originalSignalHandler = signal.getsignal(signal.SIGINT)
main()
signal.signal(signal.SIGWINCH, originalSignalHandler)
