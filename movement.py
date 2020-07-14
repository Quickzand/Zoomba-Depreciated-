import json, time, sys, argparse, threading, math, os
from threading import Event, Thread
global turnCount
turnCount = 0
global moveCount
moveCount = 0


class movingClass:          #basically just want organized static variables
    pass
moving = movingClass()
moving.forward = False
moving.left = False
moving.right = False
moving.speed = 0
moving.acceleration = 0

# def getArgs():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-s","--statsPath", dest="statsPath", help="Path Of The Zoomba Stats")
#     options = parser.parse_args()
#     if not options.statsPath:
#         parser.error("PLEASE SPECIFY A STATS PATH")
#     return options

def writeJson(fName,data):
    with open(fName,'w') as outfile:
        json.dump(data,outfile)

def readJson(fname):
    with open(fname) as f:
        output = json.load(f)
    return output

def call_repeatedly(interval, func, changeInDegrees):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(changeInDegrees)
    Thread(target=loop).start()
    return stopped.set

def turnRight(deg):
    global turnCount
    turnTime = findTurnTime(deg)
    changeInDegreesInput = deg/turnTime
    endMe = call_repeatedly(0.1,turnRightTimeUpdate,changeInDegrees=changeInDegreesInput*0.1)
    starttime = time.time()
    t_end = time.time() + turnTime
    while turnCount < (turnTime/0.1):
        RandomActionGoesHere = True #Didnt know how else to wait for the condition to be false
    turnCount = 0
    endMe()


def turnRightTimeUpdate(changeInDegrees):
    turnOnLeftWheels("forward")
    turnOnRightWheels("backward")
    positionData["rotation"] = positionData["rotation"] + changeInDegrees
    writeJson("positionData.json",positionData)
    positionData["rotation"] = positionData["rotation"] % 360
    global turnCount
    turnCount = turnCount + 1


def turnLeft(deg):
    global turnCount
    turnTime = findTurnTime(deg)
    changeInDegreesInput = deg/turnTime
    endMe = call_repeatedly(0.1,turnLeftTimeUpdate,changeInDegrees=changeInDegreesInput*0.1)
    starttime = time.time()
    t_end = time.time() + turnTime
    while turnCount < (turnTime/0.1):
        RandomActionGoesHere = True #Didnt know how else to wait for the condition to be false
    turnCount = 0
    endMe()

def turnLeftTimeUpdate(changeInDegrees):
    turnOnLeftWheels("backward")
    turnOnRightWheels("forward")
    positionData["rotation"] = positionData["rotation"] - changeInDegrees
    writeJson("positionData.json",positionData)
    if positionData["rotation"] < 0:
        positionData["rotation"] = positionData["rotation"] + 360
    global turnCount
    turnCount = turnCount + 1


def findTurnTime(deg):
    return deg/((zoombaStats["speed"])/2.0) # Original Equation Is change in theta = 0.5 * (wi + w) * t
    # t = theta / (0.5 * (wi + w))
    #THIS WAS WRONG MATTHEW YOU DID * INSTEAD OF +




def updateSpeedAndAcceleration():           #This should be run on a separate thread
        changeInTime = 0.01
        getAcceleration()
        moving.speed = moving.speed + moving.acceleration * changeInTime   #Vf = vi + a*t

        zoombaStats["speed"] = moving.speed
        writeJson("zoombaStats.json", json)

        time.sleep(changeInTime)

def getAcceleration():
    moving.acceleration = readJson("zoombaStats.json")["acceleration"]





def turnOnLeftWheels(direction): #Code To Turn On Left Wheels Would Go Here - Should NEVER be used in isolation
    if direction == "forward":
        #Code To Go Forward Goes Here
        testWow = 1
    elif direction == "backwards":
        #Code To Go Backwards Goes here
        testWow = 1

def turnOnRightWheels(direction): #Code To Turn On Right Wheels Would Go Here - Should NEVER be used in isolation
    if direction == "forward":
        #Code To Go Forward Goes Here
        testWow = 1
    elif direction == "backwards":
        #Code To Go Backwards Goes here
        testWow = 1

def rotate(deg):
    turn(deg)

def turn(deg): #ammount to turn
    if deg < 0:
        turnLeft(deg * -1)
    else:
        turnRight(deg)

