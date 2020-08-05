import baseFunctions #Importing all functions made by us

import jsonStorage #Importing All JSON

import movement #Importing all movement commands



global availableActions
availableActions = {
    "move": movement.moveForward
}

def executeNextAction():
    jsonStorage.getActionSet()
    print(jsonStorage.actionSet)
    pendingActions = jsonStorage.actionSet["pending"]
    if len(pendingActions) > 0:
        currentAction = pendingActions.pop()
        if currentAction[0] in availableActions:
            print("Executing Action: '" + currentAction[0] +"'...")
            availableActions[currentAction[0]](currentAction[1])
        else:
            print("Action: '" + currentAction[0] +"' is not available")
        jsonStorage.actionSet["pastActions"].insert(0,currentAction)
        jsonStorage.writeActionSet()



# Gets Executed Every Cycle Interval and Acts as The System Cycle
def cycle():
    jsonStorage.updateAllJSON()
    executeNextAction()

#Only Runs if main file.
if __name__ == "__main__":
    baseFunctions.call_repeatedly(jsonStorage.zoombaStats["cycleInterval"], cycle)
