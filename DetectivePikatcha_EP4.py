import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

VECTOR = [[-1,0], [0,1], [1, 0], [0,-1]]

size = int(input())
cube = []
for k in range(6):
    grille = []
    for i in range(size):
        line = list(input())
        for j in range(len(line)):
            cell = line[j]
            if cell == '>':
                pika = [i, line.index('>'), RIGHT, k]
            elif cell == '<': 
                pika = [i, line.index('<'), LEFT, k]
            elif cell == '^': 
                pika = [i, line.index('^'), UP, k]
            elif cell == 'v': 
                pika = [i, line.index('v'), DOWN, k]
            if (cell != '#'):
                line[j] = 0
        grille.append(line)
    cube.append(grille)
side = input()

def getNextPosition(currentPosition, cube, side):
    #Testing if there is a wall at side:
    if(side == 'L'):
        directionToCheck = -1
        rotationMouvement = 1
    else:
        directionToCheck = 1
        rotationMouvement = -1

    # identifying what is on side of Pika:
    pikaSideDirection = (currentPosition[2] + directionToCheck) % 4
    PikaSideI = currentPosition[0] + VECTOR[pikaSideDirection][0]
    PikaSideJ = currentPosition[1] + VECTOR[pikaSideDirection][1]
    PikaFace = currentPosition[3]

    #print("** Pika is in (%d,%d,%d) - Following it"%(currentPosition[0], currentPosition[1], currentPosition[2]), file=sys.stderr, flush=True)                
    testIfFree, PikaSideI, PikaSideJ, pikaSideDirection, PikaFace = isFreeCube(PikaSideI, PikaSideJ, pikaSideDirection, PikaFace, cube)
    if not testIfFree:
        # there is a wall on the side followed
        # Try to follow it in the same direction
        #print("** Wall on position (%d,%d,%d) - Following it"%(PikaSideI, PikaSideJ, pikaSideDirection), file=sys.stderr, flush=True)                
        positionFound = False
        direction = currentPosition[2]
        iteration = 0
        while not positionFound:
            posI = currentPosition[0] + VECTOR[direction][0]
            posJ = currentPosition[1] + VECTOR[direction][1]
            posFace = currentPosition[3]
            # print("   -> Checking position (%d,%d,%d)"%(posI, posJ, direction), file=sys.stderr, flush=True)        
            testIfFree, posI, posJ, direction, posFace= isFreeCube(posI, posJ, direction, posFace, cube)
            if testIfFree:
                # print("   -> it's free. Moving to it", file=sys.stderr, flush=True)        
                return posI, posJ, direction, posFace

            direction = (direction + rotationMouvement) % 4
            # print("   -> it's NOT Free - changing direction : %d"%(direction), file=sys.stderr, flush=True)      
            iteration += 1
            if iteration > 4:
                return -1,-1,-1,-1
    else:
        # no wall there. Moving here to follow the wall
        #print("** Free on position (%d,%d,%d) - Going There"%(PikaSideI, PikaSideJ, pikaSideDirection), file=sys.stderr, flush=True)                
        return PikaSideI, PikaSideJ, pikaSideDirection, PikaFace
    return -1,-1,-1,-1

def isFree(i,j,face,cube): 
    # return true if it's possible to move there
    size = len(cube[0])
    if 0 <= i < size and 0 <= j < size:
        if cube[face][i][j] != '#':
            return True
    else:
        return False

