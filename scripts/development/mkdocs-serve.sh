#!/bin/bash
set -eu

# Install location agnostic "cd ~/IOTstack"
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Create python virtualenv and install any changes to the requirements:
virtualenv .virtualenv-mkdocs
source .virtualenv-mkdocs/bin/activate
pip3 install --upgrade -r requirements-mkdocs.txt

mkdocs serve "$@"
