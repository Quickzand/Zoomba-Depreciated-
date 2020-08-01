import baseFunctions



zoombaStats = baseFunctions.readJson("zoombaStats.json")







def cycle():
    print("wow")


if __name__ == "__main__":
    baseFunctions.call_repeatedly(zoombaStats["cycleInterval"], cycle)
