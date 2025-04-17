#!/bin/bash

source configs.sh

python3 -m venv $pythonVenvDir
# activates the python virtual environment, must be bash
source $pythonVenv

## rest could be a python module, check libs.
# only if source is active
pip install -r $pythonDepends

# only if requirements met, clears message logs "pages XXXX already installed"
# clear

# launches the program
python3 ./pymain.py