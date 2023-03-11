#!/usr/bin/env python3

#  This script will return a markdown table containing the service names, mode (host or non-host), and default
#  external ports used by all services found in the .templates directory. The markdown output can be used to 
#  quickly update the docs/Basic_setup/Default-Configs.md file.

import glob
import pathlib
import re

# Setup columns & print service names, mode, and default ports.

print("| Service Name | Mode | Port(s)<br> *External:Internal* |")
print("| ------------ | -----| --------------- |")

# Change directories

currentPath = pathlib.Path(__file__)
dirName = str(currentPath.parents[1])
templates = glob.glob(dirName + '/.templates/**/service.yml',recursive = True)

# Iterate through service.ymls for required info.

for template in sorted(templates):
    
    with open(template) as file:
        
        fileInput = file.read()

        # Search for service names and mode.

        try:
            serviceName = re.search(r'container_name:.?(["a-z0-9_-]+)', fileInput).group(1)
        except:
            serviceName = 'Parsing error'
        try:
            if (re.search(r'^([^\#]\s+network_mode:).?([a-z0-9]+)', fileInput,flags = re.M).group(2) == 'host'):
                mode = 'host'
        except:
            mode = 'non-host'        
        
        # Print service and mode but do not end the line.

        print("| " + serviceName + " | " + mode + " | ", end= "")
        
        # Search for ports used by each service. findall is split into 2 groups to deal with #'s in some service.yml's.
        # Keep only the ports and not the whitespace or "-"
        
        portSearchResult = re.findall(r'^(\s*[-]\s*"*)(\d{2,5}[:]\d{2,5})', fileInput,re.M)
        ports = []
        for result in portSearchResult:
            ports.append(result[1])
        
        # Get rid of found doubles - UDP and TCP ports etc.
        
        dropDuplicates = []
        [dropDuplicates.append(port) for port in ports if port not in dropDuplicates]
        
        # Print the ports used and end the line when the for loop completes.

        for port in dropDuplicates:
            print(port + " <br> ", end= "")
        print("|")