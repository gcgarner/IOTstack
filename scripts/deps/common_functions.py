import time
import string
import random
import sys
import os
import subprocess
from deps.consts import ifCheckList

def generateRandomString(size = 0, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
  if size == 0:
    size = random.randint(16, 24)
  return ''.join(random.choice(chars) for _ in range(size))

def getNetworkDetails(inputList = None):
  ifList = inputList
  if (inputList == None):
    ifList = ifCheckList

  results = {
    "name": "",
    "mac": "",
    "ip": ""
  }

  for (index, ifName) in enumerate(ifList):
    try:
      ip = getIpAddress(ifName)
      mac = getMacAddress(ifName)
      results["name"] = ifName
      results["ip"] = ip
      results["mac"] = mac
      if (results["ip"] == "" or results["mac"] == ""):
        continue
      break
    except:
      continue
      # pass

  return results

def getMacAddress(ifName = None):
  if (ifName == None):
    print("getMacAddress: Need interface name")
    return ""

  mac = ""

  if sys.platform == 'win32':
    print("getMacAddress: Linux support only")
  else:
    FNULL = open(os.devnull, 'w')
    ipRes = subprocess.Popen("/sbin/ifconfig %s" % ifName, shell=True, stdout=subprocess.PIPE, stderr=FNULL).communicate()
    for line in ipRes[0].decode('utf-8').splitlines():
      if line.find('Ethernet') > -1:
        mac = line.split()[1]
        break
  return mac

def getIpAddress(ifName = None):
  if (ifName == None):
    print("getIpAddress: Need interface name")
    return ""

  ip = ""

  if sys.platform == 'win32':
    print("getIpAddress: Linux support only")
  else:
    FNULL = open(os.devnull, 'w')
    ipRes = subprocess.Popen("/sbin/ifconfig %s" % ifName, shell=True, stdout=subprocess.PIPE, stderr=FNULL).communicate()
    for line in ipRes[0].decode('utf-8').splitlines():
      if line.find('inet') > -1:
        ip = line.split()[1]
        break
  return ip

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

def checkDependsOn(serviceName, dockerComposeServicesYaml):
  missingServices = []
  yamlService = dockerComposeServicesYaml[serviceName]
  if "depends_on" in yamlService:
    for (index, dependsOnName) in enumerate(yamlService["depends_on"]):
      if not dependsOnName in dockerComposeServicesYaml:
        missingServices.append([dependsOnName, serviceName])
  return missingServices

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

def enterPortNumberWithWhiptail(term, dockerComposeServicesYaml, currentServiceName, hotzoneLocation, defaultPort):
  newPortNumber = ""
  try:
    portProcess = subprocess.Popen(['./scripts/deps/portWhiptail.sh', defaultPort, currentServiceName], stdout=subprocess.PIPE)
    portResult = portProcess.communicate()[0]
    portResult = portResult.decode("utf-8").split(",")
    newPortNumber = portResult[0]
    returnCode = portResult[1]
    time.sleep(0.1) # Prevent loop
    
    if not returnCode == "0":
      return -1
    
    newPortNumber = int(str(newPortNumber))
    if 1 <= newPortNumber <= 65535:
      time.sleep(0.2) # Prevent loop
      return newPortNumber
    else:
      print(term.center('   {t.white_on_red} "{port}" {message} {t.normal} <-'.format(t=term, port=newPortNumber, message="is not a valid port")))
      time.sleep(2) # Give time to read error
      return -1
  except Exception as err: 
    print(term.center('   {t.white_on_red} "{port}" {message} {t.normal} <-'.format(t=term, port=newPortNumber, message="is not a valid port")))
    print(term.center('   {t.white_on_red} Error: {errorMsg} {t.normal} <-'.format(t=term, errorMsg=err)))
    time.sleep(2.5) # Give time to read error
    return -1

def literalPresenter(dumper, data):
  if isinstance(data, str) and "\n" in data:
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  # if isinstance(data, None):
  #   return self.represent_scalar('tag:yaml.org,2002:null', u'')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')