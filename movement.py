import json, time, sys, argparse


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

def turnRight(deg):
    turnTime = findTurnTime(deg)
    t_end = time.time() + turnTime
    changeInDegrees = deg/turnTime
    starttime = time.time()
    while time.time() < t_end:
        turnOnLeftWheels("forward")
        turnOnRightWheels("backwards")
        positionData["rotation"] = positionData["rotation"] + changeInDegrees
        writeJson("positionData.json",positionData)
        if positionData["rotation"] > 360:
            positionData["rotation"] = positionData["rotation"] - 360


def turnLeft(deg):
    turnTime = findTurnTime(deg)
    t_end = time.time() + turnTime
    changeInDegrees = deg/turnTime
    while time.time() < t_end:
        turnOnLeftWheels("forward")
        turnOnRightWheels("backwards")
        positionData["rotation"] = positionData["rotation"] - changeInDegrees
        writeJson("positionData.json",positionData)
        if positionData["rotation"] > 360:
            positionData["rotation"] = positionData["rotation"] - 360



def findTurnTime(deg):
    return deg/((zoombaStats["speed"]*zoombaStats["radius"])/2.0) # Original Equation Is change in theta = 0.5 * (wi + w) * t




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




def cycle():
    global zoombaStats
    global positionData
    wow = True
    while True:
        zoombaStats = readJson("zoombaStats.json")
        positionData = readJson("positionData.json")



        if wow:
            turnRight(100)
            wow = False
        writeJson("positionData.json",positionData)


if __name__ == "__main__":
    #options = getArgs()
    #statsPath = options.statsPath
    pass

cycle()
