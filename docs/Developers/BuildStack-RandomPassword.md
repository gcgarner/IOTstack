# Build Stack Random Services Password

This page explains how to have a service generate a random password during build time. This will require that your service have a working options menu.

Keep in mind that updating strings in a service's yaml config isn't limited to passwords.

## A word of caution
Many services often set a password on their initial spin up and store it internally. That means if if the password is changed by the menu afterwards, it may not be reflected in the service. By default the password specified in the documentation should be used, unless the user specifically selected to use a randomly generated one. In the future, the feature to specify a password manually may be added in, much like how ports can be customised.

## A basic example
Inside the service's `service.yml` file, a special string can be added in for the build script to find and replace. Commonly the string is `%randomPassword%`, but technically any string can be used. The same string can be used multiple times for the same password to be used multiple times, and/or multiple difference strings can be used for multiple passwords.
```
  mariadb:
    image: linuxserver/mariadb
    container_name: mariadb
    environment:
      - MYSQL_ROOT_PASSWORD=%randomAdminPassword%
      - MYSQL_DATABASE=default
      - MYSQL_USER=mariadbuser
      - MYSQL_PASSWORD=%randomPassword%
```

These strings will be updated during the Prebuild Hook stage when building. The code to make this happen is shown below.

## Code commonly used to update passwords
This code can basically be copy-pasted into your service's `build.py` file. You are welcome to expand upon it if required. It will probably be refactored into a utils function in the future to adear to DRY (Don't Repeat Yourself) practices.
```
def preBuild():
  # Multi-service load. Most services only include a single service. The exception being NextCloud where the database information needs to match between NextCloud and MariaDB (as defined in NextCloud's 'service.yml' file, not IOTstack's MariaDB).
  with open((r'%s/' % serviceTemplate) + servicesFileName) as objServiceFile:
    serviceYamlTemplate = yaml.load(objServiceFile)

  oldBuildCache = {}
  try:
    with open(r'%s' % buildCache) as objBuildCache: # Load previous build, if it exists
      oldBuildCache = yaml.load(objBuildCache)
  except:
    pass

  buildCacheServices = {}
  if "services" in oldBuildCache: # If a previous build does exist, load it so that we can reuse the password from it if required.
    buildCacheServices = oldBuildCache["services"]

  if not os.path.exists(serviceService): # Create the service directory for the service
    os.makedirs(serviceService, exist_ok=True)

  # Check if buildSettings file exists (from previous build), or create one if it doesn't (in the else block).
  if os.path.exists(buildSettings):
    # Password randomisation
    with open(r'%s' % buildSettings) as objBuildSettingsFile:
      piHoleYamlBuildOptions = yaml.load(objBuildSettingsFile)
      if (
        piHoleYamlBuildOptions["databasePasswordOption"] == "Randomise database password for this build"
        or piHoleYamlBuildOptions["databasePasswordOption"] == "Randomise database password every build"
        or deconzYamlBuildOptions["databasePasswordOption"] == "Use default password for this build"
      ):
      
        if deconzYamlBuildOptions["databasePasswordOption"] == "Use default password for this build":
          newAdminPassword = "######" # Update to what's specified in your documentation
          newPassword = "######" # Update to what's specified in your documentation
        else:
          # Generate our passwords
          newAdminPassword = generateRandomString()
          newPassword = generateRandomString()
        
        # Here we loop through each service included in the current service's `service.yml` file and update the password strings.
        for (index, serviceName) in enumerate(serviceYamlTemplate):
          dockerComposeServicesYaml[serviceName] = serviceYamlTemplate[serviceName]
          if "environment" in serviceYamlTemplate[serviceName]:
            for (envIndex, envName) in enumerate(serviceYamlTemplate[serviceName]["environment"]):
              envName = envName.replace("%randomPassword%", newPassword)
              envName = envName.replace("%randomAdminPassword%", newAdminPassword)
              dockerComposeServicesYaml[serviceName]["environment"][envIndex] = envName

        # If the user had selected to only update the password once, ensure the build options file is updated.
        if (piHoleYamlBuildOptions["databasePasswordOption"] == "Randomise database password for this build"):
          piHoleYamlBuildOptions["databasePasswordOption"] = "Do nothing"
          with open(buildSettings, 'w') as outputFile:
            yaml.dump(piHoleYamlBuildOptions, outputFile)
      else: # Do nothing - don't change password
        for (index, serviceName) in enumerate(buildCacheServices):
          if serviceName in buildCacheServices: # Load service from cache if exists (to maintain password)
            dockerComposeServicesYaml[serviceName] = buildCacheServices[serviceName]
          else:
            dockerComposeServicesYaml[serviceName] = serviceYamlTemplate[serviceName]

  # Build options file didn't exist, so create one, and also use default password (default action).
  else:
    print("PiHole Warning: Build settings file not found, using default password")
    time.sleep(1)
    newAdminPassword = "######" # Update to what's specified in your documentation
    newPassword = "######" # Update to what's specified in your documentation
    for (index, serviceName) in enumerate(serviceYamlTemplate):
      dockerComposeServicesYaml[serviceName] = serviceYamlTemplate[serviceName]
      if "environment" in serviceYamlTemplate[serviceName]:
        for (envIndex, envName) in enumerate(serviceYamlTemplate[serviceName]["environment"]):
          envName = envName.replace("%randomPassword%", newPassword)
          envName = envName.replace("%randomAdminPassword%", newAdminPassword)
          dockerComposeServicesYaml[serviceName]["environment"][envIndex] = envName
      piHoleYamlBuildOptions = {
        "version": "1",
        "application": "IOTstack",
        "service": "PiHole",
        "comment": "PiHole Build Options"
      }

    piHoleYamlBuildOptions["databasePasswordOption"] = "Do nothing"
    with open(buildSettings, 'w') as outputFile:
      yaml.dump(piHoleYamlBuildOptions, outputFile)

  return True
```

