#!/bin/python3

#Python Modules
import os,sys, urllib3
from pathlib import Path

#External modules
#makes an HTTP request for a website
import requests
#parses HTML into easily skimmable objects
from bs4 import BeautifulSoup


root = Path(os.path.dirname( __file__ ))

'''
#import another module from anywhere
modPath = root/"module"
sys.path.append(modPath)
'''

if __name__ == "__main__":
    #print(__name__)
    #print(sys.argv)    
    #print(sys.path)
    print(root)
    pass
