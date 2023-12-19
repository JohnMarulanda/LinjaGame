import numpy as np

matrix = [
    [1, 1, 1, 1, 1, 1, 1, 2], 
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 2],
    [1, 2, 2, 2, 2, 2, 2, 2]
]

maxX = len(matrix[0])
minX = 0
maxY = len(matrix)
minY = 0

#----------------- Movements ------------------------

#check if values are btw values
def overflowCheck(array):
    if array[1] >= minX and array[1] < maxX and array[0] >= minY and array[0] < maxY:
        return True
    else:
        return False

#check if postion is 0
def positionCheck(coordTo):
    if  matrix[coordTo[0]][coordTo[1]] == 0:
        return True
    else:
        return False

#move one peace to another position
def movePiece(coordFrom, coordTo):
    if overflowCheck(coordFrom) and overflowCheck(coordTo) and positionCheck(coordTo):
        matrix[coordTo[0]][coordTo[1]] = matrix[coordFrom[0]][coordFrom[1]]
        matrix[coordFrom[0]][coordFrom[1]] = 0
        return True
    return False


#----------------- GameRules ------------------------

turn = 1 #1 = rojas, 2 = negras
countTurns = 0 #count turns inside a turn, max 2 turns per player


#Check if movement is posible
def checkMaxMovements(coordFrom, coordTo, maxMovements):
    if (abs(coordFrom[1] - coordTo[1]) + abs(coordFrom[0] - coordTo[0])) <= maxMovements:
        return True
    else:
        return False
    
def inputPlayer(coordFrom, coordTo):
    return 0

def inputOpponent():
    return 0

#----------------- Gameplay ------------------------


    


#[y, x]
print(movePiece([0,7], [2,5]))
print(np.array(matrix))

print(checkMaxMovements([0,7], [2,5], 4))