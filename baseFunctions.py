import json
from threading import Event, Thread
def call_repeatedly(interval, func):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func()
    Thread(target=loop).start()
    return stopped.set


def writeJson(fName,data):
    with open(fName,'w') as outfile:
        json.dump(data,outfile)

def readJson(fname):
    with open(fname) as f:
        output = json.load(f)
    return output