def isFreeCube(i,j,direction, face,cube): 
    # return true if it's possible to move there, includinc cube capability
    lastLine = len(cube[0]) - 1
    lastColumn = lastLine
    if 0 <= i <= lastLine and 0 <= j <= lastColumn:
        # within boudaries - no cube effect
        if cube[face][i][j] != '#':
            return True, i, j, direction, face
        else:
            return False, i, j, direction, face
    elif j < 0:
        # Leaving face from left : changing face if possible
        if (face == 3) or (face == 2):
            #leaving face 3 or 2 by left, arriving on face 2 or 1 from right
            newFaceI = i
            newFaceJ = lastColumn
            direction = LEFT
            newFace = face - 1
        elif (face == 0):
            #leaving face 0 by left, arriving on face 1 from the top: 
            newFaceI = 0
            newFaceJ = i
            newFace = 1
            direction = DOWN
        elif (face == 1):
            #leaving face 1 by left, arriving on face 5 from the right: 
            newFaceI = lastLine - i 
            newFaceJ = 0
            newFace = 5
            direction = RIGHT
        elif (face == 4):
            #leaving face 4 by left, arriving on face 1 from the bottom: 
            newFaceI = lastLine
            newFaceJ = lastColumn - i
            newFace = 1
            direction = UP
        elif (face == 5):
            #leaving face 5 by left, arriving on face 1 by left: 
            newFaceI = lastLine - i
            newFaceJ = 0
            newFace = 1
            direction = RIGHT

        if isFree(newFaceI, newFaceJ, newFace, cube):
            return True, newFaceI, newFaceJ, direction, newFace

    elif j > lastColumn:
        # Leaving face of Cube by right : changing face if possible
        if (face == 1) or (face == 2):
            #leaving face 1 or 2 by right, arriving on face 2 or 3 from left
            newFaceI = i
            newFaceJ = 0
            direction = RIGHT
            newFace = face + 1
        elif (face == 0):
            #leaving face 0 by right, arriving on face 3 from the top: 
            newFaceI = 0
            newFaceJ = lastLine - i
            newFace = 3
            direction = DOWN
        elif (face == 3):
            #leaving face 3 by right, arriving on face 5 from the right: 
            newFaceI = lastLine - i 
            newFaceJ = lastColumn
            newFace = 5
            direction = LEFT
        elif (face == 4):
            #leaving face 4 by right, arriving on face 3 from the bottom: 
            newFaceI = lastLine
            newFaceJ = i
            newFace = 3
            direction = UP
        elif (face == 5):
            #leaving face 5 on the right, arriving on face 3 fr om the right: 
            newFaceI = lastLine - i
            newFaceJ = lastColumn
            newFace = 3
            direction = LEFT

        if isFree(newFaceI, newFaceJ, newFace, cube):
            return True, newFaceI, newFaceJ, direction, newFace
        
    elif i < 0:
        # Leaving face from Top : changing face if possible
        if (face == 5) or (face == 4) or (face == 2):
            #leaving face 5, 4 or 2 by top, arriving on face 4, 2 or 0 from the bottom: 
            newFaceI = lastLine
            newFaceJ = j
            direction = UP
            if face == 5:
                newFace = 4
            elif face == 4:
                newFace = 2
            elif face == 2:
                newFace = 0
        elif (face == 1):
            #leaving face 1 by top, arriving on face 0 from the left: 
            newFaceI = j
            newFaceJ = 0
            newFace = 0
            direction = RIGHT
        elif (face == 3):
            #leaving face 3 by top, arriving on face 0 from the right: 
            newFaceI = lastLine - j
            newFaceJ = lastColumn
            newFace = 0
            direction = LEFT
        elif (face == 0):
            #leaving face 0 by top, arriving on face 5 by bottom: 
            newFaceI = lastLine
            newFaceJ = j
            newFace = 5
            direction = UP

        if isFree(newFaceI, newFaceJ, newFace, cube):
            return True, newFaceI, newFaceJ, direction, newFace
            
    elif i > lastLine:
        # Leaving face from Bottom : changing face if possible
        if (face == 0) or (face == 2) or (face == 4):
            #leaving face 0, 2 or 4 by bottom, arriving on face 2, 4 or 5 from the top: 
            newFaceI = 0
            newFaceJ = j
            direction = DOWN
            if face == 0:
                newFace = 2
            elif face == 2:
                newFace = 4
            elif face == 4:
                newFace = 5
        elif (face == 1):
            #leaving face 1 by bottom, arriving on face 4 from the left: 
            newFaceI = lastColumn - j
            newFaceJ = 0
            newFace = 4
            direction = RIGHT
        elif (face == 3):
            #leaving face 3 by bottom, arriving on face 4 from the right: 
            newFaceI = j
            newFaceJ = lastColumn
            newFace = 4
            direction = LEFT
        elif (face == 5):
            #leaving face 5 by bottom, arriving on face 0 by top: 
            newFaceI = 0
            newFaceJ = j
            newFace = 0
            direction = DOWN

        if isFree(newFaceI, newFaceJ, newFace, cube):
            return True, newFaceI, newFaceJ, direction, newFace



    return False, -1, -1, -1, -1


def updateGrille(pika, side, cube):

    initialPika = [pika[0], pika[1], pika[2], pika[3]]
    while not cube[initialPika[3]][initialPika[0]][initialPika[1]] == 1:
        nextI, nextJ, nextDirection, nextFace = getNextPosition(pika, cube, side)
        if nextFace != pika[3]:
            print("Pika move from face %d-(%d,%d) to face %d-(%d,%d)"%(pika[3], pika[0], pika[1], nextFace, nextI, nextJ), file=sys.stderr, flush=True)        
        if nextI == -1:
            break
        pika[0] = nextI
        pika[1] = nextJ 
        pika[2] = nextDirection
        pika[3] = nextFace
        cube[nextFace][nextI][nextJ] += 1

    for grille in cube:
        for line in grille: 
            strLine = ""
            for cell in line:
                strLine += str(cell)
            print(strLine)

print("size=%d - Side=%s"%(size, side), file=sys.stderr, flush=True)
print("Cube=%s"%cube, file=sys.stderr, flush=True)
print("Pika=%s"%pika, file=sys.stderr, flush=True)

updateGrille(pika, side, cube)
