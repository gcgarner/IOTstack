#!/usr/bin/python3
from blessed import Terminal
import sys
import subprocess
import os
import time
import types
import signal
from deps.chars import specialChars
from deps.version_check import checkVersion

term = Terminal()

# Settings/Consts
requiredDockerVersion = "18.2.0"

# Vars
selectionInProgress = True
currentMenuItemIndex = 0
menuNavigateDirection = 0
projectStatusPollRateRefresh = 1
promptFiles = False
buildComplete = None
hotzoneLocation = [((term.height // 16) + 6), 0]
screenActive = True

  # Render Modes:
  #  0 = No render needed
  #  1 = Full render
  #  2 = Hotzone only
needsRender = 1

def checkRenderOptions():
  global term
  global renderMode
  if len(sys.argv) > 1 and (sys.argv[1] == "simple" or sys.argv[1] == "latin" or sys.argv[1] == "ascii"):
    renderMode = sys.argv[1]
  else:
    print(term.clear())
    try:
      print(
        specialChars["latin"]["rightArrowFull"],
        specialChars["latin"]["upArrowFull"],
        specialChars["latin"]["upArrowLine"],
        specialChars["latin"]["downArrowFull"],
        specialChars["latin"]["downArrowLine"],
        specialChars["latin"]["borderVertical"],
        specialChars["latin"]["borderHorizontal"],
        specialChars["latin"]["borderTopLeft"],
        specialChars["latin"]["borderTopRight"],
        specialChars["latin"]["borderBottomLeft"],
        specialChars["latin"]["borderBottomRight"],
      )
      print(term.clear())
      renderMode = "latin"
      return "latin"
    except:
      try:
        print(
          specialChars["simple"]["rightArrowFull"],
          specialChars["simple"]["upArrowFull"],
          specialChars["simple"]["upArrowLine"],
          specialChars["simple"]["downArrowFull"],
          specialChars["simple"]["downArrowLine"],
          specialChars["simple"]["borderVertical"],
          specialChars["simple"]["borderHorizontal"],
          specialChars["simple"]["borderTopLeft"],
          specialChars["simple"]["borderTopRight"],
          specialChars["simple"]["borderBottomLeft"],
          specialChars["simple"]["borderBottomRight"],
        )
        print(term.clear())
        renderMode = "simple"
        return "simple"
      except:
        print(term.clear())
        renderMode = "ascii"
        return "ascii"


def onResize(sig, action):
  global needsRender
  global mainMenuList
  global currentMenuItemIndex
  global screenActive
  if screenActive:
    mainRender(1, mainMenuList, currentMenuItemIndex)

# Menu Functions
def exitMenu():
  print("Exiting IOTstack menu.")
  print(term.clear())
  sys.exit(0)

def buildStack():
  global buildComplete
  global needsRender
  global screenActive
  
  buildComplete = None
  buildstackFilePath = "./scripts/buildstack_menu.py"
  with open(buildstackFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), buildstackFilePath, "exec")
  execGlobals = {
    "renderMode": renderMode
  }
  execLocals = {}
  screenActive = False
  print(term.clear())
  exec(code, execGlobals, execLocals)
  buildComplete = execGlobals["results"]["buildState"]
  signal.signal(signal.SIGWINCH, onResize)
  screenActive = True
  needsRender = 1

def runExampleMenu():
  exampleMenuFilePath = "./.templates/example_template/example_build.py"
  with open(exampleMenuFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), exampleMenuFilePath, "exec")
  # execGlobals = globals()
  execGlobals = {
    "renderMode": renderMode
  }
  execLocals = locals()
  execGlobals["currentServiceName"] = 'SERVICENAME'
  execGlobals["toRun"] = 'runOptionsMenu'
  screenActive = False
  exec(code, execGlobals, execLocals)
  signal.signal(signal.SIGWINCH, onResize)
  screenActive = True

def dockerCommands():
  global needsRender
  dockerCommandsFilePath = "./scripts/docker_commands.py"
  with open(dockerCommandsFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), dockerCommandsFilePath, "exec")
  # execGlobals = globals()
  # execLocals = locals()
  execGlobals = {
    "renderMode": renderMode
  }
  execLocals = {}
  screenActive = False
  exec(code, execGlobals, execLocals)
  signal.signal(signal.SIGWINCH, onResize)
  screenActive = True
  needsRender = 1

