import baseFunctions #Importing all functions made by us

import jsonStorage #Importing All JSON

import math, time

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
    global changeInDegrees
    turnTime = findTurnTime(deg)
    endDirection = jsonStorage.positionData["rotation"] + deg
    changeInDegrees = jsonStorage.zoombaStats["maxSpeed"] * jsonStorage.zoombaStats["radius"]
    while not round(endDirection,2) == round(jsonStorage.positionData["rotation"],2):
        changeInDegrees = changeInDegrees/2
        if endDirection < jsonStorage.positionData["rotation"]:
            while round(endDirection,2) < round(jsonStorage.positionData["rotation"],2):
                turnTickUpdate()
                if abs(changeInDegrees) < 0.01:
                    break
        elif endDirection > jsonStorage.positionData["rotation"]:
            while round(endDirection,2) > round(jsonStorage.positionData["rotation"],2):
                turnTickUpdate()
                if abs(changeInDegrees) < 0.01:
                    break
        if abs(changeInDegrees) < 0.01:
            break
        changeInDegrees *= -1


def turnTickUpdate():
    jsonStorage.positionData["rotation"] = jsonStorage.positionData["rotation"] + changeInDegrees
    jsonStorage.writePositionData()
    time.sleep(jsonStorage.zoombaStats["cycleInterval"])
