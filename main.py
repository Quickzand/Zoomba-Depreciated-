import json, time, sys
viewingDistance = 200
speed = 1
diameter = 20
angularSpeed = speed*(diameter/2)
cycleSpeed = 0.25
obstaclePosNumber = 1



obstacleData = {
"0":[0,0]
}



def writeObstacles(fName):
    with open(fName,'w') as outfile:
        json.dump(obstacleData,outfile)

def turnRight(deg):
    time = findturnTime(deg)

def turnLeft(deg):
    time = findturnTime(deg)


def findTurnTime(deg):
    return deg/(angularSpeed/2) # Original Equation Is change in theta = 0.5 * (wi + w) * t

def cycle():
    writeObstacles('test.json')
    time.sleep(cycleSpeed)


while True:
    cycle()
