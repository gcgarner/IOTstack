import time

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

def enterPortNumber(term, dockerComposeServicesYaml, currentServiceName, hotzoneLocation, createMenuFn):
  newPortNumber = ""
  try:
    print(term.move_y(hotzoneLocation[0]))
    print(term.center("                                              "))
    print(term.center("                                              "))
    print(term.center("                                              "))
    print(term.move_y(hotzoneLocation[0] + 1))
    time.sleep(0.1) # Prevent loop
    newPortNumber = input(term.center("Enter new port number: "))
    # newPortNumber = sys.stdin.readline()
    time.sleep(0.1) # Prevent loop
    newPortNumber = int(str(newPortNumber))
    if 1 <= newPortNumber <= 65535:
      time.sleep(0.2) # Prevent loop
      internalPort = getInternalPorts(currentServiceName, dockerComposeServicesYaml)[0]
      dockerComposeServicesYaml[currentServiceName]["ports"][0] = "{newExtPort}:{oldIntPort}".format(
        newExtPort = newPortNumber,
        oldIntPort = internalPort
      )
      createMenuFn()
      return True
    else:
      print(term.center('   {t.white_on_red} "{port}" {message} {t.normal} <-'.format(t=term, port=newPortNumber, message="is not a valid port")))
      time.sleep(2) # Give time to read error
      return False
  except Exception as err: 
    print(term.center('   {t.white_on_red} "{port}" {message} {t.normal} <-'.format(t=term, port=newPortNumber, message="is not a valid port")))
    print(term.center('   {t.white_on_red} Error: {errorMsg} {t.normal} <-'.format(t=term, errorMsg=err)))
    time.sleep(2.5) # Give time to read error
    return False
