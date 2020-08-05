import baseFunctions #Importing all functions made by us

#Initalizing all Json
global zoombaStats
zoombaStats = baseFunctions.readJson("zoombaStats.json")

global actionSet
actionSet = baseFunctions.readJson("actionSet.json")

global positionData
positionData = baseFunctions.readJson("positionData.json")

#Json Maintnence Functions
def getZoombaStats():
    global zoombaStats
    zoombaStats = baseFunctions.readJson("zoombaStats.json")

def writeZoombaStats():
    baseFunctions.writeJson("zoombaStats.json",zoombaStats)


def getActionSet():
    global actionSet
    actionSet = baseFunctions.readJson("actionSet.json")

def writeActionSet():
    baseFunctions.writeJson("actionSet.json",actionSet)

def getPositionData():
    global positionData
    positionData = baseFunctions.readJson("positionData.json")

def writePositionData():
    baseFunctions.writeJson("positionData.json",positionData)


#The function that compresses all json gets
def updateAllJSON():
    getActionSet()
    getZoombaStats()
