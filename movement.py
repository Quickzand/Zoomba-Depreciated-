import json, time, sys, argparse
import accelerometer

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
    time = findturnTime(deg)

def turnLeft(deg):
    time = findturnTime(deg)

def findTurnTime(deg):
    return deg/(angularSpeed/2) # Original Equation Is change in theta = 0.5 * (wi + w) * t

def updateSpeedAndAcceleration():           #This should be run on a separate thread
    while True:
        changeInTime = 0.01
        getAcceleration()
        moving.speed = moving.speed + moving.acceleration * changeInTime   #Vf = vi + a*t

        json = readJson("zoombaStats.json")
        json["speed"] = moving.speed
        writeJson("zoombaStats.json", json)

        time.sleep(changeInTime)

def getAcceleration():
    moving.acceleration = readJson("zoombaStats.json")["acceleration"]


def deccelerate():
    # Normally Code to Make the Zoomba Decelerate Would go here, but this is temp Code

if __name__ == "__main__":
    #options = getArgs()
    #statsPath = options.statsPath
    pass
