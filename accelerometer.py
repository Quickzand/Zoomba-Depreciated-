#!/usr/bin/env python3
import movement

#This program will be used to get data from the accelerometer pretty much
class staticClass:
    pass
static = staticClass()
static.acceleration = [1,1]

def getAcceleration():  #This will get acceleration from the thing but for now its just one
    return static.acceleration

def writeAcceleration():
    json = movement.readJson("zoombaStats.json")
    json["acceleration"] = getAcceleration()
    movement.writeJson("zoombaStats.json", json)

def setAcceleration(number):        #TEMPERARY FOR NOW BECAUSE THE ACCELEROMETER WILL DO THIS
    static.acceleration = number
