import re

def checkVersion(requiredVersion, currentVersion):
  """
  >>> checkVersion('18.2.0', '20.10.11')
  (True, '', [])
  >>> checkVersion('18.2.0', '16.3.1')
  (False, 'Version Check Fail', [False, False, True])
  >>> checkVersion('18.2.0', '20.10.5+dfsg1')
  (True, '', [])
  """
  requiredSplit = requiredVersion.split('.')

  if len(requiredSplit) < 2:
    return False, 'Invalid Required Version', requiredVersion

  try:
    requiredMajor = int(requiredSplit[0])
    requiredMinor = int(requiredSplit[1])
    requiredBuild = int(requiredSplit[2])
  except:
    return False, 'Invalid Required Version', requiredVersion

  currentSplit = currentVersion.split('.')

  if len(currentSplit) < 2:
    return False, 'Invalid Current Version', currentVersion

  try:
    currentMajor = int(currentSplit[0])
    currentMinor = int(currentSplit[1])
    currentBuild = re.split(r'[+-]', currentSplit[2])[0]
    currentBuild = int(currentBuild)
  except:
    return False, 'Invalid Current Version', currentVersion

  if currentMajor > requiredMajor:
    return True, '', []

  if currentMajor == requiredMajor and currentMajor > requiredMinor:
    return True, '', []

  if currentMajor == requiredMajor and currentMinor == requiredMinor and currentBuild >= requiredBuild:
    return True, '', []

  return False, 'Version Check Fail', [currentMajor == requiredMajor, currentMinor == requiredMinor, currentBuild >= requiredBuild]