def forward(dist):
    #The Code To Move foward
    moveTime = dist/zoombaStats["speed"]
    global moveCount
    if moveTime == 0:
        changeInPos = dist
    else:
        changeInPos = dist/moveTime
    endMe = call_repeatedly(0.1,forwardTimeUpdate,changeInPos*0.1)
    starttime = time.time()
    t_end = time.time() + moveTime
    while moveCount < (moveTime/0.1):
        RandomActionGoesHere = True #Didnt know how else to wait for the condition to be false
    moveCount = 0
    endMe()

def forwardTimeUpdate(changeInPos):
    turnOnLeftWheels("forward")
    turnOnRightWheels("forward")
    positionData["x"] = positionData["x"] + (math.cos((math.pi/180) * positionData["rotation"]) * changeInPos)
    positionData["y"] = positionData["y"] + (math.sin((math.pi/180) * positionData["rotation"]) * changeInPos)
    writeJson("positionData.json",positionData)
    if positionData["rotation"] < 0:
        positionData["rotation"] = positionData["rotation"] + 360
    global moveCount
    moveCount = moveCount + 1

pathData = readJson("path.json")

def lookAt(x,y):
    x = zoombaStats["destination"]["x"]                                         #This is just temp so i can use it on random points without finding the function that calls this
    y = zoombaStats["destination"]["y"]

    changeInX = x - positionData["x"]
    changeInY = y - positionData["y"]

    angleOfLine = math.atan2(changeInY,changeInX)
    angleOfLineDeg = angleOfLine * 180 / math.pi

    if positionData["rotation"] % 360 > angleOfLineDeg:                         #This is to get the most efficient direction without fucking with negatives
        amountToTurn = positionData["rotation"] % 360 - angleOfLineDeg
        if amountToTurn > 180:
            amountToTurn = amountToTurn - 180
            return(amountToTurn)
        else:
            if amountToTurn > 180:
                amountToTurn = amountToTurn - 180
                return((amountToTurn*-1))
            return((amountToTurn*-1))
    elif positionData["rotation"] % 360 < angleOfLineDeg:
        amountToTurn = angleOfLineDeg - positionData["rotation"] % 360
        return(amountToTurn)

    #if changeInY == 0:
    #     if changeInX < 0:
    #         deg = 180
    #     else:
    #         deg = 0
    # else:
    #     if changeInY < 0:
    #         deg = 180 + math.atan2(changeInY,changeInX)
    #     else:
    #         if changeInX < 0:
    #             deg = 180 - math.atan2(changeInY,changeInX)
    #         else:
    #             deg = math.atan2(changeInY,changeInX)
    #
    # #changeInDegrees = -math.atan2(changeInY,changeInX) - (math.pi/2)
    # return "rotate("+str(deg - positionData["rotation"])+")"



def followPath():
    global pathData
    if len(pathData["path"]) > 0:
        line = pathData["path"].pop(0)
        if line["start"][0] == 0:
            angle = 0
        else:
            angle = math.atan2(line["start"][1]-positionData["y"],line["start"][0] - positionData["x"])
        #print angle
        #print positionData["rotation"]
        zoombaStats["actions"].append("rotate("+str(lookAt(line["end"][0],line["end"][1]))+")")
        xDist = line["start"][0] - line["end"][0]
        yDist = line["start"][1] - line["end"][1]
        dist = math.sqrt((xDist*xDist) + (yDist * yDist))
        zoombaStats["actions"].append("forward("+str(dist)+")")



def pathfind():
    os.system('python pathfinder.py')
    #exec(open('pathfinder.py').read())
    #execfile("pathfinder.py")

def cycle(hmmm):
    global zoombaStats
    global positionData
    global pathData
    zoombaStats = readJson("zoombaStats.json")
    positionData = readJson("positionData.json")
    actionSet = zoombaStats["actions"]
    if len(actionSet) > 0:
        print("Executing... " + actionSet[0])
        exec(actionSet.pop(0))
    else:
        followPath()
    zoombaStats["actions"] = actionSet
    writeJson("positionData.json",positionData)
    writeJson("zoombaStats.json",zoombaStats)
    writeJson("path.json",pathData)


if __name__ == "__main__":
    #options = getArgs()
    #statsPath = options.statsPath
    call_repeatedly(0.1,cycle,5)
