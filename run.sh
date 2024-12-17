#!/bin/bash

python3 -m venv venv
#activates the python virtual environment, must be bash
source ./.venv/bin/activate

## rest could be a python module, check libs.
# only if source is active
pip install -r ./requirements.txt

#only if requirements met, clears message logs "pages XXXX already installed"
clear

#launches the program
python3 ./pymain.py