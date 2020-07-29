import json
from threading import Event, Thread


zoombaStats = readJson("zoombaStats.json")


cycleInterval = zoombaStats["cycleInterval"]

def call_repeatedly(interval, func):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func()
    Thread(target=loop).start()
    return stopped.set



def cycle():
    print("wow")


if __name__ == "__main__":
    call_repeatedly(cycleInterval, cycle)