## Code for your service's menu
While not needed, since the default action is to create a random password, it is a good idea to allow the user to choose what to do. This can be achieved by giving them access to a password menu. This code can be placed in your service's `build.py` file, that will show a new menu option, allowing users to select it and be taken to a password settings screen.

Remember that you need to have an already working menu, and to place this code into it.

```
import signal

...

def setPasswordOptions():
  global needsRender
  global hasRebuiltAddons
  passwordOptionsMenuFilePath = "./.templates/{currentService}/passwords.py".format(currentService=currentServiceName)
  with open(passwordOptionsMenuFilePath, "rb") as pythonDynamicImportFile:
    code = compile(pythonDynamicImportFile.read(), passwordOptionsMenuFilePath, "exec")
  execGlobals = {
    "currentServiceName": currentServiceName,
    "renderMode": renderMode
  }
  execLocals = {}
  screenActive = False
  exec(code, execGlobals, execLocals)
  signal.signal(signal.SIGWINCH, onResize)
  screenActive = True
  needsRender = 1

...

def createMenu():
  global yourServicesBuildOptions
  global serviceService

  yourServicesBuildOptions = []
  yourServicesBuildOptions.append([
    "Your Service Password Options",
    setPasswordOptions
  ])

  yourServicesBuildOptions.append(["Go back", goBack])

```

