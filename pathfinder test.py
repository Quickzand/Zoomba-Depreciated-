import random, argparse, json, math, sys
#
#parser = argparse.ArgumentParser()
#parser.add_argument("-w","--wallsPath", dest="wallsPath", help="Path Of The Walls JSON")
#options = parser.parse_args()
#if not options.wallsPath:
#    parser.error("PLEASE SPECIFY A WALLS PATH")
#wallsPath = options.wallsPath

wallsPath = "walls.json"
def readJson(fname):
    with open(fname) as f:
        output = json.load(f)
        return output


def writeJson(fName,data):
    with open(fName,'w') as outfile:
        json.dump(data,outfile)


wallsJson = readJson(wallsPath)
global walls
walls = wallsJson["walls"]

zoombaStats = readJson("zoombaStats.json")
positionData = readJson("positionData.json")
# Creating a class 'station' which would be like a node on the screen
class Station:
    def __init__(self, i, j):
        """ Set is present for the coloring purpose"""
        self.set = 0
        self.i = i
        self.j = j
        # f is the cost function
        # g is like the actual distance from the starting point
        # h is the heuristic - shortest possible distance - here, it would be displacement (euclidean distance)
        self.f = 0
        self.g = 0
        self.h = 0
        # To trace back the path, we need to record parents
        self.parent = None
        self.wall = False
        # list of neighbors of a station
        self.neighbors = []
        #THIS IS HOW WALLS ARE SET WE DID IT BOYS
        if self.checkIfWall():
            self.wall = True
    def checkIfWall(self):
        posArray = [self.i,self.j]
        if posArray in walls:
            return True
        else:
            return False

    def add_neighbors(self, grid_passed):
        """Returns list of neighbor stations"""
        i = self.i
        j = self.j
        if j < size - 1:
            self.neighbors.append(grid_passed[i][j + 1])
        if i > 0:
            self.neighbors.append(grid_passed[i - 1][j])
        if j > 0:
            self.neighbors.append(grid_passed[i][j - 1])
        if i < size - 1:
            self.neighbors.append(grid_passed[i + 1][j])
        if i < size - 1 and j < size - 1:
            self.neighbors.append(grid_passed[i + 1][j + 1])
        if i > 0 and j < size - 1:
            self.neighbors.append(grid_passed[i - 1][j + 1])
        if i < size - 1 and j > 0:
            self.neighbors.append(grid_passed[i + 1][j - 1])
        if i > 0 and j > 0:
            self.neighbors.append(grid_passed[i - 1][j - 1])


# Used a class instead of array just to update the value of set every time a station is added to open_set
class Set:
    def __init__(self, array):
        self.array = array

    def add(self, station, var):
        if var == 'open':
            station.set = -5
        self.array.append(station)


def heuristic(a, b):
    """Our heuristic function"""
    dist = ((a.i - b.i)**2 + (a.j - b.j)**2)**0.5
    return dist


open_set = []
open_set = Set(open_set)
closed_set = []
closed_set = Set(closed_set)
global size
global xChange
global yChange
size = int(round(math.sqrt(((positionData["x"] - zoombaStats["destination"]["x"])*(positionData["x"] - zoombaStats["destination"]["x"])) + ((positionData["y"] - zoombaStats["destination"]["y"])*(positionData["y"] - zoombaStats["destination"]["y"]))) + 100))
if positionData["x"] < zoombaStats["destination"]["x"]:
    xChange = zoombaStats["destination"]["x"]
else:
    xChange = int(round(positionData["x"]))

if positionData["y"] < zoombaStats["destination"]["y"]:
    yChange = zoombaStats["destination"]["y"]
else:
    yChange = int(round(positionData["y"]))
print(size)
grid = []

# Making a grid
for i in range(size):
    row = [Station(0, 0) for i in range(size)]
    grid.append(row)

# Allotting one Station object to each of the element in the grid
for i in range(size):
    for j in range(size):
        grid[i][j] = Station(i, j)

# Filling neighbours
for i in range(size):
    for j in range(size):
        grid[i][j].add_neighbors(grid)

start = grid[int(0)][int(0)]
#int(round(positionData["x"]))][int(round(positionData["y"]))
end = grid[(zoombaStats["destination"]["x"]-xChange)][(zoombaStats["destination"]["y"]-yChange)]
grid[0][0].wall = False
grid[size - 1][size - 1].wall = False

# Adding the start point to the open_set
open_set.add(start, 'open')

# Actual loop
a = 0
while a < 1:
    if open_set.array:
        winner = 0
        for i in range(len(open_set.array)):
            if open_set.array[i].f < open_set.array[winner].f:
                winner = i
        current = open_set.array[winner]

        if current == end:
            # Calculating path
            current.set = 8
            while current.parent:
                current.parent.set = 16
                current = current.parent
            print('Done')
            a = a + 1

        # Remove the evaluated point from open_set and add to closed_set
        open_set.array.pop(winner)
        closed_set.array.append(current)

        # Adding a new point to evaluate in open_set
        neighbors = current.neighbors
        for neighbor in neighbors:
            if neighbor not in closed_set.array:
                if not neighbor.wall:
                    temp_g = current.g + 1
                    new_path = False
                    if neighbor in open_set.array:
                        if temp_g < neighbor.g:
                            neighbor.g = temp_g
                            new_path = True
                    else:
                        neighbor.g = temp_g
                        new_path = True
                        open_set.add(neighbor, 'open')
                    if new_path:
                        neighbor.h = heuristic(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.parent = current
            # print(neighbor.parent)
    else:
        current.set = 12
        while current.parent:
            current.parent.set = 8
            current = current.parent
        print('No path found!')
        a = a + 1

# For debugging purpose - Visualisation
vis_grid = []
for i in range(size):
    row = [0 for i in range(size)]
    vis_grid.append(row)

start.set = 20
end.set = 25
for i in range(size):
    for j in range(size):
        if grid[i][j].wall:
            vis_grid[i][j] = grid[i][j].set - 10
        else:
            vis_grid[i][j] = grid[i][j].set

pathJSON = {"path":[]}
basePath = {
    "points": []
}
for i in range(size):
    for j in range(size):
        basePath["points"].append([(i+xChange),(j+yChange)])
        print( str(i) + "," + str(j))



writeJson('pathPoints.json',basePath)

linePath = {
    "path": [
        {"start":[positionData["x"],positionData["y"]],"end":[round(basePath["points"][1][0]),round(basePath["points"][1][1])]}
    ]
}

def pointIsOnLine(m, c, x, y):
    if (y == ((m * x) + c)):
        return True;
    return False;

for point in basePath["points"]:
    currentLine = linePath["path"][-1]
    if (currentLine["end"][0] - currentLine["start"][0]) == 0 or currentLine["end"] == point:
        currentLine["end"] = point
        continue
    else:
        currentSlope = (currentLine["end"][1] - currentLine["start"][1])/(currentLine["end"][0] - currentLine["start"][0])
    yInt = currentLine["end"][1]-(currentLine["end"][0]*currentSlope)
    if pointIsOnLine(currentSlope,yInt,point[0],point[1]):
        currentLine["end"] = point
    else:
        linePath["path"].append({"start":currentLine["end"],"end":point})


res = []
for i in linePath["path"]:
    if i not in res and not i["start"] == i["end"]:
        res.append(i)
linePath["path"] = res
writeJson('path.json',linePath)



#plt.figure(figsize =(12, 12))
#plt.title('A* Algorithm - Shortest Path Finder\n')
#plt.imshow(vis_grid)
#plt.show()
