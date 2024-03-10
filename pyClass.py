#!/bin/python3
import os,sys
from pathlib import Path
root = Path(os.path.dirname( __file__ ))

'''
#import another module from anywhere
modPath = root/"module"
sys.path.append(modPath)
'''

class base:
    
    def __init__(self,) -> None:
        self.name = "base"
        print(self.name)
    pass
