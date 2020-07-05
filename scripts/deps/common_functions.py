def getExternalPorts(serviceName, dockerComposeServicesYaml):
  externalPorts = []
  try:
    yamlService = dockerComposeServicesYaml[serviceName]
    if "ports" in yamlService:
      for (index, port) in enumerate(yamlService["ports"]):
        try:
          externalAndInternal = port.split(":")
          externalPorts.append(externalAndInternal[0])
        except:
          pass
  except:
    pass
  return externalPorts

def getInternalPorts(serviceName, dockerComposeServicesYaml):
  externalPorts = []
  try:
    yamlService = dockerComposeServicesYaml[serviceName]
    if "ports" in yamlService:
      for (index, port) in enumerate(yamlService["ports"]):
        try:
          externalAndInternal = port.split(":")
          externalPorts.append(externalAndInternal[1])
        except:
          pass
  except:
    pass
  return externalPorts

def checkPortConflicts(serviceName, currentPorts, dockerComposeServicesYaml):
  portConflicts = []
  yamlService = dockerComposeServicesYaml[serviceName]
  servicePorts = getExternalPorts(serviceName, dockerComposeServicesYaml)
  for (index, servicePort) in enumerate(servicePorts):
    for (index, currentPort) in enumerate(currentPorts):
      if (servicePort == currentPort):
        portConflicts.append([servicePort, serviceName])
  return portConflicts
