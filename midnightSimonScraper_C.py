#!/bin/python3
import commonLibs as clb

'''
#import another module from anywhere
modPath = root/"module"
sys.path.append(modPath)
'''

class Champion():
    '''
    a data struct representing a typing racer outcomes 
    '''
    def __init__(self, date="", name="", initialWordCount=0 ) -> None:
        self.name = name
        self.dates = []
        self.wordsPerMinute= []

        self.dates.append(date)
        self.wordsPerMinute.append(initialWordCount)
    def addAnotherSingleAttempt(self, date = "", wordsPerMin=0):
        self.dates.append(date)
        self.wordsPerMinute.append(wordsPerMin)
    def replaceExistingLists(self,dates=[], listOfWords=[]):
        self.dates = dates
        self.wordsPerMinute = listOfWords
    def convertToJSON(self,):
        theDictVersion = {}
        theDictVersion ["name"] = self.name
        theDictVersion["dates"]  = self.dates
        theDictVersion["wordsPerMinute"] = self.wordsPerMinute
        return clb.json.dumps(theDictVersion,indent=2)
    def getWordsPerLimitList(self,):
        return self.wordsPerMinute
    def getAttendance(self,):
        return self.dates
    def getName(self,):
        return self.name
    def getCountedWins(self,):
        return len(self.getWordsPerLimitList())
    def getCalculatedAverageWPM(self):
            total = 0
            for x in self.wordsPerMinute:
                total += x
            
            return total/self.getCountedWins() 
