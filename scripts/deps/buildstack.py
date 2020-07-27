import os
import yaml
import math
import sys
from deps.yaml_merge import mergeYaml
from deps.consts import servicesDirectory, templatesDirectory, volumesDirectory, buildCache, envFile, dockerPathOutput, servicesFileName, composeOverrideFile

buildScriptFile = 'build.py'

def buildServices(dockerComposeServicesYaml):
  try:
    runPrebuildHook()
    dockerFileYaml = {}
    menuStateFileYaml = {}
    dockerFileYaml["version"] = "3.6"
    dockerFileYaml["services"] = {}
    menuStateFileYaml["services"] = {}
    dockerFileYaml["services"] = dockerComposeServicesYaml
    menuStateFileYaml["services"] = dockerComposeServicesYaml

    if os.path.exists(envFile):
      with open(r'%s' % envFile) as fileEnv:
        envSettings = yaml.load(fileEnv, Loader=yaml.SafeLoader)
      mergedYaml = mergeYaml(envSettings, dockerFileYaml)
      dockerFileYaml = mergedYaml

    if os.path.exists(composeOverrideFile):
      with open(r'%s' % composeOverrideFile) as fileOverride:
        yamlOverride = yaml.load(fileOverride, Loader=yaml.SafeLoader)

      mergedYaml = mergeYaml(yamlOverride, dockerFileYaml)
      dockerFileYaml = mergedYaml

    with open(r'%s' % dockerPathOutput, 'w') as outputFile:
      yaml.dump(dockerFileYaml, outputFile, default_flow_style=False, sort_keys=False)

    with open(r'%s' % buildCache, 'w') as outputFile:
      yaml.dump(menuStateFileYaml, outputFile, default_flow_style=False, sort_keys=False)
    runPostBuildHook()
    return True
  except Exception as err: 
    print("Issue running build:")
    print(err)
    input("Press Enter to continue...")
    return False

def runPrebuildHook(dockerComposeServicesYaml):
  for (index, checkedMenuItem) in enumerate(checkedMenuItems):
    buildScriptPath = templatesDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
    if os.path.exists(buildScriptPath):
        with open(buildScriptPath, "rb") as pythonDynamicImportFile:
          code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
        execGlobals = {
          "dockerComposeServicesYaml": dockerComposeServicesYaml,
          "toRun": "checkForPreBuildHook",
          "currentServiceName": checkedMenuItem
        }
        execLocals = locals()
        try:
          exec(code, execGlobals, execLocals)
          if "preBuildHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["preBuildHook"]:
            execGlobals = {
              "dockerComposeServicesYaml": dockerComposeServicesYaml,
              "toRun": "preBuild",
              "currentServiceName": checkedMenuItem
            }
            execLocals = locals()
            exec(code, execGlobals, execLocals)
        except Exception as err:
          print("Error running PreBuildHook on '%s'" % checkedMenuItem)
          print(err)
          input("Press Enter to continue...")
          try: # If the prebuild hook modified the docker-compose object, pull it from the script back to here.
            dockerComposeServicesYaml = execGlobals["dockerComposeServicesYaml"]
          except:
            pass

def runPostBuildHook():
  for (index, checkedMenuItem) in enumerate(checkedMenuItems):
    buildScriptPath = templatesDirectory + '/' + checkedMenuItem + '/' + buildScriptFile
    if os.path.exists(buildScriptPath):
        with open(buildScriptPath, "rb") as pythonDynamicImportFile:
          code = compile(pythonDynamicImportFile.read(), buildScriptPath, "exec")
        execGlobals = {
          "dockerComposeServicesYaml": dockerComposeServicesYaml,
          "toRun": "checkForPostBuildHook",
          "currentServiceName": checkedMenuItem
        }
        execLocals = locals()
        try:
          exec(code, execGlobals, execLocals)
          if "postBuildHook" in execGlobals["buildHooks"] and execGlobals["buildHooks"]["postBuildHook"]:
            execGlobals = {
              "dockerComposeServicesYaml": dockerComposeServicesYaml,
              "toRun": "postBuild",
              "currentServiceName": checkedMenuItem
            }
            execLocals = locals()
            exec(code, execGlobals, execLocals)
        except Exception as err:
          print("Error running PostBuildHook on '%s'" % checkedMenuItem)
          print(err)
          input("Press Enter to continue...")
