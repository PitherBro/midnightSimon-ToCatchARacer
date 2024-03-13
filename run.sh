#!/bin/bash

#activates the python virtual environment
source ./.venv/bin/activate

# only if source is active
pip install -r ./requirements.txt

#only if requirements met, clears message logs "pages XXXX already installed"
clear

#launches the program
python3 ./pymain.py