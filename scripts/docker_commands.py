#!/usr/bin/env python3
import signal

def main():
  from blessed import Terminal
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  import math
  import time
  import subprocess

  global dockerCommandsSelectionInProgress
  global renderMode
  global signal
  global mainMenuList
  global currentMenuItemIndex
  global hideHelpText

  try: # If not already set, then set it.
    hideHelpText = hideHelpText
  except:
    hideHelpText = False

  term = Terminal()
  hotzoneLocation = [7, 0] # Top text
  
  def onResize(sig, action):
    global mainMenuList
    global currentMenuItemIndex
    mainRender(1, mainMenuList, currentMenuItemIndex)

  def startStack():
    print("Start Stack:")
    print("docker-compose up -d --remove-orphans")
    subprocess.call("docker-compose up -d", shell=True)
    print("")
    print("Stack Started")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True
  
  def restartStack():
    print("Restarting Stack...")
    print("Stop Stack:")
    print("docker-compose down")
    subprocess.call("docker-compose down", shell=True)
    print("")
    print("Start Stack:")
    print("docker-compose up -d --remove-orphans")
    subprocess.call("docker-compose up -d", shell=True)
    # print("docker-compose restart")
    # subprocess.call("docker-compose restart", shell=True)
    print("")
    print("Stack Restarted")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def stopStack():
    print("Stop Stack:")
    print("docker-compose down")
    subprocess.call("docker-compose down", shell=True)
    print("")
    print("Stack Stopped")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def stopAllStack():
    print("Stop All Stack:")
    print("docker container stop $(docker container ls -aq)")
    subprocess.call("docker container stop $(docker container ls -aq)", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def pruneVolumes():
    print("Stop All Stack:")
    print("docker container stop $(docker container ls -aq)")
    subprocess.call("docker container stop $(docker container ls -aq)", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def updateAllContainers():
    print("Update All Containers:")
    print("docker-compose pull")
    subprocess.call("docker-compose pull", shell=True)
    print("")
    print("docker-compose build --no-cache --pull")
    subprocess.call("docker-compose build --no-cache --pull", shell=True)
    print("")
    print("docker-compose up -d")
    subprocess.call("docker-compose up -d", shell=True)
    print("")
    print("docker system prune -f")
    subprocess.call("docker system prune -f", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def deleteAndPruneVolumes():
    print("Delete and prune volumes:")
    print("docker system prune --volumes")
    subprocess.call("docker system prune --volumes", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def deleteAndPruneImages():
    print("Delete and prune volumes:")
    print("docker image prune -a")
    subprocess.call("docker image prune -a", shell=True)
    print("")
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def monitorLogs():
    print("Monitor Logs:")
    print("Press CTRL+X or CTRL+C to exit.")
    time.sleep(2)
    print("")
    print("docker-compose logs -f")
    time.sleep(0.5)
    subprocess.call("docker-compose logs -f", shell=True)
    print("")
    time.sleep(0.5)
    input("Process terminated. Press [Enter] to show menu and continue.")
    needsRender = 1
    return True

  def goBack():
    global dockerCommandsSelectionInProgress
    global needsRender
    dockerCommandsSelectionInProgress = False
    needsRender = 1
    return True

  mainMenuList = [
    ["Start stack", startStack],
    ["Restart stack", restartStack],
    ["Stop stack", stopStack],
    ["Monitor Logs", monitorLogs],
    ["Stop ALL running docker containers", stopAllStack],
    ["Update all containers (may take a long time)", updateAllContainers],
    ["Delete all stopped containers and docker volumes (prune volumes)", deleteAndPruneVolumes],
    ["Delete all images not associated with container", deleteAndPruneImages],
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

      print(term.clear())
      print(term.move_y(6 - hotzoneLocation[0]))
      print(term.black_on_cornsilk4(term.center('IOTstack Docker Commands')))
      print("")
      print(term.center(commonTopBorder(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Select Docker Command to run                                              {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
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
    import types
    if len(mainMenuList[selection]) > 1 and isinstance(mainMenuList[selection][1], types.FunctionType):
      mainMenuList[selection][1]()
      mainRender(1, mainMenuList, currentMenuItemIndex)
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
    signal.signal(signal.SIGWINCH, onResize)
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
              menuNavigateDirection += 1
            if key.name == 'KEY_DOWN':
              menuNavigateDirection += 1
            if key.name == 'KEY_UP':
              menuNavigateDirection -= 1
            if key.name == 'KEY_ENTER':
              mainRender(1, mainMenuList, currentMenuItemIndex)
              runSelection(currentMenuItemIndex)
              if dockerCommandsSelectionInProgress == False:
                return True
            if key.name == 'KEY_ESCAPE':
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
    return True

  return True

originalSignalHandler = signal.getsignal(signal.SIGINT)
main()
signal.signal(signal.SIGWINCH, originalSignalHandler)