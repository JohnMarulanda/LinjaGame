import numpy as np

#----------------- Movements ------------------------

#check if values are btw values
def overflowCheck(matrix, array):
    maxX = len(matrix[0])
    minX = 0
    maxY = len(matrix)
    minY = 0
    if array[1] >= minX and array[1] < maxX and array[0] >= minY and array[0] < maxY:
        return True
    else:
        return False

#check if postion is 0
def positionCheck(matrix, coordTo):
    if  matrix[coordTo[0]][coordTo[1]] == 0:
        return True
    else:
        print("Regla: La posicion final debe estar vacia")
        return False

#move one peace to another position
def movePiece(matrix, coordFrom, coordTo):
    matrix[coordTo[0]][coordTo[1]] = matrix[coordFrom[0]][coordFrom[1]]
    matrix[coordFrom[0]][coordFrom[1]] = 0
    return matrix


#----------------- GameRules ------------------------

turn = 1 #1 = rojas, 2 = negras
countTurns = 0 #count turns inside a turn, max 2 turns per player


#Check if movement is posible
def ruleMaxMovements(coordFrom, coordTo, maxMovements):
    if (abs(coordFrom[1] - coordTo[1]) + abs(coordFrom[0] - coordTo[0])) <= maxMovements:
        return True
    else:
        return False

def ruleNoComeBack(coordFrom, coordTo, turn):
    if turn == 1 and coordFrom[1] < coordTo[1]:
        return True
    else:
        print("Regla: Se tiene que mover a otra columna y no se puede devolver")
        return False

def ruleOnlyMoveYourPeace(piece, turn):
    if piece == turn:
        return True
    else:
        print("Regla: no puedes mover la pieza de tu contrincante")
        return False
    
def inputPlayer(coordFrom, coordTo):
    return 0

def inputOpponent():
    return 0

#----------------- Gameplay ------------------------

def move(matrix, coordFrom, coordTo, turn):
    if overflowCheck(matrix, coordFrom) and overflowCheck(matrix, coordTo) and positionCheck(matrix, coordTo) and ruleNoComeBack(coordFrom, coordTo, turn):
        matrix = movePiece(matrix, coordFrom, coordTo)
        return matrix
    else:
        return False



"""m1 = [0, 0]
m2 = [0, 0]
count = 0
def setCoords(matrix, coord):
    if count == 0:
        m1 = coord
        count = 1
    else:
        m2 = coord
        count = 0
        matrix = move(matrix, m1, m2)
    
    return matrix"""
    
