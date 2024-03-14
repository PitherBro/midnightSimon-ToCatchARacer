#!/bin/python3

#Python Modules
import os,sys, urllib3,json,math
from pathlib import Path

root = Path(os.path.dirname( __file__ ))

#where the data is on the web
urlResource = "https://midnightsimon.com/"
#where to save our data dumps
dataFolder= root/"data"
#data that still needs to be sanatized
rawDataFolder = dataFolder/"raws"
#a list of objects representing typing champion data over time
jsonFileFolder= dataFolder/"json"

#the local HTML Resource
htmlFilePath=rawDataFolder/"index.html"
#the final form of the data we want
championsFilePath=jsonFileFolder/"champions.json"

paths = [
    root,
    dataFolder,
    rawDataFolder,
    jsonFileFolder,
]
'''a list of all known program directories'''
def checkDirs():
    '''
    checks if all the program directories exists, creates them if not.
    '''
    for p in paths:
        if not os.path.exists(p):
            os.mkdir(p)
            print(f"Directory DNE: {p}")
'''
#import another module from anywhere
modPath = root/"module"
sys.path.append(modPath)
'''