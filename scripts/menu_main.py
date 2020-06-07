#!/usr/bin/env python3

from blessed import Terminal
import sys
import subprocess
import os
import time
import types
from deps.version_check import checkVersion

term = Terminal()

# Settings/Consts
requiredDockerVersion = "18.2.0"

# Vars
selectionInProgress = True
currentMenuItemIndex = 0
menuNavigateDirection = 0
projectStatusPollRateRefresh = 1
needsRender = True
promptFiles = False
buildComplete = None

# Menu Functions
def exitMenu():
  print("Exiting IOTstack menu.")
  sys.exit(0)

def updateProject():
  print("Update Project")
  sys.exit(0)

def buildStack():
  global buildComplete
  global needsRender
  buildComplete = None
  buildstackFilePath = "./scripts/buildstack_menu.py"
  with open(buildstackFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), buildstackFilePath, "exec")
  # execGlobals = globals()
  # execLocals = locals()
  execGlobals = {}
  execLocals = {}
  exec(code, execGlobals, execLocals)
  buildComplete = execGlobals["results"]["buildState"]
  needsRender = True

def runExampleMenu():
  exampleMenuFilePath = "./.templates/example_template/example_build.py"
  with open(exampleMenuFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), exampleMenuFilePath, "exec")
  # execGlobals = globals()
  execGlobals = {}
  execLocals = locals()
  execGlobals["currentServiceName"] = 'SERVICENAME'
  execGlobals["toRun"] = 'runOptionsMenu'
  exec(code, execGlobals, execLocals)

def dockerCommands():
  global needsRender
  dockerCommandsFilePath = "./scripts/docker_commands.py"
  with open(dockerCommandsFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), dockerCommandsFilePath, "exec")
  # execGlobals = globals()
  # execLocals = locals()
  execGlobals = {}
  execLocals = {}
  exec(code, execGlobals, execLocals)
  needsRender = True

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

def installDocker(): # TODO: Fix shell issues
  print("Install Docker: curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker $USER")
  installDockerProcess = subprocess.Popen(['sudo', 'bash', './install_docker.sh', 'install'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  installDockerProcess.wait()
  installDockerResult, stdError = installDockerProcess.communicate()
  installDockerResult = installDockerResult.decode("utf-8").rstrip()

  return installDockerResult

def upgradeDocker(): # TODO: Fix shell issues
  print("Upgrade Docker: sudo apt upgrade docker docker-compose")
  upgradeDockerProcess = subprocess.Popen(['sudo', 'bash', './install_docker.sh', 'upgrade'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  upgradeDockerProcess.wait()
  upgradeDockerResult, stdError = upgradeDockerProcess.communicate()
  upgradeDockerResult = upgradeDockerResult.decode("utf-8").rstrip()

  return upgradeDockerResult

baseMenu = [
  ["Build Stack", buildStack],
  ["Docker Commands", dockerCommands],
  # ["Backup and Restore"],
  # ["Miscellaneous Commands"],
  # ["Native Installs"],
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
  getDockerVersion = subprocess.Popen(['docker', 'version', '-f', '"{{.Server.Version}}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  getDockerVersion.wait()
  currentDockerVersion, stdError = getDockerVersion.communicate()
  currentDockerVersion = currentDockerVersion.decode("utf-8").rstrip().replace('"', '')

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
    needsRender = True
  else:
    removeMenuItemByLabel("deletePromptFiles")

  if (projectStatus.poll() == None):
    addPotentialMenuItem("updatesCheck", False)
    needsRender = True
  else:
    removeMenuItemByLabel("updatesCheck")

  if (projectStatus.poll() == 1):
    added = addPotentialMenuItem("projectUpdate")
    projectStatusPollRateRefresh = None
    if (added):
      needsRender = True

  if (projectStatus.poll() == 0):
    added = addPotentialMenuItem("noProjectUpdate")
    projectStatusPollRateRefresh = None
    if (added):
      needsRender = True

  if (dockerVersion == False):
    added = addPotentialMenuItem("dockerNotUpdated")
    if (added):
      needsRender = True

def checkIfPromptFilesExist():
  if os.path.exists(".project_outofdate"):
    return True
  if os.path.exists(".docker_outofdate"):
    return True
  if os.path.exists(".docker_notinstalled"):
    return True
  return False

def mainRender(menu, selection):
  term = Terminal()
  print(term.clear())
  print(term.move_y(term.height // 16))
  print(term.black_on_cornsilk4(term.center('IOTstack Main Menu')))
  print("")

  if (buildComplete):
    print("")
    print(term.center('{t.blue_on_green} {text} {t.normal}{t.white_on_black}{cPath} {t.normal}'.format(t=term, text="Build completed:", cPath=" ./docker-compose.yml")))
    print("")

  for (index, menuItem) in enumerate(menu):
    if index == selection:
      print(term.center('{t.white_on_gold4}{title}{t.normal}'.format(t=term, title=menuItem[0])))
    else:
      print(term.center('{title}'.format(t=term, title=menuItem[0])))

def runSelection(selection):
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

# Entrypoint
if __name__ == '__main__':
  projectStatus = checkProjectUpdates() # Async
  dockerVersion, reason, data = checkDockerVersion()
  promptFiles = checkIfPromptFilesExist()
  term = Terminal()
  with term.fullscreen():
    mainRender(mainMenuList, currentMenuItemIndex) # Initial Draw
    with term.cbreak():
      while selectionInProgress:
        menuNavigateDirection = 0
        if (promptFiles):
          promptFiles = checkIfPromptFilesExist()
        doPotentialMenuCheck(projectStatus=projectStatus, dockerVersion=dockerVersion, promptFiles=promptFiles)
        
        if needsRender: # Only rerender when changed to prevent flickering
          mainRender(mainMenuList, currentMenuItemIndex)
          needsRender = False

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
        elif key:
          print("got {0}.".format(key))
        
        if menuNavigateDirection != 0: # If a direction was pressed, find next selectable item
          currentMenuItemIndex += menuNavigateDirection
          currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
          needsRender = True

          while not isMenuItemSelectable(mainMenuList, currentMenuItemIndex):
            currentMenuItemIndex += menuNavigateDirection
            currentMenuItemIndex = currentMenuItemIndex % len(mainMenuList)
