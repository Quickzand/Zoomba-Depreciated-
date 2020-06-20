import json, time, sys, optparse
parser = optparse.OptionParser()
parser.add_option("-s","--speed", dest="speed", help="speed of the zoomba")
(options,arguments) = parser.parse_args()
if not options.speed:
    parser.error("PLEASE SPECIFY A SPEED")
viewingDistance = 200
speed = options.speed
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
