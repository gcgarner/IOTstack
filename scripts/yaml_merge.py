import sys
import traceback
import yaml

if sys.argv[1] == "--pyyaml-version":
  try:
    print("pyyaml", yaml.__version__)
    sys.exit(0)
  except SystemExit:
    sys.exit(0)
  except:
    print("could not get pyyaml version")
    sys.exit(3)

if len(sys.argv) < 4:
  print("Error: Not enough args")
  print("Usage:")
  print(" yaml_merge.py [inputFile] [mergeFile] [outputFile]")
  print("")
  print("Example:")
  print(" yaml_merge.py ./.tmp/docker-compose.tmp.yml ./compose-override.yml ./docker-compose.yml")
  sys.exit(4)

try:
  pathTempDockerCompose = sys.argv[1]
  pathOverride = sys.argv[2]
  pathOutput = sys.argv[3]

  def mergeYaml(priorityYaml, defaultYaml):
    finalYaml = {}
    if isinstance(defaultYaml, dict):
      for dk, dv in defaultYaml.items():
        if dk in priorityYaml:
          finalYaml[dk] = mergeYaml(priorityYaml[dk], dv)
        else:
          finalYaml[dk] = dv
      for pk, pv in priorityYaml.items():
        if pk in finalYaml:
          finalYaml[pk] = mergeYaml(finalYaml[pk], pv)
        else:
          finalYaml[pk] = pv
    else:
      finalYaml = defaultYaml
    return finalYaml

  with open(r'%s' % pathTempDockerCompose) as fileTempDockerCompose:
    yamlTempDockerCompose = yaml.load(fileTempDockerCompose, Loader=yaml.SafeLoader)

  with open(r'%s' % pathOverride) as fileOverride:
    yamlOverride = yaml.load(fileOverride, Loader=yaml.SafeLoader)

  mergedYaml = mergeYaml(yamlOverride, yamlTempDockerCompose)

  with open(r'%s' % pathOutput, 'w') as outputFile:
    yaml.dump(mergedYaml, outputFile, default_flow_style=False, sort_keys=False)

  sys.exit(0)
except SystemExit:
  sys.exit(0)
except:
  print("Something went wrong: ")
  print(sys.exc_info())
  print(traceback.print_exc())
  print("")
  print("")
  print("PyYaml Version: ", yaml.__version__)
  print("")
  sys.exit(2)
