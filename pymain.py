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

#terminal output stylings 
header="#"*6
resultsHeader = header + " RESULTS ARE IN " + header
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
    table :BeautifulSoup= bs.find('table') 
    rows :BeautifulSoup= table.find_all('tr')[1:]

    championList = [Champion]

    for dataElement in rows:
        # print(dataElement)
        rowData= dataElement.find_all('th')
        # dataElement.replace_with(rowData, "")

        date = rowData[1].text
        name = rowData[2].text
        words = rowData[3].text

        # #some have comments beside them, might extract later
        # if(len(words.split())>1):
        #     words = words.split()[0].strip()
        #     #print(words)

        #print(f"{date} <-> {name} <-> { words}")
        try:
            words= int(words)
        except:
            words = 0
            # print("error in getChampList")
        if words > 0:
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
    '''Return champions by reading champions.json'''
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
    #removes the list since we can use the newly generated JSON file
    del champList
    print("----- Excess Memory usage cleared (champList) -----")

    #doing stuff with data
    theRealChampions = loadChampionsUpFromJSON()
    theFirstChampion :Champion = theRealChampions[0]

    
    theFastestChamp = theFirstChampion
    theSlowestChamp = theFirstChampion
    theAverageChamp = theFirstChampion

    theMostVictoriousChampion = theFirstChampion
    theLeastVictoriousChamption = theFirstChampion
    
    theMostImprovedChampion = theFirstChampion
    theLeastImprovedChampion = theFirstChampion

    stepTracker = 0

    theOverallAverage = theFirstChampion.getAverageWPM()

    for c in theRealChampions:
        champ: Champion = c
        #if the most victorious champion has less wins than the current, reassign the champion
        if theMostVictoriousChampion.getCountedWins() < champ.getCountedWins():
            print(f"{theMostVictoriousChampion.getName()} is no longer <MOST> champ with {theMostVictoriousChampion.getCountedWins() } wins and is replaced with {champ.getName()} and {champ.getCountedWins()} wins")
            theMostVictoriousChampion = champ
            
        #if the least victorious champion has more wins than the current, reassign the champion
        if len(theLeastVictoriousChamption.getWordsPerLimitList()) > len(champ.getWordsPerLimitList()):
            print(f"{theLeastVictoriousChamption.getName()} is no longer <LEAST> champ with {theLeastVictoriousChamption.getCountedWins() } wins and is replaced with {champ.getName()} and {champ.getCountedWins()} wins")
            theLeastVictoriousChamption = champ
        #if the slowest champ is faster, they are not the slowest
        if theSlowestChamp.getSlowestSpeed() > champ.getSlowestSpeed():
            theSlowestChamp = champ
        #if the fastest champ is slower, they are not the fastest
        if theFastestChamp.getFastestSpeed() < champ.getFastestSpeed():
            theFastestChamp = champ

        #the most Average
        if theAverageChamp.getAverageWPM() < champ.getAverageWPM():
            theAverageChamp = champ

        #the least improved
        if theLeastImprovedChampion.getImprovementWeight() > champ.getImprovementWeight():
            theLeastImprovedChampion = champ

        #the most improved
        if theMostImprovedChampion.getImprovementWeight() < champ.getImprovementWeight():
            theMostImprovedChampion = champ

        #find the person with most wins, assign them at the top of the loop nest
        #Check person with most wins, against person with least, to find the one who types the fastest, slowest and most average.
        #the average needs to be known previously or, somehow tracked and adjusted during this loop.
        
        if not stepTracker == 0:
            theOverallAverage += champ.getAverageWPM() 
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