def miscCommands():
  global needsRender
  dockerCommandsFilePath = "./scripts/misc_commands.py"
  with open(dockerCommandsFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), dockerCommandsFilePath, "exec")
  # execGlobals = globals()
  # execLocals = locals()
  execGlobals = {
    "renderMode": renderMode
  }
  execLocals = {}
  screenActive = False
  exec(code, execGlobals, execLocals)
  signal.signal(signal.SIGWINCH, onResize)
  screenActive = True
  needsRender = 1

def nativeInstalls():
  global needsRender
  global screenActive
  dockerCommandsFilePath = "./scripts/native_installs.py"
  with open(dockerCommandsFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), dockerCommandsFilePath, "exec")
  # currGlobals = globals()
  # currLocals = locals()
  execGlobals = {
    "renderMode": renderMode
  }
  execLocals = {}
  screenActive = False
  exec(code, execGlobals, execLocals)
  signal.signal(signal.SIGWINCH, onResize)
  screenActive = True
  needsRender = 1

def backupAndRestore():
  global needsRender
  global screenActive
  dockerCommandsFilePath = "./scripts/backup_restore.py"
  with open(dockerCommandsFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), dockerCommandsFilePath, "exec")
  # currGlobals = globals()
  # currLocals = locals()
  execGlobals = {
    "renderMode": renderMode
  }
  execLocals = {}
  screenActive = False
  exec(code, execGlobals, execLocals)
  signal.signal(signal.SIGWINCH, onResize)
  screenActive = True
  needsRender = 1

def doNothing():
  selectionInProgress = True

def skipItem(currentMenuItemIndex, direction):
  currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
  if len(mainMenuList[currentMenuItemIndex]) > 2 and mainMenuList[currentMenuItemIndex][2]["skip"] == True:
    currentMenuItemIndex += lastSelectionDirection
  return currentMenuItemIndex

def deletePromptFiles():
  # global promptFiles
  # global currentMenuItemIndex
  if os.path.exists(".project_outofdate"):
    os.remove(".project_outofdate")
  if os.path.exists(".docker_outofdate"):
    os.remove(".docker_outofdate")
  if os.path.exists(".docker_notinstalled"):
    os.remove(".docker_notinstalled")
  promptFiles = False
  currentMenuItemIndex = 0

