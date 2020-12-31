#!/usr/bin/python3
import sys

if sys.argv[1] == "--pyyaml-version":
  try:
    import yaml
    print("pyyaml", yaml.__version__)
    sys.exit(0)
  except SystemExit:
    sys.exit(0)
  except Exception:
    print("could not get pyyaml version")
    sys.exit(3)

if sys.argv[1] == "--pyaml-version":
  try:
    import ruamel.yaml
    print("ruamel.yaml", ruamel.yaml.__version__)
    sys.exit(0)
  except SystemExit:
    sys.exit(0)
  except Exception:
    print("could not get ruamel.yaml version")
    sys.exit(3)

if sys.argv[1] == "--blessed-version":
  try:
    import blessed
    print("blessed", blessed.__version__)
    sys.exit(0)
  except SystemExit:
    sys.exit(0)
  except Exception:
    print("could not get blessed version")
    sys.exit(3)
