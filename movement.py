import baseFunctions #Importing all functions made by us

import jsonStorage #Importing All JSON

import math

global moveCount
moveCount = 0
def moveForward(dist):
    global changeInPos
    global moveCount
    moveCount = 0
    speed = jsonStorage.zoombaStats["maxSpeed"]
    moveTime = dist/speed
    changeInPos = (dist / moveTime) * jsonStorage.zoombaStats["cycleInterval"]
    stopMoving = baseFunctions.call_repeatedly(0.1,forwardTimeUpdate)
    while moveCount < (moveTime/jsonStorage.zoombaStats["cycleInterval"]):
        RandomActionGoesHere = True #Didnt know how else to wait for the condition to be false
    moveCount = 0
    stopMoving()

def forwardTimeUpdate():
    global moveCount
    jsonStorage.positionData["x"] = jsonStorage.positionData["x"] + (math.cos((math.pi/180) * jsonStorage.positionData["rotation"]) * changeInPos)
    jsonStorage.positionData["y"] = jsonStorage.positionData["y"] + (math.sin((math.pi/180) * jsonStorage.positionData["rotation"]) * changeInPos)
    moveCount = moveCount + 1
    baseFunctions.writeJson("positionData.json",jsonStorage.positionData)


def findTurnTime(deg):
    return abs(deg/((jsonStorage.zoombaStats["maxSpeed"]*jsonStorage.zoombaStats["radius"])/2.0)) # Original Equation Is change in theta = 0.5 * (wi + w) * t

def turn(deg):
    global turnCount
    global changeInDegrees
    turnCount = 0
    turnTime = findTurnTime(deg)
    changeInDegrees = (deg/turnTime) * jsonStorage.zoombaStats["cycleInterval"]
    stopTurning = baseFunctions.call_repeatedly(0.1,turnTimeUpdate)
    while turnCount < (turnTime/jsonStorage.zoombaStats["cycleInterval"]):
        RandomActionGoesHere = True #Didnt know how else to wait for the condition to be false
    turnCount = 0
    stopTurning()

def turnTimeUpdate():
    jsonStorage.positionData["rotation"] = jsonStorage.positionData["rotation"] + changeInDegrees
    jsonStorage.writePositionData()
    global turnCount
    turnCount = turnCount + 1
