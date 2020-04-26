import sys
import yaml

if len(sys.argv) < 4:
  print("Error: Not enough args")
  print("Usage:")
  print(" yaml_merge.py [inputFile] [mergeFile] [outputFile]")
  print("")
  print("Example:")
  print(" yaml_merge.py ./.tmp/docker-compose.tmp.yml ./compose-override.yml ./docker-compose.yml")
  sys.exit(1)

pathTempDockerCompose = sys.argv[1]
pathOverride = sys.argv[2]
pathOutput = sys.argv[3]

def mergeYaml(priorityYaml, extensionYaml):
  if isinstance(priorityYaml,dict) and isinstance(extensionYaml,dict):
    for k,v in extensionYaml.iteritems():
      if k not in priorityYaml:
        priorityYaml[k] = v
      else:
        priorityYaml[k] = mergeYaml(priorityYaml[k],v)
  return priorityYaml

with open(r'%s' % pathTempDockerCompose) as fileTempDockerCompose:
  yamlTempDockerCompose = yaml.load(fileTempDockerCompose)

with open(r'%s' % pathOverride) as fileOverride:
  yamlOverride = yaml.load(fileOverride)

mergedYaml = mergeYaml(yamlOverride, yamlTempDockerCompose)

with open(r'%s' % pathOutput, 'w') as outputFile:
  # yaml.dump(mergedYaml, outputFile, default_flow_style=False, sort_keys=False) # TODO: 'sort_keys' not available in this version of Python/yaml
  yaml.dump(mergedYaml, outputFile, default_flow_style=False)
