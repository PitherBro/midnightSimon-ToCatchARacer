#!/bin/python3

#Python Modules
import os,sys, urllib3,json,math
from pathlib import Path

#External modules
#makes an HTTP request for a website
import requests
#parses HTML into easily skimmable objects
from bs4 import BeautifulSoup

#where the program rests on the disk
root = Path(os.path.dirname( __file__ ))


'''
#import another module from anywhere
modPath = root/"module"
sys.path.append(modPath)
'''

### most or all variables can be moved into a common.py module

#where the data is on the web
urlResource = "https://midnightsimon.com/"
#where to save our data dumps
dataFolder= root/"data"
#data that still needs to be sanatized
rawDataFolder = dataFolder/"raws"
#a list of objects representing typing champion data over time
jsonFileFolder= dataFolder/"json"

#the local HTML Resource
htmlFile=rawDataFolder/"index.html"
#the final form of the data we want
championsFile=jsonFileFolder/"champions.json"

paths = [
    root,
    dataFolder,
    rawDataFolder,
    jsonFileFolder,
]
'''a list of all know program directories'''


def checkDirs():
    '''
    checks if all the program directories exists, creates them if not.
    '''
    for p in paths:
        if not os.path.exists(p):
            os.mkdir(p)
            print(f"Directory DNE: {p}")

def getHTMLFileOrNot():
    '''
    Gets html source if it does not exist on the files system already.
    '''
    if(not Path.is_file(htmlFile)):
        #makes a live http request
        req = requests.get(urlResource)
        raw_html = req.text
        print(f"Retrived Datafile with Code:{req.status_code}")
        print(raw_html, file=open(htmlFile,"w"))
    print("Completed Check")
    return open(htmlFile,'r').read()

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
        return json.dumps(theDictVersion,indent=2)
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
def getChampList():
    '''
    Return a list of classes (Champion) by scraping index.html
    '''
    #creates the parser for the HTML Data Document
    bs = BeautifulSoup(getHTMLFileOrNot(), "html.parser")
    champElementHolder = bs.find('div', {"id": "champs"})
    championElementList = champElementHolder.find_all('p')

    championList = [Champion]

    for champ in championElementList:
        nameElement = champ.find_all('b')[0]
        champ.replace_with(nameElement, "")

        name = str(nameElement.text.split(" ")[0]).strip()
        dateAndWords = champ.text.split("@")
        date = dateAndWords[0].replace(":", "").strip()
        words = dateAndWords[1].replace(" wpms", "").strip()

        #some have comments beside them, might extract later
        if(len(words.split())>1):
            words = words.split()[0].strip()
            #print(words)

        #print(f"{date} <-> {name} <-> { words}")
        words= int(words)
        alreadyAdded = False

        if(len(championList) > 1):

            for x in range(len(championList)):
                #print(f"testing item: {x}")
                if( not x == 0 and championList[x].name == name):

                    alreadyAdded = True
                    championList[x].addAnotherSingleAttempt(date, words)
        if(not alreadyAdded):
            c = Champion(date, name, words)
            championList.append(c)
            #print(c.convertToJSON())
            
    return championList[1:]

def saveToJSONFile(champList=[Champion]):
    '''
    checks if the champions.json exists, creates from index.html if not
    '''
    champJSONList = []
    for c in champList:
        champJSONList.append(json.loads(c.convertToJSON()))
    if not os.path.isfile(championsFile):
        print(json.dumps(champJSONList, indent=2), file=open(championsFile,'w'))
           
def loadChampionsUpFromJSON():
    '''Return champtions by reading champtions.json'''
    jsonListOfChamps = json.loads(open(championsFile,'r').read())
    listOfChampions = [Champion]

    for c in jsonListOfChamps:
        champ = Champion(name=c["name"])
        champ.replaceExistingLists(c["dates"],c["wordsPerMinute"])
        listOfChampions.append(champ)
    return listOfChampions[1:]



if __name__ == "__main__":

    #preliminary steps to gather and consolidate data
    checkDirs()
    champList = getChampList()
    saveToJSONFile(champList)

    #doing stuff with data
    theRealChampions = loadChampionsUpFromJSON()

    theFastestChamp = theRealChampions[0]
    theSlowestChamp = theRealChampions[0]
    theAverageChamp = theRealChampions[0]

    theMostVictoriousChampion = theRealChampions[0]
    theLeastVictoriousChamption = theRealChampions[0]

    stepTracker =0

    theOverallAverage = theRealChampions[0].getCalculatedAverageWPM()

    for c in theRealChampions:
        #if the most victorious champion has less wins than the current, reassign the champion
        if theMostVictoriousChampion.getCountedWins() < c.getCountedWins():
            print(f"{theMostVictoriousChampion.getName()} is no longer <MOST> champ with {theMostVictoriousChampion.getCountedWins() } wins and is replaced with {c.getName()} and {c.getCountedWins()} wins")
            theMostVictoriousChampion = c
            
        #if the least victorious champion has more wins than the current, reassign the champion
        if len(theLeastVictoriousChamption.getWordsPerLimitList()) > len(c.getWordsPerLimitList()):
            print(f"{theLeastVictoriousChamption.getName()} is no longer <LEAST> champ with {theLeastVictoriousChamption.getCountedWins() } wins and is replaced with {c.getName()} and {c.getCountedWins()} wins")
            theLeastVictoriousChamption = c

        #find the person with most wins, assign them at the top of the loop nest
        #Check person with most wins, against person with least, to find the one who types the fastest, slowest and most average.
        #the average needs to be known previously or, somehow tracked and adjusted during this loop.
        
        
        
        if not stepTracker == 0:
            theOverallAverage += c.getCalculatedAverageWPM() 
            theOverallAverage /= 2
        stepTracker +=1
    
    print(f"""{theMostVictoriousChampion.getName()} is most Victorious with {theMostVictoriousChampion.getCountedWins()} wins\n\
{theLeastVictoriousChamption.getName()} is the least Victorius with {theLeastVictoriousChamption.getCountedWins()}""")

    pass
