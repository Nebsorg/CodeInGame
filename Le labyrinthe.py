import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.

_ROW = 0
_COL = 1
_DIR = 2
_CRITERIA = 3
_DIR_VECTOR = [[-1,0], [0,1], [1, 0], [0,-1]]
_DIR_NAME = ["UP", "RIGHT", "DOWN", "LEFT"]

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

def isPositionInNodeListe(position, nodeListe):
    for node in nodeListe:
        if (node.position[0] == position[0]) and (node.position[1] == position[1]):
            return(True)
    return(False)

def astar(start, end, maze, avoidConsole):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = set()
    closed_list = set()

    # Add the start node
    open_list.add(start_node)

    # Loop until you find the end or you explore all the open node
    while len(open_list) > 0:
        # Get the best node (with lower f)
        current_node = next(iter(open_list))
        for item in open_list:
            if item.f < current_node.f:
                current_node = item

        # Pop current off open list, add to closed list
        open_list.discard(current_node)
        closed_list.add(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path
 
        # Generate new open node
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == '#' or maze[node_position[0]][node_position[1]] == '?':
                continue
            
            if avoidConsole:
                if maze[node_position[0]][node_position[1]] == 'C':
                    continue

            # Make sure position is not already in a list
            if isPositionInNodeListe(node_position, open_list) or isPositionInNodeListe(node_position, closed_list):
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            new_node.g = current_node.g + 1
            new_node.h = 0
            new_node.f = new_node.g + new_node.h

            # Append
            open_list.add(new_node)
            #print("astar - adding {0} to open list - len Open list = {1} - len closed list = {2}".format(new_node.position, len(open_list), len(closed_list)), file=sys.stderr, flush=True)
    return([])

def displayLabyrinthe(labi, kirkPos):
    result = ""
    for i in range(0, len(labi)):
        line = labi[i]
        if i == kirkPos[_ROW]:
            strLine = ''
            for j in range(0, len(line)):
                if j == kirkPos[_COL]:
                    strLine += 'K'
                else:
                    strLine += str(line[j])
            result += strLine + "\n"
        else:
            result += ''.join(line) + "\n"
    return(result)

def displayPath(labi, path):
    result = ""
    modifiedLabi = labi

    for i in range(len(path)):
        pos = path[i]
        modifiedLabi[pos[_ROW]][pos[_COL]] = '*'
        if i == len(path)-1:
            modifiedLabi[pos[_ROW]][pos[_COL]] = 'O'

    for i in range(0, len(modifiedLabi)):
        line = modifiedLabi[i]
        result += ''.join(line) + "\n"
    return(result)


def isFree(row, col):
    # return true if it's possible to move there
    if 0 <= row < len(detectedLabyrinth) and 0 <= col < len(detectedLabyrinth[0]):
        if detectedLabyrinth[row][col] != '#':
            return True
    else:
        return False

def getUnknownPositionAround(pos):
    vector = [-2,-1,0,1,2]
    unknown = 0
    for rowshift in vector: 
        for colshift in vector:
            testRow = pos[_ROW]+rowshift
            testCol = pos[_COL]+colshift
            if 0 <= testRow < len(detectedLabyrinth) and 0 <= testCol < len(detectedLabyrinth[0]):
                if detectedLabyrinth[testRow][testCol] == "?":
                    unknown += 1
    return(unknown)


def getFreePositionOnly(pos):
    freePos = []
    for i in range(0,4):
        testRow = pos[_ROW] + _DIR_VECTOR[i][_ROW]
        testCol = pos[_COL] + _DIR_VECTOR[i][_COL]
        if (isFree(testRow, testCol)):
            freePos.append((testRow, testCol))
    return(freePos)



def getFreePositionAround(pos):
    freePos = []
    for i in range(0,4):
        testRow = pos[_ROW] + _DIR_VECTOR[i][_ROW]
        testCol = pos[_COL] + _DIR_VECTOR[i][_COL]
        if (isFree(testRow, testCol)):
            freePos.append((testRow, testCol, _DIR_NAME[i], getUnknownPositionAround((testRow, testCol))))
    return(freePos)

def isPositionInList(position, liste):
    for pos in liste:
        if (pos[_ROW] == position[_ROW]) and (pos[_COL] == position[_COL]):
            return(True)
    return(False)


def getClosestReachableUnexploredPosition(initialPosition):
    positionFind = False
    positionToTest = set()
    positionTested = set()

    distance = 0
    positionToTest.add((initialPosition[_ROW], initialPosition[_COL], distance))
    while len(positionToTest) > 0:
        ##  On prends la position à tester la plus proche
        testPos = next(iter(positionToTest))
        for pos in positionToTest:
            if pos[2] < testPos[2]:
                testPos = pos
        ## Est-ce que cette position est innexplorée ? 
        if (testPos[_ROW],testPos[_COL]) not in exploredPosition:
            ## Inexploré. Est-ce qu'elle est atteignable, en evitant d'actionner la console ? 
            path = astar(initialPosition, (testPos[_ROW], testPos[_COL]), detectedLabyrinth, True)
            if len(path) > 0:
                print("getClosestReachableUnexploredPosition : {0} et atteignable, on y va - Path{1}".format(testPos, path), file=sys.stderr, flush=True)    
                return(path[1], (testPos[_ROW], testPos[_COL]))
            print("getClosestReachableUnexploredPosition : {0} inexploré mais non atteignable".format(testPos), file=sys.stderr, flush=True)
        
        ## cette position n'est pas valide, on l'ajoute au position testée, et on testes les suivantes
        positionToTest.discard(testPos)
        positionTested.add(testPos)
        distance += 1
        for pos in getFreePositionOnly(testPos):
            if isPositionInList(pos, positionToTest) or isPositionInList(pos, positionTested):
                continue
            positionToTest.add((pos[_ROW], pos[_COL], distance))
    print("getClosestReachableUnexploredPosition : Distance={0} - No reachable unexplore position found !!! crashing :)".format(distance), file=sys.stderr, flush=True)
    return([])




def exploring():
    ## On commence par regarder les mouvements possible autours de Kirk, enrichie de la direction pour y aller, et du nombre de case inconnues autours
    freePosList = getFreePositionAround(kirkPos)

    ## Strategie de recherche : on se deplace vers le point avec le plus de zone inconnue autours
    ## Si tous les points autours n'ont pas de zone inconnue, on se dirige vers la case inexploree la plus proche
    choosenPos = freePosList[0]
    for pos in freePosList:
        if pos[_CRITERIA] > choosenPos[_CRITERIA]:
            choosenPos = pos
        
    if choosenPos[_CRITERIA] == 0:
        #nothing to reveal, we prioritize to move on unexpored position
        global targetPos 
        nextPosition, targetPos = getClosestReachableUnexploredPosition(kirkPos)
        print("Exploring : all squared around already reveal - move to closest unexplore position {0}".format(targetPos), file=sys.stderr, flush=True)
        return(getDirectionFromPosition(kirkPos, nextPosition))
    else:
        print("Exploring : Moving to position which maximize discovery {0} (max unknown = {1})".format(choosenPos, choosenPos[_CRITERIA]), file=sys.stderr, flush=True)
        return(choosenPos[_DIR])
      

def getDirectionFromPosition(kirkPos, targetPos):
    if targetPos[_ROW] == kirkPos[_ROW] + 1:
        return("DOWN")
    elif  targetPos[_ROW] == kirkPos[_ROW] - 1:
        return("UP")
    elif  targetPos[_COL] == kirkPos[_COL] - 1:
        return("LEFT")
    else:
        return("RIGHT")


### Debut du main
nbOfRow, nbOfColumn, alarmRound = [int(i) for i in input().split()]
exploredPosition = set()
currentPathFollowed = []
startPos = None
consolePos = None
consoleFound = False
consoleActivated = False
targetPos = None
pathToFollow = []

# game loop
while True:
    # kr: row where Kirk is located.
    # kc: column where Kirk is located.
    kirkRow, kirkCol = [int(i) for i in input().split()]
    kirkPos = (kirkRow, kirkCol)
    exploredPosition.add(kirkPos)

    if targetPos != None:
        if kirkPos == targetPos:
            targetPos = None

    if kirkPos == consolePos:
        consoleActivated = True
        targetPos = startPos

    if consoleActivated:
        alarmRound -= 1

    if startPos == None:
        startPos = kirkPos

    ## Mise à jour du Labyrinthe
    detectedLabyrinth = []
    numberOfUnknownCells = 0
    for i in range(nbOfRow):
        line = input()
        numberOfUnknownCells += line.count('?')
        if not consoleFound: 
            if 'C' in line: 
                consoleFound = True
                consolePos = (i, line.index('C'))
        detectedLabyrinth.append(list(line))  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).

    ## Affichage du status
    if (not consoleFound):
        strConsole = "Not found"
    else:
        if consoleActivated:
            strConsole = "Found {1} & Activated - Alarm triggered in {0} rounds".format(alarmRound, consolePos)
        else:
            strConsole = "Found {0} & Not Activated (Alarm tick : {1})".format(consolePos, alarmRound)
    print("Kirk Position={0} - Target:{2} - Unkown Cells:{3} - Console Status: {1}".format(kirkPos, strConsole, targetPos, numberOfUnknownCells), file=sys.stderr, flush=True)

    ## On regarde si on a trouvé la console (et non activé)
    if consoleFound and not consoleActivated: 
        ## est-ce qu'on sait y aller ? 
        pathToFollow = astar(kirkPos, consolePos, detectedLabyrinth, False)
        if len(pathToFollow) == 0:
            ## on ne sait pas rejoindre la console, on explore dans sa direction : 
            print("Console found - No path found to console - exploring in his direction (target set to consolePos)", file=sys.stderr, flush=True)
            targetPos = consolePos
        else: 
            ## on sait rejoindre la console. Mais avant d'y aller et de l'activer, on regarde si le chemin du retour est assez court
            pathToFollow = astar(consolePos, startPos, detectedLabyrinth, False)
            if 0 < len(pathToFollow) <= alarmRound + 2:
                ## c'est bon, on peut y aller
                targetPos = consolePos
                print("Console found - path found to console, return path short enough ({0}) and alarm will not trigger ({1})! - moving to console".format(len(pathToFollow), alarmRound), file=sys.stderr, flush=True)
                # print(displayPath(detectedLabyrinth, pathToFollow), file=sys.stderr, flush=True)
            else:
                print("Console found - path found to console, but return path is too long ({0}) and alarm will trigger ({1})! - keep exploring".format(len(pathToFollow), alarmRound), file=sys.stderr, flush=True)
                # print(displayPath(detectedLabyrinth, pathToFollow), file=sys.stderr, flush=True)
                exploredPosition.add(consolePos) ## on rajoute la console a la liste des epxloré pour eviter d'aller dessus par erreur
                targetPos = None
    
    ## si on a une target, on cherche à l'atteindre
    ## sinon on explore
    if targetPos != None:
        # on a une target, on essaye de le rejoidre avec A*
        pathToFollow = astar(kirkPos, targetPos, detectedLabyrinth, False)
        if len(pathToFollow) > 0:
            nextPosition = pathToFollow[1]
            nextMove = getDirectionFromPosition(kirkPos, nextPosition)
            print("A* : Path found to target {2} - Following Path (lenght={0}) - moving to {1}".format(len(pathToFollow)-1, nextMove, targetPos), file=sys.stderr, flush=True)
        else:
            # on a une target mais pas de chemin, on explore
            print("No path found with A*, exploring to find a path to target", file=sys.stderr, flush=True)
            nextMove = exploring()
    else:
        # pas de target, on explore
        nextMove = exploring()

    print("Explored Position size = {0}".format(len(exploredPosition)), file=sys.stderr, flush=True)
    print(displayLabyrinthe(detectedLabyrinth, kirkPos), file=sys.stderr, flush=True)    

    print(nextMove)
    