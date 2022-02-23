#!/usr/bin/env python3
import signal

def main():
  from blessed import Terminal
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  global renderMode
  import time
  import subprocess

  global signal
  global dockerCommandsSelectionInProgress
  global mainMenuList
  global currentMenuItemIndex
  global screenActive
  global hideHelpText
  global needsRender

  try: # If not already set, then set it.
    hideHelpText = hideHelpText
  except:
    hideHelpText = False

  term = Terminal()
  hotzoneLocation = [7, 0] # Top text
  
  def onResize(sig, action):
    global mainMenuList
    global currentMenuItemIndex
    if (screenActive):
      mainRender(1, mainMenuList, currentMenuItemIndex)

  def installRtl433():
    print(term.clear())
    print("Install RTL_433")
    print("bash ./.native/rtl_433.sh")
    subprocess.call("bash ./.native/rtl_433.sh", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    return True

  def installRpiEasy():
    print(term.clear())
    print("Install RPIEasy")
    print("bash ./.native/rpieasy.sh")
    subprocess.call("bash ./.native/rpieasy.sh", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    return True

  def installDockerAndCompose():
    print(term.clear())
    print("Install docker")
    print("Install docker-compose")
    print("bash ./scripts/install_docker.sh install")
    subprocess.call("bash ./scripts/install_docker.sh install", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    return True

  def upgradeDockerAndCompose():
    print(term.clear())
    print("Install docker")
    print("Install docker-compose")
    print("bash ./scripts/install_docker.sh upgrade")
    subprocess.call("bash ./scripts/install_docker.sh upgrade", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    return True

  def goBack():
    global dockerCommandsSelectionInProgress
    global needsRender
    global screenActive
    screenActive = False
    dockerCommandsSelectionInProgress = False
    needsRender = 1
    return True

  mainMenuList = [
    ["RTL_433", installRtl433],
    ["RPIEasy", installRpiEasy],
    ["Upgrade Docker and Docker-Compose", upgradeDockerAndCompose],
    ["Install Docker and Docker-Compose", installDockerAndCompose],
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
    lineLengthAtTextStart = 71

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
      print(term.move_y(6 - hotzoneLocation[0]))
      print(term.black_on_cornsilk4(term.center('Native Installs')))
      print("")
      print(term.center(commonTopBorder(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Select service to install                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))

    if needsRender >= 1:
      renderHotZone(term, menu, selection, hotzoneLocation)

    if needsRender == 1:
      print(term.center(commonEmptyLine(renderMode)))
      if not hideHelpText:
        if term.height < 30:
          print(term.center(commonEmptyLine(renderMode)))
          print(term.center("{bv}      Not enough vertical room to render controls help text                     {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center(commonEmptyLine(renderMode)))
        else: 
          print(term.center(commonEmptyLine(renderMode)))
          print(term.center("{bv}      Controls:                                                                 {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [H] Show/hide this text                                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Enter] to run command                                                    {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Escape] to go back to main menu                                          {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center(commonBottomBorder(renderMode)))




  def runSelection(selection):
    global needsRender
    import types
    if len(mainMenuList[selection]) > 1 and isinstance(mainMenuList[selection][1], types.FunctionType):
      mainMenuList[selection][1]()
      needsRender = 1
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
      global screenActive
      screenActive = True
      signal.signal(signal.SIGWINCH, onResize)
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
              menuNavigateDirection += 1
            if key.name == 'KEY_DOWN':
              menuNavigateDirection += 1
            if key.name == 'KEY_UP':
              menuNavigateDirection -= 1
            if key.name == 'KEY_ENTER':
              runSelection(currentMenuItemIndex)
              if dockerCommandsSelectionInProgress == False:
                screenActive = False
                return True
              mainRender(1, mainMenuList, currentMenuItemIndex)
            if key.name == 'KEY_ESCAPE':
              screenActive = False
              dockerCommandsSelectionInProgress = False
              return True
          elif key:
            if key == 'h': # H pressed
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
    screenActive = False
    return True

  screenActive = False
  return True

main()

