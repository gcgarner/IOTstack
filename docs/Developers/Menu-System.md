# Menu system

This page explains how the menu system works for developers.

## Background
Originally this script was written in bash. After a while it became obvious that bash wasn't well suited to dealing with all the different types of configuration files, and logic that goes with configuring everything. IOTstack needs to be accessible to all levels of programmers and tinkerers, not just ones experienced with Linux and bash. For this reason, it was rewritten in Python since the language syntax is easier to understand, and is more commonly used for scripting and programming than bash. Bash is still used in IOTstack where it makes sense to use it, but the menu system itself uses Python. The code it self while not being the most well structured or efficient, was intentionally made that way so that beginners and experienced programmers could contribute to the project. We are always open to improvements if you have suggestions.

## Menu Structure

Each screen of the menu is its own Python script. You can find most of these in the `./scripts` directory. When you select an item from the menu, and it changes screens, it actually dynamically loads and executes that Python script. It passes data as required by placing it into the global variable space so that both the child and the parent script can access it.

### Injecting and getting globals in a child script
```
with open(childPythonScriptPath, "rb") as pythonDynamicImportFile:
  code = compile(pythonDynamicImportFile.read(), childPythonScriptPath, "exec")
execGlobals = {
  "globalKeyName": "globalKeyValue"
}
execLocals = {}
print(globalKeyName) # Will print out 'globalKeyValue'
exec(code, execGlobals, execLocals)
print(globalKeyName) # Will print out 'newValue'
```

### Reading and writing global variables in a child script
```
def someFunction:
  global globalKeyName
  print(globalKeyName) # Will print out 'globalKeyValue'
  globalKeyName = "newValue"
```

Each menu is its own python executable. The entry point is down the bottom of the file wrapped in a `main()` function to prevent variable scope creep.

The code at the bottom of the `main()` function:
```
if __name__ == 'builtins':
```

Is actually where the execution path runs, all the code above it is just declared so that it can be called without ordering or scope issues.

### Optimisations

It was obvious early on that the menu system would be slow on lower end devices, such as the Raspberry Pi, especially if it were rending a 4k terminal screen from a desktop via SSH. To mitigate this issue, not all of the screen is redrawn when there is a change. A "Hotzone" as it's called in the code, is usually rerendered when there's a change (such as pressing up or down to change an item selection, but not when scrolling). Full screen redraws are expensive and are only used when required, for example, when scrolling the pagination, selecting or deselecting a service, expanding or collapsing the menu and so on.

### Environments and encoding
At the very beginning of the main menu screen (`./scripts/main_menu.py`) the function `checkRenderOptions()` is run to determine what characters can be displayed on the screen. It will try various character sets, and eventually default to ASCII if none of the fancier stuff can be rendered. This setting is passed into of the sub menus through the submenu's global variables so that they don't have to recheck when they load.

### Sub-Menus

From the main screen, you will see several sections leading to various submenus. Most of these menus work in the same way as the main menu. The only exception to this rule is the Build Stack menu, which is probably the most complex part of IOTstack.

## Build Stack Menu

Path: `./scripts/buildstack_menu.py`

### Loading

1. Upon loading, the Build Stack menu will get a list of folders inside the `./templates` directory and check for a `build.py` file inside each of them. This can be seen in the `generateTemplateList()` function, which is executed before the first rendering happens.
2. The menu will then check if the file `./services/docker-compose.save.yml` exists. This file is used to save the configuration of the last build. This happens in the `loadCurrentConfigs()` function. It is important that the service name in the compose file matches the folder name, any service that doesn't will either cause an error, or won't be loaded into the menu.
3. If a previous build did exist the menu will then run the `prepareMenuState()` function that basically checks which items should be ticked, and check for any issues with the ticked items by running `checkForIssues()`.

### Selection and deselection
When an item is selected, 3 things happen:
1. Update the UI variable (`menu`) with function `checkMenuItem(selectionIndex)` to let the user know the current state.
2. Update the array holding every checked item `setCheckedMenuItems()`. It uses the UI variable (`menu`) to know which items are set.
3. Check for any issues with the new list of selected items by running `checkForIssues()`.

### Check for options (submenus of services)
During a full render sequence (this is not a hotzone render), the build stack menu checks to see if each of the services has an options menu. It does this by executing the `build.py` script of each of the services and passing in `checkForOptionsHook` into the `toRun` global variable property to see if the script has a `runOptionsMenu` function. If the service's function result is true, without error, then the options text will appear up for that menu item.

### Check for issues
When a service is selected or deselected on the menu, the `checkForIssues()` function is run. This function iterates through each of the selected menu items' folders executing the `build.py` script and passing in `checkForRunChecksHook` into the `toRun` global variable property to see if the script has a `runChecks` function. The `runChecks` function is different depending on the service, since each service has its own requirements. Generally though, the `runChecks` function should check for conflicting port conflicts again any of the other services that are enabled. The menu will still allow you to build the stack, even if issues are present, assumine there's no errors raised during the build process.

### Prebuild hook
Pressing enter on the Build Stack menu kicks off the build process. The Build Stack menu will execute the `runPrebuildHook()` function. This function iterates through each of the selected menu items' folders executing the `build.py` script and passing in `checkForPreBuildHook` into the `toRun` global variable property to see if the script has a `preBuild` function. The `preBuild` function is different depending on the service, since each service has its own requirements. Some services may not even use the prebuild hook. The prebuild is very useful for setting up the services' configuration however. For example, it can be used to autogenerate a password for a paticular service, or copy and modify a configuration file from the `./.templates` directory into the `./services` or `./volumes` directory.

### Postbuild hook
The Build Stack menu will execute the `runPostBuildHook()` function in the final step of the build process, after the `docker-compose.yml` file has been written to disk. This function iterates through each of the selected menu items' folders executing the `build.py` script and passing in `checkForPostBuildHook` into the `toRun` global variable property to see if the script has a `postBuild` function. The `postBuild` function is different depending on the service, since each service has its own requirements. Most services won't require this function, but it can be useful for cleaning up temporary files and so on.

### The build process
The selected services' yaml configuration is already loaded into memory before the build stack process is started.

1. Run prebuildHooks.
2. Read `./.templates/docker-compose-base.yml` file into a in memory yaml structure.
3. Add selected services into the in memory structure.
4. If it exists merge the `./compose-override.yml` file into memory
5. Write the in memory yaml structure to disk `./docker-compose.yml`.
6. Run postbuildHooks.
7. Run `postbuild.sh` if it exists, with the list of services built.
