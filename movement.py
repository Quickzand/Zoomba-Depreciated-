import json, time, sys, argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s","--statsPath", dest="statsPath", help="Path Of The Zoomba Stats")
options = parser.parse_args()
if not options.statsPath:
    parser.error("PLEASE SPECIFY A STATS PATH")
statsPath = options.statsPath

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