## Password settings screen
The code for the Password settings is lengthy, but it's pasted here for convienence
```
#!/usr/bin/env python3

import signal

def main():
  from blessed import Terminal
  from deps.chars import specialChars, commonTopBorder, commonBottomBorder, commonEmptyLine
  from deps.consts import servicesDirectory, templatesDirectory, buildSettingsFileName
  import time
  import subprocess
  import ruamel.yamls
  import os

  global signal
  global currentServiceName
  global menuSelectionInProgress
  global mainMenuList
  global currentMenuItemIndex
  global renderMode
  global paginationSize
  global paginationStartIndex
  global hideHelpText

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
  buildSettings = serviceService + buildSettingsFileName
  
  def goBack():
    global menuSelectionInProgress
    global needsRender
    menuSelectionInProgress = False
    needsRender = 1
    return True

  mainMenuList = []

  hotzoneLocation = [((term.height // 16) + 6), 0]

  menuSelectionInProgress = True
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
      print(term.black_on_cornsilk4(term.center('IOTstack YourServices Password Options')))
      print("")
      print(term.center(commonTopBorder(renderMode)))
      print(term.center(commonEmptyLine(renderMode)))
      print(term.center("{bv}      Select Password Option                                                    {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
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
          print(term.center("{bv}      [Space] to select option                                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Up] and [Down] to move selection cursor                                  {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [H] Show/hide this text                                                   {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
          print(term.center("{bv}      [Enter] to build and save option                                          {bv}".format(bv=specialChars[renderMode]["borderVertical"])))
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

  def loadOptionsMenu():
    global mainMenuList
    mainMenuList.append(["Use default password for this build", { "checked": True }])
    mainMenuList.append(["Randomise database password for this build", { "checked": False }])
    mainMenuList.append(["Randomise database password every build", { "checked": False }])
    mainMenuList.append(["Do nothing", { "checked": False }])

  def checkMenuItem(selection):
    global mainMenuList
    for (index, menuItem) in enumerate(mainMenuList):
      mainMenuList[index][1]["checked"] = False

    mainMenuList[selection][1]["checked"] = True

  def saveOptions():
    try:
      if not os.path.exists(serviceService):
        os.makedirs(serviceService, exist_ok=True)

      if os.path.exists(buildSettings):
        with open(r'%s' % buildSettings) as objBuildSettingsFile:
          yourServicesYamlBuildOptions = yaml.load(objBuildSettingsFile)
      else:
        yourServices = {
          "version": "1",
          "application": "IOTstack",
          "service": "Your Service",
          "comment": "Your Service Build Options"
        }

      yourServices["databasePasswordOption"] = ""

      for (index, menuOption) in enumerate(mainMenuList):
        if menuOption[1]["checked"]:
          yourServices["databasePasswordOption"] = menuOption[0]
          break

      with open(buildSettings, 'w') as outputFile:
        yaml.dump(yourServices, outputFile)

    except Exception as err: 
      print("Error saving Your Services Password options", currentServiceName)
      print(err)
      return False
    global hasRebuiltHardwareSelection
    hasRebuiltHardwareSelection = True
    return True

  def loadOptions():
    try:
      if not os.path.exists(serviceService):
        os.makedirs(serviceService, exist_ok=True)

      if os.path.exists(buildSettings):
        with open(r'%s' % buildSettings) as objBuildSettingsFile:
          yourServicesYamlBuildOptions = yaml.load(objBuildSettingsFile)

        for (index, menuOption) in enumerate(mainMenuList):
          if menuOption[0] == yourServicesYamlBuildOptions["databasePasswordOption"]:
            checkMenuItem(index)
            break

    except Exception as err: 
      print("Error loading Your Services Password options", currentServiceName)
      print(err)
      return False
    return True


  if __name__ == 'builtins':
    global signal
    term = Terminal()
    signal.signal(signal.SIGWINCH, onResize)
    loadOptionsMenu()
    loadOptions()
    with term.fullscreen():
      menuNavigateDirection = 0
      mainRender(needsRender, mainMenuList, currentMenuItemIndex)
      menuSelectionInProgress = True
      with term.cbreak():
        while menuSelectionInProgress:
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
              if saveOptions():
                return True
              else:
                print("Something went wrong. Try saving the list again.")
            if key.name == 'KEY_ESCAPE':
              menuSelectionInProgress = False
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

```