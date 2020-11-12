import sys
import yaml
import blessed
import ruamel.yaml

if sys.argv[1] == "--pyyaml-version":
  try:
    print("pyyaml", yaml.__version__)
    sys.exit(0)
  except SystemExit:
    sys.exit(0)
  except:
    print("could not get pyyaml version")
    sys.exit(3)

if sys.argv[1] == "--pyaml-version":
  try:
    print("ruamel.yaml", ruamel.yaml.__version__)
    sys.exit(0)
  except SystemExit:
    sys.exit(0)
  except:
    print("could not get ruamel.yaml version")
    sys.exit(3)

if sys.argv[1] == "--blessed-version":
  try:
    print("blessed", blessed.__version__)
    sys.exit(0)
  except SystemExit:
    sys.exit(0)
  except:
    print("could not get blessed version")
    sys.exit(3)
