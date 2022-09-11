
def mergeYaml(priorityYaml, defaultYaml):
  if not priorityYaml:
      return defaultYaml
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
