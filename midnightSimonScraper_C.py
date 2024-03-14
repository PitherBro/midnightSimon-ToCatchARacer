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
        '''Adds 1 attempt to the existing list of Dates and wordsPerMinute'''
        self.dates.append(date)
        self.wordsPerMinute.append(wordsPerMin)
    def replaceExistingLists(self,dates=[], listOfWords=[]):
        '''Overwrites the existing properies with a new set of data for dates and wordsPerMinute'''
        self.dates = dates
        self.wordsPerMinute = listOfWords
    def convertToJSON(self,):
        '''Converts the class fields into a JSON string'''
        theDictVersion = {}
        theDictVersion ["name"] = self.name
        theDictVersion["dates"]  = self.dates
        theDictVersion["wordsPerMinute"] = self.wordsPerMinute
        return clb.json.dumps(theDictVersion,indent=2)
    def getWordsPerLimitList(self,):
        '''Returns the list of the WPM per attempt recorded'''
        return self.wordsPerMinute
    def getAttendance(self,):
        '''Returns the list of dates that champ won/participated'''
        return self.dates
    def getName(self,):
        '''Returns the name of the champion'''
        return self.name
    def getCountedWins(self,):
        '''Counts the number of wins that the champion has on record'''
        return len(self.getWordsPerLimitList())
    def getAverageWPM(self):
            '''Calculates the Champions average WPM, based on the wordsPerMinute List'''
            total = 0
            for x in self.wordsPerMinute:
                total += x

            return round(total/self.getCountedWins(),3) 
    def getFastestSpeed(self,):
        '''Compares the first recorded WPM aginst all attempts recorded, to find the fastest WPM'''
        fastestSpeed = self.wordsPerMinute[0]
        for w in self.wordsPerMinute:
            if fastestSpeed < w:
                fastestSpeed = w
        return fastestSpeed
    def getSlowestSpeed(self):
        '''Compares the first recorded WPM aginst all attempts recorded, to find the slowest WPM'''
        slowestSpeed = self.wordsPerMinute[0]
        for w in self.wordsPerMinute:
            if slowestSpeed > w:
                slowestSpeed = w
        return slowestSpeed
    def getImprovementWeight(self,):
        '''
        Takes the earliest known attempt and subtracts the next known attempt by it.\n
        Thus if 125 is the earliest and 127 is the next win, then the weight is 2.\n
        It is then added by the diffrence of 127 and the next earliest words per minute.\n
        Returns the total weight to compare against the others for most improved.\n
        '''
        startDate = ""
        endDate = ""
        currentWeight = 0

        newestDate = self.wordsPerMinute[0]
        wonComps = len(self.wordsPerMinute)-1

        x = wonComps
        #print(wonComps)
        while x > 0 :
            
            currentWeight += self.wordsPerMinute[x-1] - self.wordsPerMinute[x] 
            #print(f"{x}: {currentWeight}")
                #print(f"{self.name} {x}:  {self.wordsPerMinute[x]}")
            x -= 1
        #print(f"weighted improvement: {currentWeight}")
        return currentWeight