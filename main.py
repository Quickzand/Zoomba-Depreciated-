import baseFunctions #Importing all functions made by us

import jsonStorage #Importing All JSON

def forward(test):
    print(test)

def display(test):
    print(test)

global availableActions
availableActions = {
    "move": forward,
    "print": display
}

def executeNextAction():
    pendingActions = jsonStorage.actionSet["pending"]
    if len(pendingActions) > 0:
        currentAction = pendingActions.pop()
        if currentAction[0] in availableActions:
            availableActions[currentAction[0]](currentAction[1])
        else:
            print("Action: '" + currentAction[0] +"' is not available")
        jsonStorage.actionSet["pastActions"].insert(0,currentAction)
        jsonStorage.writeActionSet()



# Gets Executed Every Cycle Interval and Acts as The System Cycle
def cycle():
    jsonStorage.updateAllJSON()
    executeNextAction()
    print(jsonStorage.zoombaStats)

#Only Runs if main file.
if __name__ == "__main__":
    baseFunctions.call_repeatedly(jsonStorage.zoombaStats["cycleInterval"], cycle)