def installDocker():
  print("Install Docker: curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker $USER")
  installDockerProcess = subprocess.Popen(['sudo', 'bash', './install_docker.sh', 'install'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  installDockerProcess.wait()
  installDockerResult, stdError = installDockerProcess.communicate()
  installDockerResult = installDockerResult.decode("utf-8").rstrip()

  return installDockerResult

def upgradeDocker():
  print("Upgrade Docker: sudo apt upgrade docker docker-compose")
  upgradeDockerProcess = subprocess.Popen(['sudo', 'bash', './install_docker.sh', 'upgrade'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  upgradeDockerProcess.wait()
  upgradeDockerResult, stdError = upgradeDockerProcess.communicate()
  upgradeDockerResult = upgradeDockerResult.decode("utf-8").rstrip()

  return upgradeDockerResult

baseMenu = [
  ["Build Stack", buildStack],
  ["Docker Commands", dockerCommands],
  ["Miscellaneous Commands", miscCommands],
  ["Backup and Restore", backupAndRestore],
  ["Native Installs", nativeInstalls],
  # ["Developer: Example Menu", runExampleMenu], # Uncomment if you want to see the example menu
  ["Exit", exitMenu]
]

# Main Menu
mainMenuList = baseMenu

potentialMenu = {
  "projectUpdate": {
    "menuItem": ["Update IOTstack", installDocker],
    "added": False
  },
  "dockerUpdate": { # TODO: Do note use, fix shell issues first
    "menuItem": ["Update Docker", upgradeDocker],
    "added": False
  },
  "dockerNotUpdated": { # TODO: Do note use, fix shell issues first
    "menuItem": [term.red_on_black("Docker is not up to date"), doNothing, { "skip": True }],
    "added": False
  },
  "dockerTerminals": { # TODO: Do note use, not finished
    "menuItem": ["Docker Terminals", doNothing],
    "added": False
  },
  "noProjectUpdate": {
    "menuItem": [term.green_on_black("IOTstack is up to date"), doNothing, { "skip": True }],
    "added": False
  },
  "spacer": {
    "menuItem": ["------", doNothing, { "skip": True }],
    "added": False
  },
  "newLine": {
    "menuItem": [" ", doNothing, { "skip": True }],
    "added": False
  },
  "deletePromptFiles": {
    "menuItem": ["Delete 'out of date' prompt files", deletePromptFiles],
    "added": False
  },
  "updatesCheck": {
    "menuItem": [term.blue_on_black("Checking for updates..."), doNothing, { "skip": True }],
    "added": False
  }
}

def checkDockerVersion():
  try:
    getDockerVersion = subprocess.Popen(['docker', 'version', '-f', '"{{.Server.Version}}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    getDockerVersion.wait()
    currentDockerVersion, stdError = getDockerVersion.communicate()
    currentDockerVersion = currentDockerVersion.decode("utf-8").rstrip().replace('"', '')
  except Exception as err:
    print("Error attempting to run docker command:", err)
    currentDockerVersion = ""

  return checkVersion(requiredDockerVersion, currentDockerVersion)

def checkProjectUpdates():
  getCurrentBranch = subprocess.Popen(["git", "name-rev", "--name-only", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  getCurrentBranch.wait()
  currentBranch, stdError = getCurrentBranch.communicate()
  currentBranch = currentBranch.decode("utf-8").rstrip()
  projectStatus = subprocess.Popen(["git", "fetch", "origin", currentBranch], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  return projectStatus

def addPotentialMenuItem(menuItemName, hasSpacer=True):
  if (potentialMenu["newLine"]["added"] == False):
    potentialMenu["newLine"]["added"] = True
    baseMenu.append(potentialMenu["newLine"]["menuItem"])
  if hasSpacer and potentialMenu["spacer"]["added"] == False:
    potentialMenu["spacer"]["added"] = True
    baseMenu.append(potentialMenu["spacer"]["menuItem"])

  if (potentialMenu[menuItemName]["added"] == False):
    potentialMenu[menuItemName]["added"] = True
    baseMenu.append(potentialMenu[menuItemName]["menuItem"])
    return True

  return False

def removeMenuItemByLabel(potentialItemKey):
  i = -1
  for menuItem in mainMenuList:
    i += 1
    if menuItem[0] == potentialMenu[potentialItemKey]["menuItem"][0]:
      potentialMenu[potentialItemKey]["added"] = False
      mainMenuList.pop(i)

def doPotentialMenuCheck(projectStatus, dockerVersion=True, promptFiles=False):
  global needsRender

  if (promptFiles == True):
    addPotentialMenuItem("deletePromptFiles")
    needsRender = 2
  else:
    removeMenuItemByLabel("deletePromptFiles")

  # if (projectStatus.poll() == None):
  #   addPotentialMenuItem("updatesCheck", False)
  #   needsRender = 2
  # else:
  #   removeMenuItemByLabel("updatesCheck")

  # if (projectStatus.poll() == 1):
  #   added = addPotentialMenuItem("projectUpdate")
  #   projectStatusPollRateRefresh = None
  #   if (added):
  #     needsRender = 1

  # if (projectStatus.poll() == 0):
  #   added = addPotentialMenuItem("noProjectUpdate")
  #   projectStatusPollRateRefresh = None
  #   if (added):
  #     needsRender = 1

  if (dockerVersion == False):
    added = addPotentialMenuItem("dockerNotUpdated")
    if (added):
      needsRender = 1

def checkIfPromptFilesExist():
  if os.path.exists(".project_outofdate"):
    return True
  if os.path.exists(".docker_outofdate"):
    return True
  if os.path.exists(".docker_notinstalled"):
    return True
  return False

def renderHotZone(term, menu, selection):
  print(term.move(hotzoneLocation[0], hotzoneLocation[1]))
  for (index, menuItem) in enumerate(menu):
    if index == selection:
      print(term.center('-> {t.blue_on_green}{title}{t.normal} <-'.format(t=term, title=menuItem[0])))
    else:
      print(term.center('{title}'.format(t=term, title=menuItem[0])))

def mainRender(needsRender, menu, selection):
  term = Terminal()
  if needsRender == 1:
    print(term.clear())
    print(term.move_y(term.height // 16))
    print(term.black_on_cornsilk4(term.center('IOTstack Main Menu')))
    print("")

  if needsRender >= 1:
    renderHotZone(term, menu, selection)

  if (buildComplete and needsRender == 1):
    print("")
    print("")
    print("")
    print(term.center('{t.blue_on_green} {text} {t.normal}{t.white_on_black}{cPath} {t.normal}'.format(t=term, text="Build completed:", cPath=" ./docker-compose.yml")))
    print(term.center('{t.white_on_black}{text}{t.blue_on_green2} {commandString} {t.normal}'.format(t=term, text="You can start the stack from the Docker Commands menu, or from the CLI with: ", commandString="docker-compose up -d")))
    if os.path.exists('./compose-override.yml'):
      print("")
      print(term.center('{t.grey_on_blue4} {text} {t.normal}{t.white_on_black}{t.normal}'.format(t=term, text="'compose-override.yml' was merged into 'docker-compose.yml'")))
    print("")

def runSelection(selection):
  global needsRender
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

# Entrypoint
if __name__ == '__main__':
  projectStatus = checkProjectUpdates() # Async
  dockerVersion, reason, data = checkDockerVersion()
  promptFiles = checkIfPromptFilesExist()
  term = Terminal()
  
  signal.signal(signal.SIGWINCH, onResize)

  with term.fullscreen():
    checkRenderOptions()
    mainRender(needsRender, mainMenuList, currentMenuItemIndex) # Initial Draw
    with term.cbreak():
      while selectionInProgress:
        menuNavigateDirection = 0
        if (promptFiles):
          promptFiles = checkIfPromptFilesExist()

        if needsRender > 0: # Only rerender when changed to prevent flickering
          mainRender(needsRender, mainMenuList, currentMenuItemIndex)
          needsRender = 0

        doPotentialMenuCheck(projectStatus=projectStatus, dockerVersion=dockerVersion, promptFiles=promptFiles)
        
        key = term.inkey(timeout=projectStatusPollRateRefresh)
        if key.is_sequence:
          if key.name == 'KEY_TAB':
            menuNavigateDirection = 1
          if key.name == 'KEY_DOWN':
            menuNavigateDirection = 1
          if key.name == 'KEY_UP':
            menuNavigateDirection = -1
          if key.name == 'KEY_ENTER':
            runSelection(currentMenuItemIndex)
          if key.name == 'KEY_ESCAPE':
            exitMenu()
        
        if not menuNavigateDirection == 0: # If a direction was pressed, find next selectable item
          currentMenuItemIndex += menuNavigateDirection
          currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
          needsRender = 2

          while not isMenuItemSelectable(mainMenuList, currentMenuItemIndex):
            currentMenuItemIndex += menuNavigateDirection
            currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
