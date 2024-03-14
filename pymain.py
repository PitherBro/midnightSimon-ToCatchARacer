#!/bin/python3


#custom made modules
from midnightSimonScraper_C import *

#External modules
#makes an HTTP request for a website
import requests
#parses HTML into easily skimmable objects
from bs4 import BeautifulSoup

'''
#import another module from anywhere
modPath = root/"module"
sys.path.append(modPath)
'''
resultsHeader = "#"*6 + " RESULTS ARE IN " + "#"*6
headerDivider = "-"*12

def getHTMLFileOrNot():
    '''
    Gets html source if it does not exist on the files system already.
    '''
    if(not clb.Path.is_file(clb.htmlFilePath)):
        #makes a live http request
        req = requests.get(clb.urlResource)
        raw_html = req.text
        print(f"Retrived Datafile with Code:{req.status_code}")
        print(raw_html, file=open(clb.htmlFilePath,"w"))
    print("Completed Program Directory Check")
    return open(clb.htmlFilePath,'r').read()

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
    checks if the champions.json exists, creates from index.html Champion List if it DNE
    '''
    champJSONList = []
    for c in champList:
        champJSONList.append(clb.json.loads(c.convertToJSON()))
    if not clb.os.path.isfile(clb.championsFilePath):
        print(clb.json.dumps(champJSONList, indent=2), file=open(clb.championsFilePath,'w'))
           
def loadChampionsUpFromJSON():
    '''Return champtions by reading champtions.json'''
    jsonListOfChamps = clb.json.loads(open(clb.championsFilePath,'r').read())
    listOfChampions = [Champion]

    for c in jsonListOfChamps:
        champ = Champion(name=c["name"])
        champ.replaceExistingLists(c["dates"],c["wordsPerMinute"])
        listOfChampions.append(champ)
    return listOfChampions[1:]

if __name__ == "__main__":

    #preliminary steps to gather and consolidate data
    clb.checkDirs()
    champList = getChampList()
    saveToJSONFile(champList)
    print("----- Data Gathered and Organized From Source -----")
    del champList
    print("----- Excess Memory usage cleared (champList) -----")

    #doing stuff with data
    theRealChampions = loadChampionsUpFromJSON()

    theFastestChamp = theRealChampions[0]
    theSlowestChamp = theRealChampions[0]
    theAverageChamp = theRealChampions[0]

    theMostVictoriousChampion = theRealChampions[0]
    theLeastVictoriousChamption = theRealChampions[0]
    
    theMostImprovedChampion = theRealChampions[0]
    theLeastImprovedChampion = theRealChampions[0]

    stepTracker =0

    theOverallAverage = theRealChampions[0].getAverageWPM()

    for c in theRealChampions:
        #if the most victorious champion has less wins than the current, reassign the champion
        if theMostVictoriousChampion.getCountedWins() < c.getCountedWins():
            print(f"{theMostVictoriousChampion.getName()} is no longer <MOST> champ with {theMostVictoriousChampion.getCountedWins() } wins and is replaced with {c.getName()} and {c.getCountedWins()} wins")
            theMostVictoriousChampion = c
            
        #if the least victorious champion has more wins than the current, reassign the champion
        if len(theLeastVictoriousChamption.getWordsPerLimitList()) > len(c.getWordsPerLimitList()):
            print(f"{theLeastVictoriousChamption.getName()} is no longer <LEAST> champ with {theLeastVictoriousChamption.getCountedWins() } wins and is replaced with {c.getName()} and {c.getCountedWins()} wins")
            theLeastVictoriousChamption = c
        #if the slowest champ is faster, they are not the slowest
        if theSlowestChamp.getSlowestSpeed() > c.getSlowestSpeed():
            theSlowestChamp = c
        #if the fastest champ is slower, they are not the fastest
        if theFastestChamp.getFastestSpeed() < c.getFastestSpeed():
            theFastestChamp = c

        #the most Average
        if theAverageChamp.getAverageWPM() < c.getAverageWPM():
            theAverageChamp = c

        #the least improved
        if theLeastImprovedChampion.getImprovementWeight() > c.getImprovementWeight():
            theLeastImprovedChampion = c

        #the most improved
        if theMostImprovedChampion.getImprovementWeight() < c.getImprovementWeight():
            theMostImprovedChampion = c

        #find the person with most wins, assign them at the top of the loop nest
        #Check person with most wins, against person with least, to find the one who types the fastest, slowest and most average.
        #the average needs to be known previously or, somehow tracked and adjusted during this loop.
        
        if not stepTracker == 0:
            theOverallAverage += c.getAverageWPM() 
            theOverallAverage /= 2
        stepTracker +=1

    print(headerDivider)
    print(resultsHeader)
    print(headerDivider)

    print(f"""\
{theMostVictoriousChampion.getName()} is MOST Victorious with {theMostVictoriousChampion.getCountedWins()} wins\n\
{theLeastVictoriousChamption.getName()} is the LEAST Victorius with {theLeastVictoriousChamption.getCountedWins()}\n\
{theSlowestChamp.getName()} is the SLOWEST with {theSlowestChamp.getSlowestSpeed()} WPM\n\
{theFastestChamp.getName()} is the FASTEST with {theFastestChamp.getFastestSpeed()} WPM\n\
{theAverageChamp.getName()} is the most AVERAGE  with {theAverageChamp.getAverageWPM()} WPM\n\
Program took {stepTracker} steps to complete and calculates a global average of {round(theOverallAverage, 3)} WPM for all Racers\n\
{theLeastImprovedChampion.getName()} is the LEAST IMPROVED with {theLeastImprovedChampion.getCountedWins()} championship wins and a weighted averaged of {theLeastImprovedChampion.getImprovementWeight()}\n\
{theMostImprovedChampion.getName()} is the MOST IMPROVED with {theMostImprovedChampion.getCountedWins()} championship wins and a weighted averaged of {theMostImprovedChampion.getImprovementWeight()}\n\
""")
    testChamp = theRealChampions[0] 
    testChamp.getImprovementWeight()
    #print(f"{testChamp.getName()} {testChamp.getAttendance()[0]} {testChamp.getWordsPerLimitList()[0]}")
    pass
